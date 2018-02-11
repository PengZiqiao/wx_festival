from init_db import session, login, query, Friend

from time import sleep
from random import randint
from retrying import retry

MSG = [
    '衷心祝愿您及您全家在新的一年里身体健康!心想事成!万事如意!',
    '真诚地祝愿您在新的一年里：所有的期待都能出现、所有的梦想都能实现、所有的希望都能如愿、所有的努力都能成功!',
    '衷心祝愿您年年圆满如意，月月事事顺心，日日喜悦无忧，时时高兴欢喜!',
    '真诚地祝愿您在新一年里，快乐常在，好运常伴，成功相随，健康相陪，心想事成!'
]


def set_remark(friend):
    @retry(wait_fixed=randint(120, 180) * 1e4)
    def do():
        print('[*] SET REMARK', remark_name)
        friend.set_remark_name(remark_name)
        sleep(randint(2, 3))

    nick_name = friend.nick_name
    record = query.filter(Friend.nick_name == nick_name).first()

    if record:
        remark_name = record.remark_name
        if friend.remark_name == remark_name:
            print('[*] pass')
        else:
            do()
    else:
        print('[*] NOT IN')


def send(friend, msg):
    record = query.filter(Friend.nick_name == friend.nick_name).first()

    @retry(wait_fixed=randint(120, 180) * 1e4)
    def do():
        text = f'{name}，{msg}'
        print(text)
        friend.send(text)

    if record and record.done == False:
        if record.call_name == 'skip':
            print(f'SKIP')
        else:
            if record.call_name:
                name = record.call_name
            else:
                name = record.remark_name.split()[1]
            do()
        record.done = True
        session.add(record)
        session.commit()
    else:
        print('[*] Already sent')


def rest(friend):
    try:
        record = query.filter(Friend.nick_name == friend.nick_name).first()
        record.done = False
        session.add(record)
        session.commit()
    except AttributeError:
        pass


if __name__ == '__main__':
    bot = login()
    for i, each in enumerate(bot.friends()[1:]):
        print(f'[{i}] {each.nick_name}')
        # set_remark(each)
        rest(each)

        # msg = MSG[i % 4]
        # send(each, msg)
