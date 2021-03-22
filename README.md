# Teleout
Pipe stdout and files to telegram(via user)

# Man
```                                                                    
usage: teleout [-h] [-u U] [-f FILE] [message]

Pipe stdout and files to telegram(via userbot)

positional arguments:
  message               define text of message to send, html parsing enabled, overwrites pipes.

optional arguments:
  -h, --help            show this help message and exit
  -u U                  define user to send, default is you.
  -f FILE, --file FILE  send file, text will be sended as caption. If folder is sended, will zip and send
```

# Example
- `ls -lah | teleout -u teadove` - send output of `ls -lah` to user [@teadove](https://t.me/teadove)
- `teleout -u teadove -f main.py "<b>This is main.py!</b>"` - send file *main.py*, to [@teadove](https://t.me/teadove), with bolded text "This is main.py!"
- `teleout -f data` - zip folder *data* and send it to *Saved Messages*

# Installation
1. `pip3 install git+https://github.com/TeaDove/teleout`
2. Go to folder with package. Should be smth like `~/.local/lib/python3.8/site-packages/teleout`
3. In folder *secret_data* create file *config.ini*. See README.md in that folder fore more info.
4. start teleout with `teleout`, enter your loggin and password.
5. Enjoy!
