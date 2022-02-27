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
_maps = ["forest","subway"]
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
def checkstrMapLegal(map_command):
    _maps = ["forest"]
    if map_command in _maps:
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
        return level*100
    elif job =="rog":
        return level*70

def getMaxExp(level):
    level = int(level)
    return 100*level*level


def getMapInfo(command_map_name):
    print("冒險囉")
    print(dataBase.getMapInfp(command_map_name))


def goToMap(command_map_name,user_line_id):
    _replyjson={}
    if dataBase.UserIsInCombat(user_line_id):
        _replyjson["reply_text"] = "玩家正在戰鬥中"
        _replyjson["intobattle"] = False
        return _replyjson
    else:
        _mapinfo = dataBase.getMapInfo(command_map_name)
        _monster_list = _mapinfo["content_monster"]
        _which_monster = random.choices(_monster_list,weights=_mapinfo["monster_weight"])[0]
        #_which_monster = 1
        _monster = dataBase.getMonsterInfo(_which_monster)
        _user_status = dataBase.getUserJob(user_line_id)
        print("get monster:")
        print(_monster)
        print(_monster["monster_id"])
        print(_monster["hp"])
        dataBase.setUserbattleStatus(user_line_id,_monster["monster_id"],"player",_monster["hp"])
        _replyjson["reply_text"] = "進入戰鬥!"
        _replyjson["_monster"] = _monster
        _replyjson["intobattle"] = True
    
    return _replyjson

def getJobRollResult(_job):
    #戰士 -> 一顆骰子 結果 4-6
    #法師 ->　兩顆骰子　結果　1-4
    #盜賊 ->三顆骰子　結果1-4
    if _job == "warrior":
        return random.randrange(6,7)
    elif _job =="majic":
        return random.randrange(3,8)
    elif _job =="rog":
        return random.randrange(3,12)

def getJobAttackByjson(_user_job_json):
    _job = _user_job_json["job"]
    print(_job)
    if _job == "warrior":
        return _user_job_json["str"]*1.3
    elif _job =="majic":
        return _user_job_json["int"]*2
    elif _job =="rog":
        return _user_job_json["dex"]*1.5

def addPlayerExp(_user_job_json,_exp):
    _user_job_json["exp"]+=_exp
    _now_max_exp = getMaxExp(_user_job_json["level"])
    while _user_job_json["exp"] >= _now_max_exp:
        _user_job_json["exp"] -= _now_max_exp
        _user_job_json["level"]+=1
        if _user_job_json["job"] == "warrior":
            _user_job_json["str"]+=4
            _user_job_json["dex"]+=2
            _user_job_json["int"]+=1
        elif _user_job_json["job"] =="majic":
            _user_job_json["str"]+=1
            _user_job_json["dex"]+=2
            _user_job_json["int"]+=4
        else:
            _user_job_json["str"]+=2
            _user_job_json["dex"]+=3
            _user_job_json["int"]+=2
        _user_job_json["hp"] = getMaxHp(_user_job_json["job"], _user_job_json["level"])
        _now_max_exp = getMaxExp(_user_job_json["level"])
        
    return _user_job_json



def attackround(_user_line_id,_user_job_json,_target_monster_id,monster_hp):
    _playerjob = _user_job_json["job"]
    print("職業:"+_playerjob)
    baseAttack = getJobAttackByjson(_user_job_json)
    attackpow = getJobRollResult(_playerjob)
    _attack_result = int(baseAttack*attackpow)
    _monster_base_info = dataBase.getMonsterInfo(_target_monster_id)
    _monster_hp = monster_hp-_attack_result
    _monsterAttack = int(random.randrange(int(_monster_base_info["attack"]*0.7),int(_monster_base_info["attack"])))
    _playerhp = _user_job_json["hp"] - _monsterAttack
    _result={}
    print("怪物攻擊:"+str(_monsterAttack))
    print("玩家傷害:"+str(_attack_result)+" 怪物剩餘血量:"+str(_monster_hp))
    if dataBase.getUserRoundInfo(_user_line_id)["use_run_chance"] == True:
        dataBase.setUserRoundRunChance(_user_line_id,False)
    if _monster_hp > 0:
        #怪物沒有死亡 把怪物的攻擊結果一起帶回
        if _playerhp <= 0:
            #輸囉
            _result={"Result":"loose"}
            _user_job_json["hp"] = 0
            dataBase.ClearUserBattle(_user_line_id)
            dataBase.setUserJobStatus(_user_line_id,_user_job_json)
            print("die")
        else:
            #玩家沒死 怪物也沒死 
            #更新status
            _user_job_json["hp"] -= _monsterAttack
            dataBase.UpdateUserBattleStatus(_user_line_id,_target_monster_id,"player",_monster_hp)
            dataBase.setUserJobStatus(_user_line_id,_user_job_json)
            _monster_base_info["hp"] = _monster_hp
            _result={"Result":"monster_alive","dice_result":attackpow,"mosnter_damage":_monsterAttack,"player_damage":_attack_result,"monster_result_json":_monster_base_info,"player_result_json":_user_job_json}
    else:
        #掉落金錢 先隨機
        _money = random.randrange(500,2000)
        _originmoney = int(dataBase.getUserMoney(_user_line_id))+_money
        dataBase.SetUserMoneyByLineId(_user_line_id,_originmoney)
        dataBase.ClearUserBattle(_user_line_id)
        _origlevel = _user_job_json["level"]
        _user_job_json = addPlayerExp(_user_job_json,_monster_base_info["exp"])
        _islevelup = False
        if _user_job_json["level"] > _origlevel:
            _islevelup = True
        dataBase.setUserJobStatus(_user_line_id,_user_job_json)
        _result={"Result":"win","dice_result":attackpow,"player_damage":_attack_result,"monster_result_json":_monster_base_info,"player_result_json":_user_job_json,"is_level_up":_islevelup,"get_money":_money}

    return _result
    