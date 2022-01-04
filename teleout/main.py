#!/usr/bin/env python3

from typing import Union
from pathlib import Path
from urllib.parse import urljoin
from getpass import getpass
import argparse
import os
import json
from json.decoder import JSONDecodeError
import sys
import select
import re
import html
import tempfile

import requests

CONFIG_FOLDER = Path(os.path.expanduser("~")) / ".config"
CONFIG_FOLDER.mkdir(exist_ok=True)
CONFIG_FILE = CONFIG_FOLDER / "teleout.json"
CONFIG_FILE.touch(exist_ok=True)

BASE_URL = "https://api.telegram.org/bot{}/sendMessage"


def send_data(
    data: Union[Path, str],
    quite: bool,
    token: str,
    user: str,
    data_type: str = "text",
    caption: str = None,
    as_file: bool = False,
    parse_mode: str = "html",
):
    """
    Connect to bot and send data to user
    """
    compiled_url = BASE_URL.format(token)
    if data_type == "text":
        if as_file:
            with tempfile.NamedTemporaryFile(prefix="message_", suffix=".txt") as fp:
                fp.write(data.encode())
                fp.seek(0)
                params = {"chat_id": user}
                if quite:
                    params["disable_notification"] = True
                response = requests.post(
                    urljoin(compiled_url, "sendDocument"),
                    params=params,
                    files={"document": fp},
                )
        else:
            params = {"chat_id": user, "text": data}
            if parse_mode is not None:
                params["parse_mode"] = parse_mode
            if quite:
                params["disable_notification"] = True
            response = requests.post(
                urljoin(compiled_url, "sendMessage"), params=params
            )
    elif data_type == "file":
        params = {"chat_id": user}
        if caption is not None:
            params["caption"] = caption[:1024]
        if parse_mode is not None:
            params["parse_mode"] = parse_mode
        if quite:
            params["disable_notification"] = True
        fp = open(data, "rb")
        response = requests.post(
            urljoin(compiled_url, "sendDocument"),
            params=params,
            files={"document": fp},
        )

    if not response.ok:
        sys.exit(
            f"Error from telegram!\nstatus_code: {response.status_code}\nContent: {response.text}"
        )


def parser_handler():
    """
    Parse args, validate data
    """
    parser = argparse.ArgumentParser(
        description="Pipe stdout and files to telegram(via bots)."
    )
    parser.add_argument(
        "message",
        nargs="*",
        action="store",
        type=str,
        help="specify text of message to send, overwrites pipes.",
    )
    parser.add_argument(
        "-u",
        "--user",
        action="store",
        type=str,
        help="specify user with chat_id to send",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        type=str,
        help="send file, text will be sent as caption.",
    )
    parser.add_argument(
        "-c",
        "--code",
        action="store_true",
        help="send text with <code> text to make it monospace, apply tags escaping and send as html",
    )
    parser.add_argument(
        "-F",
        "--force-file",
        action="store_true",
        help="send text in file even if it is shorter than 4096 symbols",
    )
    parser.add_argument(
        "-t",
        "--token",
        action="store",
        type=str,
        help="specify telegram api token. " "if not set will use default",
    )
    parser.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="use with --token or --user to set new default",
    )
    parser.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help="send message without notifications, default is false",
    )
    parser.add_argument(
        "--html", action="store_true", help="parse as html and apply <b>, <i> etc. tags"
    )
    parser.add_argument(
        "--ansi-colors",
        action="store_true",
        help="don't remove ANSI escape codes from piped strings",
    )
    args = parser.parse_args()

    # Pipe handling
    pipe = None
    if select.select(
        [
            sys.stdin,
        ],
        [],
        [],
        0.0,
    )[0]:
        pipe = sys.stdin.read()
        if not args.ansi_colors:
            ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
            pipe = ansi_escape.sub("", pipe)

    if args.html:
        parse_mode = "html"
    else:
        parse_mode = None

    # Text handling
    message_text = None
    if args.message:
        message_text = " ".join(args.message)
    elif pipe is not None:
        message_text = pipe
    elif args.file is not None:
        pass
    else:
        print(
            "No message to send, sending lirum test message. For help, use -h, --help."
        )
        message_text = f"Hello World!\n\n\n<i>With Love from teleout</i>"
        parse_mode = "html"

    try:
        config_dict = json.load(open(CONFIG_FILE, "r"))
    except JSONDecodeError:
        config_dict = {}

    token = args.token or config_dict.get("token")
    if token is None:
        print("No bot token found, enter it\nYou can find it in @BotFather")
        token = getpass("Enter token: ")
        config_dict["token"] = token

    user = args.user or config_dict.get("user")
    if user is None:
        print("No chat id found, enter it\nYou can find it in @get_useridbot")
        user = input("Enter chat id: ")
        config_dict["user"] = user

    if args.new:
        if args.token:
            config_dict["token"] = token
            print("New token saved!")
        elif args.user:
            config_dict["user"] = user
            print("New chat_id saved!")
        else:
            sys.exit("Error, no --user or --token specified")

    json.dump(config_dict, open(CONFIG_FILE, "w"))
    if args.new:
        return

    as_file = False
    if message_text is None or len(message_text) > 4000 or args.force_file:
        as_file = True

    if args.code and not as_file:
        message_text = html.escape(message_text)
        message_text = "<code>{}</code>".format(message_text)
        parse_mode = "html"

    # File handling
    filepath = None if args.file is None else Path(args.file)
    if filepath is not None:
        if not filepath.exists():
            sys.exit(f'File "{filepath}" does not exists!')
        elif filepath.is_dir():
            sys.exit(
                f"Cannot send directory, zip it first with: zip -r {filepath}.zip {filepath}"
            )

    quite = args.quite or False
    if args.file is None:
        send_data(
            message_text,
            token=token,
            user=user,
            data_type="text",
            as_file=as_file,
            parse_mode=parse_mode,
            quite=quite,
        )
    else:
        send_data(
            filepath,
            token=token,
            caption=message_text,
            user=user,
            data_type="file",
            quite=quite,
        )


def main():
    try:
        parser_handler()
    except KeyboardInterrupt:
        sys.exit("\nCancelling...")


if __name__ == "__main__":
    main()
