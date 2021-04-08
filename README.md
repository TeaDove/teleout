# Teleout
Pipe stdout and files to telegram(via user)<br>
Powered with love(and python with [pyrogram](https://github.com/pyrogram/pyrogram))

# Features
1. Send files, directories(they are ziped automatically), text messages directly to telegram
2. Pipe to teleout
3. HTML parse mode supported
4. Easy install and use
5. Captions for files

![Example](https://user-images.githubusercontent.com/12380279/114037653-d8ca2500-9889-11eb-9950-13fa22cb7906.mp4)

# Manual
```                                                                    
usage: main.py [-h] [-u USER] [-f FILE] [--new-user] [--new-app] [message [message ...]]

Pipe stdout and files to telegram(via userbot)

positional arguments:
  message               specify text of message to send, html parsing enabled, overwrites pipes.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  specify user to send, default is you.
  -f FILE, --file FILE  specify file to send, text will be sended 
            as caption. If folder is specified, will zip and send             
  --new-user            reloging to telegram
  --new-app             enter new api_id/api_hash combination
```

# Example
- `ls -la | teleout -u teadove` - send output of `ls -la` to user [@TeaDove](https://t.me/teadove)
- `teleout -u teadove -f main.py "<b>This is main.py!</b>"` - send file *main.py*, to [@TeaDove](https://t.me/teadove), with bolded text "This is main.py!"
- `teleout -f data` - zip folder *data* and send it to *Saved Messages*

# Installation
1. ```pip3 install git+https://github.com/TeaDove/teleout```
2. Get api\_id and api\_hash from [here](https://my.telegram.org/auth?to=apps)
3. Start teleout with `teleout`, enter your api\_id, api\_hash, loggin, code and password.
5. Enjoy!<br>
Works fine on Linux and Mac OS. 
> don't worry, there are no sniffer and smth like that

# Requirements
```
python>=3.7
pyrogram>=1.0.7
tgcrypto
```

# TODO
1. Omit pyrogram errors while sending big files 
2. Progress bars for big files and folders

> for feedbacks, write me [here](https://t.me/teas_feedbacks_bot)
inspired by https://termbin.com