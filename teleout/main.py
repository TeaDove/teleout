import logging
import configparser
from pathlib import Path
import argparse
import os
import sys
import select
import random
import zipfile

from pyrogram.session import Session 
from pyrogram import Client, filters, types, session

BASE_FOLDER = Path(__file__).parent.absolute()
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
Session.notice_displayed = True # Disable notice 

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


def send_data(data: str, user:str = "me", data_type:str = "text", caption: str = None):
    """
    Connect to bot and send data to user
    """
    my_bot = Bot()
    with my_bot as app:
        if data_type == "text":
            if len(data) > 4096:
                logging.warning("Text is longer than 4096, sending as file")
                temp_file = BASE_FOLDER / "data/text_message.txt"
                with open(temp_file, "w") as f:
                    f.write(data)
                app.send_document(user, temp_file)
                temp_file.unlink()
            else:
                app.send_message(user, data)
        elif data_type == "file":
            if caption is None:
                app.send_document(user, data)
            else:
                app.send_document(user, data, caption=caption[:1024])


def main():
    """
    Parse args, validate data
    """
    parser = argparse.ArgumentParser(description='Pipe stdout and files to telegram(via userbot)')
    parser.add_argument('message',  nargs='?', action="store", type=str, help='define text of message to send, html parsing enabled, overwrites pipes.')
    parser.add_argument('-u', '--user', action="store", type=str, help='define user to send, default is you.')
    parser.add_argument('-f', '--file', action="store", type=str, help='send file, text will be sended as caption. If folder is sended, will zip and send')
    args = parser.parse_args()
    
    pipe = None
    if select.select([sys.stdin,],[],[],0.0)[0]:
        pipe = sys.stdin.read()
    
    message_text = None
    if args.message is not None:
        message_text = args.message
    elif pipe is not None:
        message_text = pipe
    elif args.file is not None:
        pass
    else:
        # Sending random data to yourself for testing, i.e. "0x668bde31670"
        logging.warning("No message to send, sending random hex numbers to me. For help, use -h, --help.")
        message_text = hex(random.randrange(0x10000000000, 0x99999999999))
    
    delete_file = False
    if args.file is not None:
        file = Path(args.file)
        if not file.exists():
            logging.error(f'File "{file}" does not exists!')
            return
        elif file.is_dir():
            delete_file = True
            file = zipdir(file)
    
    user = "me" if args.user is None else args.user
    if args.file is None:
        send_data(message_text, user = user, data_type="text")
    else:
        send_data(file, caption=message_text, user = user, data_type="file")
    if delete_file:
        file.unlink()

if __name__ == "__main__":
    main()