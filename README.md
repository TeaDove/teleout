# Teleout
Pipe stdout and files to telegram  
This software uses telegram bots  
Powered with love

# Examples
- `ls -la | teleout -u 418878871 -c` - send output of `ls -la` to chat `418878871` with monospace font
- `teleout -u 418878871 -f main.py "<b>This is main.py!</b>" --html` - send file *main.py*, with bolded text "This is main.py!"

# Features
1. Send files, text messages directly to telegram
2. Pipe to teleout(`ls | teleout` will work)
3. HTML parse mode supported
4. Easy install and use
5. Captions for files

# Manual
```shell                                                                    
usage: main.py [-h] [-u USER] [-f FILE] [-c] [-F] [-t TOKEN] [-n] [--html] [--ansi-colors] [message [message ...]]

Pipe stdout and files to telegram(via bots).

positional arguments:
  message               specify text of message to send, overwrites pipes.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  specify user with chat_id to send
  -f FILE, --file FILE  send file, text will be sent as caption.
  -c, --code            send text with <code> text to make it monospace, apply tags escaping and send as html
  -F, --force-file      send text in file even if it is shorter than 4096 symbols
  -t TOKEN, --token TOKEN
                        specify telegram api token. if not set will use default
  -n, --new             use with --token or --user to set new default
  --html                parse as html and apply <b>, <i> etc. tags
  --ansi-colors         don't remove ANSI escape codes from piped strings
```

# Installation
1.
- From pip   
```pip install teleout```
- From git  
```shell
wget https://raw.githubusercontent.com/TeaDove/teleout/master/teleout/main.py -O teleout.py && chmod u+x teleout.py
```
3. Get bot token from [@BotFather](https://t.me/BotFather)
4. Start teleout with `teleout`, enter your token, default chat id.
5. Enjoy!<br>
Works fine on Linux and Mac OS. 
> don't worry, there are no sniffer and smth like that

> for feedbacks, write me [here](https://t.me/teas_feedbacks_bot)<br>
inspired by https://termbin.com
