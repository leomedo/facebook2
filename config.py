import os


class Config(object):
    BOT_TOKEN = os.environ.get("Telegram_Bot_Token")
    User_Id = int(os.environ.get("User_Id"))
    link_after_login = os.environ.get("Telegram_Bot_Token", "https://www.midasbuy.com/midasbuy/sa/homepage/pubgm")
