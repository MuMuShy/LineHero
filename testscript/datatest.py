from re import I
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import sys

sys.path.insert(0, '../')
from DataBase import DataBase
database = DataBase()
str=""
list = database.getCommandList()
for command in list:
    str+=command+"\n"+list[command][0]+"\n"

print(database.getUserRank("U0b37a9d05272a9e82d0ee60ba10bdd72"))

