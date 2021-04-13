import logging
import configparser
from pathlib import Path
import argparse
import os
import sys
import select
# import random
import zipfile
import re
from getpass import getpass

from tqdm import tqdm
from pyrogram.session import Session 
from pyrogram import Client, filters, types, session

BASE_FOLDER = Path(__file__).parent.absolute()
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
Session.notice_displayed = True # Disable notice from pyrogram

class Bot:
    def __init__(self, folder_name=BASE_FOLDER / Path("secret_data")):
        self.folder_name = folder_name
        self.__config = configparser.ConfigParser()
        self.__config.read(folder_name / "config.ini")

        self.app = Client(session_name=str(self.folder_name / "my_account"), api_id=self.__config['credentials']['pyrogram_api_id'],
                    api_hash=self.__config['credentials']['pyrogram_api_hash'], parse_mode="html", no_updates=True, hide_password=True) 

    def __enter__(self):
        self.app.start()
        return self.app
    
    def __exit__(self, type, value, traceback):
        self.app.stop()


def zipdir(dir_name):
    """
    Zip directory "dir_name" and name it as "zip_file"
    """
    zip_file = BASE_FOLDER / f'data/{dir_name.name}.zip'
    open(zip_file, "w")
    zipf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(dir_name):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(dir_name, '..')))
    zipf.close()
    return zip_file


def send_data(data: str, user:str = "me", data_type:str = "text", caption: str = None, as_file:bool = False, parse_mode = 'html'):
    """
    Connect to bot and send data to user
    """
    my_bot = Bot()
    with my_bot as app:
        if data_type == "text":
            if as_file:
                temp_file = BASE_FOLDER / "data/text_message.txt"
                with open(temp_file, "w") as f:
                    f.write(data)
                app.send_document(user, temp_file)
                temp_file.unlink()
            else:
                app.send_message(user, data, parse_mode = parse_mode)
        elif data_type == "file":
            with tqdm(total=100) as pbar:  
                def progress(current, total):
                    pbar.update(round(current * 100 / total, 4) - pbar.n) 
                if caption is not None:
                    app.send_document(user, data, caption=caption[:1024], progress=progress)
                else:
                    app.send_document(user, data, progress=progress)


def main():
    """
    Parse args, validate data
    """
    parser = argparse.ArgumentParser(description='Pipe stdout and files to telegram(via userbot)')
    parser.add_argument('message',  nargs='*', action="store", type=str, help='specify text of message to send, html parsing enabled, overwrites pipes.')
    parser.add_argument('-u', '--user', action="store", type=str, help='specify user to send, default is you.')
    parser.add_argument('-f', '--file', action="store", type=str, help='send file, text will be sended as caption. If folder is sended, will zip and send')
    parser.add_argument('-c', '--code', action='store_true', help='send text with <code> text to make it monospace')
    parser.add_argument('-F', '--force-file', action='store_true', help='send text in file even if it is shorter than 4096 symbols')
    parser.add_argument('--no-html', action='store_true', help='do not parse as html')
    parser.add_argument('--ansi-colors', action='store_true', help="don't remove ANSI escape codes from piped strings")
    parser.add_argument('--new-user', action='store_true', help='reloging to telegram')
    parser.add_argument('--new-app', action='store_true', help='enter new api_id/api_hash combination')
    args = parser.parse_args()
    
    # Pipe handling
    pipe = None
    if select.select([sys.stdin, ], [], [], 0.0)[0]:
        pipe = sys.stdin.read()
        if not args.ansi_colors:
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            pipe = ansi_escape.sub('', pipe)
    
    if args.no_html:
        parse_mode = None
    else:
        parse_mode = "html"

    # Text handling
    message_text = None
    if args.message:
        message_text = ' '.join(args.message)
    elif pipe is not None:
        message_text = pipe
    elif args.file is not None:
        pass
    else:
        print("No message to send, sending test message to Saved Messages. For help, use -h, --help.")
        # message_text = hex(random.randrange(0x10000000000, 0x99999999999))
        message_text = f"Hello World!\n\n\n<i>With Love from teleout</i>"

    as_file = False
    if message_text is None or len(message_text) > 4000 or args.force_file:
        as_file = True

    if args.code and not as_file:
        message_text = "<code>{}</code>".format(message_text)

    # File handling
    delete_file = False
    if args.file is not None:
        file = Path(args.file)
        if not file.exists():
            sys.exit(f'File "{file}" does not exists!')
            return
        elif file.is_dir():
            delete_file = True
            file = zipdir(file)
    
    # New user handling
    if args.new_user:
        session_file = BASE_FOLDER / Path("secret_data/my_account.session")
        if (session_file).exists():
            session_file.unlink()

    # New app id and hash handling
    config_file = BASE_FOLDER / Path("secret_data/config.ini")
    if not (config_file).exists() or args.new_app:
        if not (config_file).exists():
            print("No api_id and api_hash found, enter them\nYou can get them here: https://my.telegram.org/auth?to=apps")
        api_id = getpass("Enter api_id: ")
        api_hash = getpass("Enter api_hash: ")
        tmpl = open(BASE_FOLDER / Path("secret_data/config.ini.tmpl")).read()
        open(config_file, 'w').write(tmpl.format(api_id, api_hash))

    user = "me" if args.user is None else args.user
    if args.file is None:
        send_data(message_text, user=user, data_type="text", as_file=as_file, parse_mode=parse_mode)
    else:
        send_data(file, caption=message_text, user=user, data_type="file")
    if delete_file:
        file.unlink()

if __name__ == "__main__":
    main()
