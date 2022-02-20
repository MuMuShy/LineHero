from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from DataBase import DataBase


database = DataBase()
str=""
list = database.getCommandList()
for command in list:
    str+=command+"\n"+list[command][0]+"\n"

print(str)

