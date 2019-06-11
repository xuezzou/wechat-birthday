## Python + itchat: auto-greeting for friend's birthdays on Wechat

### Introduction
A python app that can send birthday messages to wechat friends on pre-defined specific date and time

### Dependencies
- [itchat](https://github.com/littlecodersh/ItChat) - wechat api
- [APScheduler](https://apscheduler.readthedocs.io/en/latest/) - scheduling

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
### Reference
- [EverydayWechat](https://github.com/sfyc23/EverydayWechat)