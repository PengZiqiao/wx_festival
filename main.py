from init_db import FriendDatabase


msg_text = '新年快乐，万事如意！'

class WxFestival:
    def __init__(self):
        self.db = FriendDatabase()

        print('>>> 初始化微信...')
        self.bot = self.db.bot
        print('>>> 获取好友列表...')
        self.friend_list = self.bot.friends()

    

    def iter_send(self):
        length = len(self.friend_list)

        for i, each in enumerate(self.friend_list):
            db_friend = self.db.db_friends.filter_by(
                nick_name=each.nick_name).first()
            call = db_friend.call_name
            if db_friend and (call == 'skip' or db_friend.already_send):
                print(f">>> 跳过【{each.remark_name}】（进度：{i+1}/{length}）。")
                continue
            else:
                msg = f"{call}，{msg_text}"
                print(f">>> 【{each.remark_name}({each.nick_name})】：{msg}（进度：{i+1}/{length}）。")
                each.send_msg(msg)
                db_friend.already_send = True
                self.db.session.commit()


if __name__ == '__main__':
    wf = WxFestival()
    input('continue..')
    wf.iter_send()
