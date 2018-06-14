from model import Friend, Session, Base, engine
from wxpy import Bot
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
        # 添加新好友
        new_friends = []
        for wx_friend in self.wx_friends:
            if not self.db_friends.filter_by(nick_name=wx_friend.nick_name).first():
                new_friends.append(wx_friend)
        self.insert(new_friends)

        # 加入删除数据库中已被删除的好友逻辑
        delet_friends = []
        for db_friend in self.db_friends:
            if not self.wx_friends.search(db_friend.nick_name):
                delet_friends.append(db_friend.nick_name)
        if delet_friends:
            self.db_friends.filter(Friend.nick_name.in_(delet_friends)).delete(synchronize_session=False)
            self.session.commit()
        print(f'[*] {len(delet_friends)} friends have been deleted.')

    def update_remark_name(self):
        n = 0
        for wx_friend in self.wx_friends:
            db_friend = self.db_friends.filter_by(nick_name=wx_friend.nick_name).first()
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
    fdb.update_friend_list()
