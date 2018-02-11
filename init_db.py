from model import engine, Base, Friend, Session
from wxpy import Bot

session = Session()
query = session.query(Friend)


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def login():
    return Bot(True)


def add(friend):
    if query.filter(Friend.nick_name == friend.nick_name).first():
        print(f'[*] {friend.nick_name} is already in database.')
    else:
        print(f'[*] add {friend.nick_name} to database.')
        f = Friend()
        f.nick_name = friend.nick_name
        f.remark_name = friend.remark_name
        f.done = False
        session.add(f)


if __name__ == '__main__':
    bot = login()
    for i, friend in enumerate(bot.friends()):
        print(f'[{i}]')
        add(friend)
        session.commit()
