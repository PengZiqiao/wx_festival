import wxpy as wx
import os.path

class WxFestival:
    def __init__(self):
        path = os.path.dirname(__file__)
        qr_path = os.path.join(path, 'files/qr.png')
        cache_path = os.path.join(path, 'files/cache.pkl')
        print('>>> 初始化微信...')
        self.bot = wx.Bot(cache_path=cache_path, qr_path=qr_path)
        print('>>> 获取好友列表...')
        self.friend_list = self.bot.friends()

    def set_message(self):
        text = input(">>> 请输入短信内容：")
        return text

    def start_send(self):
        msg_text = self.set_message()
        length = len(self.friend_list)
        for i, each in enumerate(self.friend_list):
            name = each.name
            print(f">>> 即将向好友【{name}】发送消息（进度：{i}/{length}）。")
            cmd = input(">>> 按【回车】，直接发送；输入【称呼（自定义）】，改变短信中称呼；输入【skip】，跳过此好友：")
            if cmd:
                if cmd == 'skip':
                    continue
                else:
                    name = cmd
            each.send_msg(f"{name}，{msg_text}")


if __name__ == '__main__':
    wf =WxFestival()
    wf.start_send()
