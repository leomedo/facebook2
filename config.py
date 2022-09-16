import os


class Config(object):
    BOT_TOKEN = os.environ.get("Telegram_Bot_Token")
    User_Id = int(os.environ.get("User_Id"))