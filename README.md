# Teleout
Pipe stdout and files to telegram(via user)<br>
Powered with love(and python with [pyrogram](https://github.com/pyrogram/pyrogram))

# Features
1. Send files, directories(they are ziped automatically), text messages directly to telegram
2. You can pipe to teleout
3. HTML parse mode supported
4. Easy install and use
5. Captions for files

# Manual
```                                                                    
usage: teleout [-h] [-u U] [-f FILE] [message]

Pipe stdout and files to telegram(via userbot)

positional arguments:
  message               define text of message to send, html parsing enabled, overwrites pipes.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  define user to send, default is you.
  -f FILE, --file FILE  send file, text will be sended as caption. 
        If folder is sended, will zip and send
```

# Example
- `ls -lah | teleout -u teadove` - send output of `ls -lah` to user [@teadove](https://t.me/teadove)
- `teleout -u teadove -f main.py "<b>This is main.py!</b>"` - send file *main.py*, to [@teadove](https://t.me/teadove), with bolded text "This is main.py!"
- `teleout -f data` - zip folder *data* and send it to *Saved Messages*

# Installation
1. ```pip3 install git+https://github.com/TeaDove/teleout```
2. Go to folder with package. Should be smth like `~/.local/lib/python3.8/site-packages/teleout`
3. In folder *secret_data* create file *config.ini*. See [README.md](https://github.com/TeaDove/teleout/tree/master/teleout/secret_data) in that folder for more info.
4. start teleout with `teleout`, enter your loggin, code and password.
5. Enjoy!<br>
Works fine on Linux and Mac OS. 
> don't worry, there are no sniffer and smth like it

# Requirements
```
python>=3.7
pyrogram>=1.0.7
tgcrypto
```

# TODO
1. Find way to import session and config.ini(maybe via argparse)
2. More features

> for feedbacks, write me [here](https://t.me/teas_feedbacks_bot)