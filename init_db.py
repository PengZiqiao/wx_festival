from model import engine, Base, Friend, Session
from wxpy import Bot

class FriendDB:
    def __init__(self):
        self.session = Session()
        self.bot = Bot(True)
      
    def init_db(self, add_all=False):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        
        # 初始化数据库同时添加插入所有好友记录
        if add_all:
            friends = self.bot.friends()
            for i, friend in enumerate(friends):
                print(f'[*] {i}/{len(friends)} {friend.remark_name}')
                self.insert(friend)
            self.session.commit()

    def update(self):
        friends = self.bot.friends()
        n = 0
        for i, friend in enumerate(friends):    
            progress_rate = f'{i}/{len(friends)}'
            if self.session.query(Friend).filter(Friend.nick_name == friend.nick_name).first():
                print(f'[*] {progress_rate} {friend.remark_name} is already in database.')
            else:
                print(f'[*] {progress_rate} {friend.remark_name} is a new friend.')
                self.insert(friend)
                n+=1
        self.session.commit()
        print(f'{n} friends has been inserted in database.')

    def insert(self, friend):
        f = Friend()
        f.nick_name = friend.nick_name
        f.remark_name = friend.remark_name
        f.already_send = False
        self.session.add(f)
        print(f'[*] {friend.nick_name} has been inserted to database.')
