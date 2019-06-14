## Python + itchat: auto-greeting for friend's birthdays on Wechat

### Introduction
A python app that can send birthday messages to wechat friends on pre-defined specific date and time

### Dependencies 
- [itchat](https://github.com/littlecodersh/ItChat) - wechat api
    ```python 
    # use itchat to send message
    itchat.send(friend.message, toUserName=friend.id)
    ```
- [APScheduler](https://apscheduler.readthedocs.io/en/latest/) - scheduling
    ```python 
    # use APScheduler to schedule the events
    scheduler.add_job(self.send_message, 'cron', 
                      month=friend.month, day=friend.day, hour=friend.hour, minute=friend.minute, second=0,
                              args=[friend])
    ```

### Use
file `friends_info.json` must provide wechat_name and birthday, may provide send_time and message
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
    - make send message in a group possible
    - May have another acount in a group that send birthday message for everyone in the group
    - if `is_group` is true and `group_name` provided in the constructor, message would @ the person and send the message to that group
    ```python
    wechat_birthday_bot = wechat_birthday(True, "serh gut")
    wechat_birthday_bot.run()
    ```
### Reference
- [EverydayWechat](https://github.com/sfyc23/EverydayWechat)