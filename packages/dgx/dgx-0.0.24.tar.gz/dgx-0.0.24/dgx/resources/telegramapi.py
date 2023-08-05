from const import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from requests import get
from logging import info
from datetime import datetime
from json import dumps
import traceback
import re


class TelegramMessage:

    def __init__(self, token: str, chat_id: str, parse_mode: str, msg: str or list) -> None:
        self.__token = token
        self.__chat_id = chat_id
        self.__parse_mode = parse_mode
        self.__lines = list()
        if msg:
            if isinstance(msg, str):
                self.add_line(msg)
            elif isinstance(msg, list, tuple):
                self.__lines.extend(msg)
            else:
                raise Exception("%s is not supported" % type(msg))

    def __enter__(self):
        return self

    def add_line(self, msg: str):
        """Agrega linea de mensaje"""
        msg = re.sub(' +', ' ', msg)  # quita espacios en blancos
        spl = [ln.strip() for ln in msg.splitlines() if ln.strip()]
        self.__lines.extend(spl)

    def send(self) -> dict:
        """Send a message"""
        self.__lines.insert(0, "Datetime: %s" % datetime.now().strftime(r"%b %d %Y %H:%M:%S"))
        data: str = '\n'.join(self.__lines)
        res = get("https://api.telegram.org/bot{}/sendmessage?chat_id={}&text={}&parse_mode={}".format(self.__token, self.__chat_id, data, self.__parse_mode))
        return res.json()

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        else:
            res = self.send()
            info(dumps(res, indent=2))
        return True


class TelegramAPI:

    token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    parse_mode = "html"

    def __init__(self, token: str = None, chat_id: str = None):
        if token:
            self.token = token
        if chat_id:
            self.chat_id = chat_id

    def __enter__(self, *_):
        return self

    @classmethod
    def send_message(self, msg: str or list = None) -> dict or TelegramMessage:
        """
        Create and send a new message
        """
        if msg:
            return TelegramMessage(self.token, self.chat_id, self.parse_mode, msg).send()
        else:
            return TelegramMessage(self.token, self.chat_id, self.parse_mode, msg)

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        return True


if __name__ == '__main__':
    # Sample using with
    with TelegramAPI() as tl:
        # send simple message
        tl.send_message("This a simple msg")
        # send a multiline message
        with tl.send_message() as msg:
            msg.add_line("This a long msg")
            msg.add_line("<i>Number: <b>4</b></i>")
            msg.add_line("<i>Number: <b>5</b></i>")
            msg.add_line("<i>Result: <b>20</b></i>")
    # Simple msg
    msg = """
    This a long msg
    <i>Number: <b>4</b></i>
    <i>Number: <b>5</b></i>
    <i>Result: <b>20</b></i>
    """
    TelegramAPI.send_message(msg)
