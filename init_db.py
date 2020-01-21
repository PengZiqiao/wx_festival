from model import Friend, Session, Base, engine
from wxpy import Bot, ensure_one
from retrying import retry


class FriendDatabase:
    def __init__(self):
        self.session = Session()
        self.bot = Bot(True)

    @property
    def db_friends(self):
        return self.session.query(Friend)

    @property
    def wx_friends(self):
        return self.bot.friends()

    def init_db(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.insert(self.wx_friends)

    def update_friend_list(self):
        # 删除数据库中已被删除的好友
        delet_friends = []
        for db_friend in self.db_friends:
            wx_search_result = self.wx_friends.search(db_friend.nick_name)
            if wx_search_result:
                try:
                    wx_friend = ensure_one(wx_search_result)
                    not_same = wx_friend.nick_name!=db_friend.nick_name
                except ValueError:
                    print(f'>>>have a look at {db_friend}')
            if not wx_search_result or not_same:
                delet_friends.append(db_friend.nick_name)
        if delet_friends:
            self.db_friends.filter(Friend.nick_name.in_(
                delet_friends)).delete(synchronize_session=False)
            self.session.commit()
            print(f'[*] {len(delet_friends)} friends have been deleted.')

        # 添加新好友
        new_friends = []
        for wx_friend in self.wx_friends:
            if not self.db_friends.filter_by(nick_name=wx_friend.nick_name).first():
                new_friends.append(wx_friend)
        self.insert(new_friends)

    def update_remark_name(self):
        # 用数据库中remark_name更新微信中好友备注
        n = 0
        for wx_friend in self.wx_friends:
            db_friend = self.db_friends.filter_by(
                nick_name=wx_friend.nick_name).first()
            if db_friend and (wx_friend.remark_name != db_friend.remark_name):
                self.set_remark_name(wx_friend, db_friend.remark_name)
                n += 1
        print(f"{n} friends's remark_name has been modified.")

    @retry(wait_fixed=12e5)
    def set_remark_name(self, wx_friend, remark_name):
        print(f"[*] SET {wx_friend.nick_name}'s remark_name as {remark_name}.")
        wx_friend.set_remark_name(remark_name)

    def insert(self, friends):
        mappings = (
            {
                'nick_name': each.nick_name,
                'remark_name': each.remark_name,
                'already_send': False
            }
            for each in friends
        )
        self.session.bulk_insert_mappings(Friend, mappings)
        self.session.commit()
        print(f'[*] {len(friends)} friends have been inserted to database.')


if __name__ == '__main__':
    fdb = FriendDatabase()
    # fdb.update_friend_list()
    fdb.update_remark_name()
