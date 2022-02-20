from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from DataBase import DataBase


database = DataBase()

print(database.checkUser(""))

