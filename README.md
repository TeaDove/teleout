# Teleout
Pipe stdout and files to telegram<br>
This software uses userbots, so you can send messages from **your** account<br><br>
Powered with love(and python with [pyrogram](https://github.com/pyrogram/pyrogram))

# Examples
- `ls -la | teleout -u teadove -c` - send output of `ls -la` to user [@TeaDove](https://t.me/teadove) with monospace font
- `teleout -u teadove -f main.py "<b>This is main.py!</b>" --html` - send file *main.py*, to [@TeaDove](https://t.me/teadove), with bolded text "This is main.py!"
- `teleout -f data` - zip folder *data* and send it to *Saved Messages*

# Features
1. Send files, directories(they are ziped automatically), text messages directly to telegram
2. Pipe to teleout(`ls | teleout` will work)
3. HTML parse mode supported
4. Easy install and use
5. Captions for files

<!-- ![Example](https://user-images.githubusercontent.com/12380279/114037653-d8ca2500-9889-11eb-9950-13fa22cb7906.mp4) -->

# Manual
```                                                                    
usage: teleout [-h] [-u USER] [-f FILE] [-c] [-F] [--new-user] [--new-app] [--html] [--ansi-colors] [message [message ...]]

Pipe stdout and files to telegram(via userbot).

positional arguments:
  message               specify text of message to send, html parsing enabled, overwrites pipes.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  specify user to send, default is you.
  -f FILE, --file FILE  send file, text will be sended as caption. If folder is sended, will zip and send
  -c, --code            send text with <code> text to make it monospace, apply tags escaping and send as html
  -F, --force-file      send text in file even if it is shorter than 4096 symbols
  --new-user            reloging to telegram
  --new-app             enter new api_id/api_hash combination
  --html                parse as html and apply <b>, <i> etc. tags
  --ansi-colors         don't remove ANSI escape codes from piped strings
```

# Installation
1. ```pip install teleout```
2. Get api\_id and api\_hash from [here](https://my.telegram.org/auth?to=apps)
3. Start teleout with `teleout`, enter your api\_id, api\_hash, loggin, code and password.
5. Enjoy!<br>
Works fine on Linux and Mac OS. 
> don't worry, there are no sniffer and smth like that

# Requirements
```
python>=3.7
pyrogram>=1.0.7
tqdm>=4.57.0
tgcrypto
```
# TODO
- [ ] UI for sending messages to chats without username
- [ ] Bots support

> for feedbacks, write me [here](https://t.me/teas_feedbacks_bot)<br>
inspired by https://termbin.com
