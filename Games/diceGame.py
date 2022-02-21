import psycopg2
from psycopg2.extras import Json
import sys
import json
import random
import os
import time
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

def createGame(user_line_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    if checkUserIsHosting(user_line_id) is True:
        print("此玩家已有正在主持的遊戲!")
        conn.close()
        return "此玩家已有正在主持的遊戲!"
    else:
        nowTime = time.time()
        roomid = str(nowTime).split(".")[1]
        data = json.dumps([{"user_id":"以軒"}])
        sql ="""INSERT INTO dicegames (hoster, room_id,status) VALUES (%(hoster)s, %(room_id)s, %(status)s)"""
        params = {'hoster':user_line_id, 'room_id':roomid,'status':'OPEN',}
        cursor.execute(sql,params)
        # 事物提交
        conn.commit()
        conn.close()
        print("創建遊戲成功!")
        return "創建遊戲成功! 房號為:"+roomid


def getGame(room_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    sql = "SELECT * from dicegames WHERE room_id = '"+room_id+"'"
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    conn.close()
    room_info = result
    return room_info
    bet_info = room_info[3]
    for bet in bet_info:
        _json = json.loads(bet)
        for player_bet_info in _json:
            print(player_bet_info)
            print(player_bet_info['user_id'])


def getGameInfoStr(room_id):
    _room_info = getGame(str(room_id))
    _str="房間資訊:"+room_id+"\n"+"狀態"+_room_info[2]+"\n"
    print("待開獎房間:")
    print(_room_info)
    _bets_info = _room_info[3]
    _players = _bets_info.split("#")
    for _player in _players:
        print(_player)
        _player_info = json.loads(_player)
        profile = line_bot_api.get_profile(_player_info['user_id'])
        user_line_name = profile.display_name
        _str+="user:"+user_line_name+"\n"+"betinfo:\n"
        print("line id:"+_player_info['user_id'])
        print(_player_info['bet_info'])
        allbets = _player_info['bet_info'].split("&")
        for _bet in allbets:
            num = _bet.split(":")[0]
            price = _bet.split(":")[1]
            _str+="數字:"+str(num)+"壓住:"+str(price)+"\n"
            print("數字:"+str(num))
            print("壓住:"+str(price))
    return _str


def joinGame(user_line_id,bet_info,room_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    game_info = getGame(room_id)
    print(game_info)
    new = json.dumps({"user_id":user_line_id,"bet_info":bet_info})
    if game_info[3] is None:
        game_bet_info = new
    else:
        game_bet_info = game_info[3]
        print("append")
        print(game_bet_info)
        print(type(game_bet_info))
        game_bet_info = game_bet_info+"#"+new
    print(game_bet_info)
    sql ="""UPDATE dicegames SET bets_info = (%(bets)s) WHERE room_id = (%(room_id)s)"""
    params = {'bets':game_bet_info,'room_id':room_id}
    cursor.execute(sql,params)
    # 事物提交
    conn.commit()
    conn.close()
    print("加入遊戲成功!")
    return "加入遊戲成功!"

def checkUserIsHosting(user_line_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    sql = "SELECT * from dicegames WHERE hoster = '"+user_line_id+"'"
    cursor.execute(sql)
    conn.commit()
    row = cursor.fetchall()
    conn.close()
    if len(row) ==0 :
        return False
    else:
        return True

def checkGameIsExist(room_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT hoster from dicegames WHERE room_id = '"+room_id+"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return False
    else:
        return True
    

def StartGame(user_line_id):
    _reply =""
    if checkUserIsHosting(user_line_id) is False:
        print("此玩家無主持遊戲")
        _reply ="此玩家無主持遊戲"
        return _reply
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT room_id from dicegames WHERE hoster = '"+user_line_id+"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    row = cursor.fetchone()
    conn.close()
    _room_id = row[0]
    _room_id = str(_room_id)
    _room_info = getGame(_room_id)
    print("待開獎房間:")
    print(_room_info)
    _bets_info = _room_info[3]
    _dice_result = random.randint(1, 6)
    _dice_result = str(_dice_result)
    print("此輪結果為:"+str(_dice_result))
    _reply = "房間:"+_room_id+"\n此輪結果為:"+_dice_result+"\n"
    _players = _bets_info.split("#")
    for _player in _players:
        print(_player)
        _player_info = json.loads(_player)
        print("line id:"+_player_info['user_id'])
        print(_player_info['bet_info'])
        profile = line_bot_api.get_profile(_player_info['user_id'])
        user_line_name = profile.display_name
        _reply+="玩家: "+user_line_name+"\n"+"下注結果:\n"
        allbets = _player_info['bet_info'].split("&")
        for _bet in allbets:
            num = _bet.split(":")[0]
            price = _bet.split(":")[1]
            print("數字:"+str(num))
            print("壓住:"+str(price))
            _reply+="數字:"+str(num)+" 壓住:"+str(price)
            if str(num) == str(_dice_result):
                print("成功! 獲得金錢")
                _reply+="成功! 獲得金錢"
            else:
                print("猜測失敗")
                _reply+="猜測失敗"
            _reply+="\n"
        _reply+="\n"
    clearGame(user_line_id)
    return _reply

    
def clearGame(user_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    sql ="""DELETE FROM dicegames WHERE hoster = (%(hoster)s)"""
    params = {'hoster':user_id}
    cursor.execute(sql,params)
    # 事物提交
    conn.commit()
    conn.close()
    print("done clear game with:"+user_id)



if __name__ == "__main__":
    #print(checkUserIsHosting("1"))
    #createGame("2")
    #print(checkUserIsHosting("1"))
    #createGame("shane1")
    #joinGame("shane","6:200","-3")
    #StartGame("shane1")
    #joinGame("shane","1:1","0")
    clearGame("U8d0f4dfe21ccb2f1dccd5c80d5bb20fe")

