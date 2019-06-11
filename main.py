import os
import time
from datetime import datetime
import json
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler

DATA_FILE = 'friends_info.json'

DEFAULT_MESSAGE = '生日快乐'
DEFAULT_TIME = '0:00'

# a class for a friend that help better organize the structure
class friend:
    def __init__(self, 
                 wechat_name, 
                 birthday,
                 send_time, 
                 nickname, 
                 message, 
                 is_lunar):
        self.wechat_name = wechat_name
        self.message = '{}，{}！'.format(nickname, message)
        month, day = [int(x) for x in birthday.split('.')]
        hour, minute = [int(x) for x in send_time.split(':')]
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.is_lunar = is_lunar
        self.id = None

    # for testing purpose
    def __repr__(self):
        return 'Send {} on {}.{} {}:{} with message: {} '.format(self.wechat_name, 
                                                                 self.month, self.day, self.hour, self.minute, 
                                                                 self.message)


class wechat_birthday:
    def __init__(self):
        self.friend_list = self.get_data()


    def get_data(self):
        """
        initialize the data
        :return: a friend list that contains friend instance
        """
        # grab data from json file containing friend's info
        friends = []
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            friends_list = json.load(file)["friends"]
        for each_friend in friends_list:
            # deal with default values
            if "nickname" not in each_friend:
                each_friend['message'] = each_friend['wechat_name']
            if "message" not in each_friend:
                each_friend['message'] = DEFAULT_MESSAGE
            if "send_time" not in each_friend:
                each_friend['send_time'] = DEFAULT_TIME
            if "is_lunar" not in each_friend:
                each_friend['is_lunar'] = False 
            friends.append(friend(each_friend['wechat_name'], 
                                  each_friend['birthday'],
                                  each_friend['send_time'],
                                  each_friend['nickname'],
                                  each_friend['message'],
                                  each_friend['is_lunar']))
        return friends


    @staticmethod
    def is_online(auto_login=False):
        """
        check if still online
        :param auto_login: bool, True if offline then auto login (default is False)。
        :return: bool, True，online; False offline
        """
        def _online():
            """
            check through if successfully grab user's wechat friends' data 
            :return: bool, true，online; False offline
            """
            try:
                if itchat.search_friends():
                    return True
            except IndexError:
                return False
            return True

        if _online():
            return True
        # only check if online without auto login
        if not auto_login:
            return _online()

        # try five times login
        for _ in range(5):
            # cmd line display QR Code
            if os.environ.get('MODE') == 'server':
                itchat.auto_login(enableCmdQR=2, hotReload=True)
            else:
                itchat.auto_login(hotReload=True)
            if _online():
                print('Sucessfully login')
                return True

        print('Failed to login')
        return False


    def run(self):
        """
        main program
        :return:None
        """
        # login wechat
        if not self.is_online(auto_login=True):
            return

        # schedule event
        scheduler = BlockingScheduler()

        for friend in self.friend_list:
            wechat_name = friend.wechat_name
            friends = itchat.search_friends(name=wechat_name)
            if not friends:
                print('wechat name {} does not exist'.format(wechat_name))
                return
            if len(friends) > 1:
                print('wechat name {} has duplicates'.format(wechat_name))
                return
            # tie the corresponding unique id
            friend.id = friends[0].get('UserName')
            # add job to scheduler
            scheduler.add_job(self.send_message, 'cron', 
                              month=friend.month, day=friend.day, hour=friend.hour, minute=friend.minute, second=0,
                              args=[friend])

        scheduler.start()

            
    def send_message(self, friend):
        """
        send hbd message
        :param friend: friend contains the msg
        :return: None
        """
        if self.is_online(auto_login=True):
            itchat.send(friend.message, toUserName=friend.id)
            # prevent to send msg too fast
            time.sleep(5)

        # flag for successfully send the msg
        print(friend)
        print('Send successfully...\n')


if __name__ == '__main__':
    wechat_birthday_bot = wechat_birthday()
    # test the friend list 
    # print(wechat_birthday_bot.friend_list)
    # run the main program
    wechat_birthday_bot.run()
    