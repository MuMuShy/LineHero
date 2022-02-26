from attr import dataclass
import psycopg2
from psycopg2.extras import Json
import sys
import json
import random
import os
import time
import math
import random
from datetime import datetime, timedelta
# adding Folder_2 to the system path
sys.path.insert(0, '../')
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,FlexSendMessage
)
from DataBase import DataBase
dataBase = DataBase()
DATABASE_URL = os.environ['DATABASE_URL']

environment = os.getenv("ENVIRONMENT")
print("environment: "+environment)
if environment =="DEV":
    print("本地開發 使用本地開發版本機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_DEV"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET_DEV"))  
else:
    print("線上heroku環境 預設線上版機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET"))

def checkstrjobLegal(job):
    _jobs = ["warrior","majic","rog"]
    if job in _jobs:
        return True
    else:
        return False
def getjobChinese(job):
    if checkstrjobLegal(job):
        _parser = {"warrior":"戰士","majic":"法師","rog":"盜賊"}
        return _parser[job]
    else:
        return "error"

def createrJob(user_line_id,jobs):
    _reply = ""
    if dataBase.checkUserHasJob(user_line_id):
        _reply = "你已經有職業了喔!"
        return _reply
    else:
        dataBase.createUserJob(user_line_id,jobs)
        _reply = "創建職業成功!"
    return _reply

def getMaxHp(job,level):
    level = int(level)
    if job == "warrior":
        return level*150
    elif job =="majic":
        return level*40
    elif job =="rog":
        return level*70

def getMaxExp(level):
    level = int(level)
    return 100*level*level
    