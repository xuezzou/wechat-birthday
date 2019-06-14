## Python + itchat: auto-greeting for friend's birthdays on Wechat

### Introduction
A python app that can send birthday messages to wechat friends or a group on pre-defined specific date and time

### Dependencies 
- [itchat](https://github.com/littlecodersh/ItChat) - wechat api
    ```python 
    # use itchat to send message
    itchat.send(message, toUserName=id)
    ```
- [APScheduler](https://apscheduler.readthedocs.io/en/latest/) - scheduling
    ```python 
    # use APScheduler to schedule the events
    scheduler.add_job(self.send_message, 'cron', 
                      month=friend.month, day=friend.day, hour=friend.hour, 
                      minute=friend.minute, second=0,
                      args=[friend])
    ```

### Use
- data file `friends_info.json`     
    - must provide 
        - **wechat_name** 
        - **birthday**
    - recommend provide, 
        - **nickname** 
            - default: wechat_name
        - **send_time** 
            - default: '0:00'
        - **message** 
            - default: '生日快乐'
    ```javascript
    {
        "wechat_name": "小白",
        "birthday": "6.11",
        "nickname": "大猪头"
    },
    {
        "wechat_name": "小黑",
        "birthday": "6.11",
        "send_time": "11:00",
        "message": "生快，快生！！"
    },
    ```
    - message would be `'{}，{}！'.format(nickname, message)` if not send in a group
- Send to a **Group**
    - send message in a **group** instead of send to the friend directly
    - if `is_group` is true and `group_name` provided in the constructor, message would @ the person and send the message to that group
    ```python
    wechat_birthday_bot = wechat_birthday(True, "serh gut")
    wechat_birthday_bot.run()
    ```
    - message would be `''@' + '{}\n{}'.format(friend.wechat_name, friend.message)` if send in a group

<!-- ### Illustration -->

### Run

`pip3 install -r requirements.txt`
`python3 main.py`

or use docker
```
sudo docker build -t wechat_birthday .
sudo docker run --name 'directory'
# login thru QRCode
# Ctrl+P+Q exit the container
```

### Limitation
- Could not simultaneously login wechat web and this app
    - May have another account in a group that send birthday message for everyone in the group

### Reference
- [EverydayWechat](https://github.com/sfyc23/EverydayWechat)