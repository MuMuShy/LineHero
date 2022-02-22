import psycopg2
from psycopg2.extras import Json
import sys
import json
import random
import os
import time
import math
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

def createGame(user_line_id,group_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    if checkUserIsHosting(user_line_id) is True:
        print("此玩家已有正在主持的遊戲!")
        conn.close()
        return "此玩家已有正在主持的遊戲!"
    else:
        nowTime = time.time()
        roomid = str(nowTime).split(".")[1]
        if group_id == " ":
            print("斯療 沒有group")
            sql ="""INSERT INTO dicegames (hoster, room_id,status) VALUES (%(hoster)s, %(room_id)s, %(status)s)"""
            params = {'hoster':user_line_id, 'room_id':roomid,'status':'OPEN'}
        else:
            sql ="""INSERT INTO dicegames (hoster, room_id,status,group_id) VALUES (%(hoster)s, %(room_id)s, %(status)s,%(groupid)s)"""
            params = {'hoster':user_line_id, 'room_id':roomid,'status':'OPEN','groupid':group_id}
        cursor.execute(sql,params)
        # 事物提交
        conn.commit()
        conn.close()
        print("創建遊戲成功!")
        return "創建遊戲成功! 房號為:"+roomid+"\n此遊戲為單顆骰 賠率為:\n大中小:*2.6\n指定數字:*5.2\n單雙:*1.9\n請使用 !join 房號 壓注 進行下注\n!!如果在群組中!!\n可以直接使用 !j 下注資料 不用輸入房號\n壓注請用' : '把骰子號碼跟金額分開 使用' & '區隔多筆下注\n Ex(!join xxx 1:200&3:300&單:900&大:500)"


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

def getRoomList():
    _str=""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT * from dicegames"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    for room in result:
        print("房主:")
        user_id = str(room[0])
        _str+="房主: "+dataBase.getUserName(user_id)+"房間編號"+str(room[1])+"\n"
        print(dataBase.getUserName(str(room[0])))
        print("房間編號:")
        print(str(room[1]))
    _str+="使用 !join 房間編號 骰子號碼:金額&骰子號碼2:金額\nEx: !join 666 1:100&2:300&3:300\n\n"
    return _str


def checkGroupHasGame(group_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT * from dicegames where group_id  = '"+group_id+"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print(len(result))
    conn.commit()
    conn.close()
    if len(result) == 0:
        print("沒有進行中遊戲")
        return False
    else:
        print("有進行中遊戲")
        print(result)
        print(len(result))
        print(type(result))
        print(dataBase.getUserName(result[0][0]))
        print(result[0][1])
        return True

def getGroupPlayingGame(group_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT * from dicegames where group_id  = '"+group_id+"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print(len(result))
    _hoster = dataBase.getUserName(result[0][0])
    _room_id = result[0][1]
    room_json={"room_hoster":_hoster,"room_id":_room_id}
    conn.commit()
    conn.close()
    return room_json
      
    

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
        _str+="玩家:"+user_line_name+"\n"+"下注資料\n"
        print("line id:"+_player_info['user_id'])
        print(_player_info['bet_info'])
        allbets = _player_info['bet_info'].split("&")
        for _bet in allbets:
            num = _bet.split(":")[0]
            price = _bet.split(":")[1]
            _str+="數字:"+str(num)+"壓注:$"+str(price)+"\n"
            print("數字:"+str(num))
            print("壓住:"+str(price))
    return _str


def joinGame(user_line_id,bet_info,room_id,total_bet):
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
    _money = checkPlayerMoney(user_line_id)
    _money-=total_bet
    sql ="""UPDATE users SET user_money = (%(money)s) WHERE user_line_id = (%(line_id)s)"""
    params = {'money':_money,'line_id':user_line_id}
    cursor.execute(sql,params)
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
    
    _room_id = row[0]
    _room_id = str(_room_id)
    _room_info = getGame(_room_id)
    print("待開獎房間:")
    print(_room_info)
    _bets_info = _room_info[3]
    _dice_result = random.randint(1, 6)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT room_id from dicegames WHERE hoster = '"+user_line_id+"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    _dice_result = str(_dice_result)
    print("此輪結果為:"+str(_dice_result))
    _reply = "房間:"+_room_id+"\n此輪結果為:"+_dice_result+"\n"
    try:
        _players = _bets_info.split("#")
    except:
        return "此局的下注資料好像有問題(有可能是沒有玩家) 請利用join加入此遊戲 房號: "+_room_id
    for _player in _players:
        print(_player)
        _player_info = json.loads(_player)
        print("line id:"+_player_info['user_id'])
        print(_player_info['bet_info'])
        profile = line_bot_api.get_profile(_player_info['user_id'])
        _player_id = _player_info['user_id']
        user_line_name = profile.display_name
        _reply+="玩家: "+user_line_name+"\n"+"下注結果:\n"
        allbets = _player_info['bet_info'].split("&")
        _tempmoney = checkPlayerMoney(_player_id)
        for _bet in allbets:
            num = _bet.split(":")[0]
            price = _bet.split(":")[1]
            print("數字:"+str(num))
            print("壓住:"+str(price))
            _reply+="數字:"+str(num)+" 壓 :"+str(price)
            #純數字
            if str(num).isdigit():
                if str(num) == str(_dice_result):
                    _payoff = math.ceil(int(price)*5.2)
                    _tempmoney+=_payoff
                    print("成功! 獲得金錢")
                    _reply+="成功! 獲得金錢 : "+str(_payoff)
                else:
                    print("猜測失敗")
                    _reply+="猜測失敗"
            #大中小 單雙
            else:
                choice = str(num)
                if choice =="大":
                    if int(_dice_result) ==5 or int(_dice_result) ==6:
                        _payoff = math.ceil(int(price)*2.6)
                        _tempmoney+=_payoff
                        print("成功! 獲得金錢")
                        _reply+="成功! 獲得金錢 : "+str(_payoff)
                    else:
                        print("猜測失敗")
                        _reply+="猜測失敗"
                elif choice =="中":
                    if int(_dice_result) ==3 or int(_dice_result) ==4:
                        _payoff = math.ceil(int(price)*2.6)
                        _tempmoney+=_payoff
                        print("成功! 獲得金錢")
                        _reply+="成功! 獲得金錢 : "+str(_payoff)
                    else:
                        print("猜測失敗")
                        _reply+="猜測失敗"
                elif choice =="小":
                    if int(_dice_result) ==1 or int(_dice_result) ==2:
                        _payoff = math.ceil(int(price)*2.6)
                        _tempmoney+=_payoff
                        print("成功! 獲得金錢")
                        _reply+="成功! 獲得金錢 : "+str(_payoff)
                    else:
                        print("猜測失敗")
                        _reply+="猜測失敗"
                elif choice =="單":
                    if int(_dice_result)%2 !=0:
                        _payoff = math.ceil(int(price)*1.9)
                        _tempmoney+=_payoff
                        print("成功! 獲得金錢")
                        _reply+="成功! 獲得金錢 : "+str(_payoff)
                    else:
                        print("猜測失敗")
                        _reply+="猜測失敗"
                elif choice =="雙":
                    if int(_dice_result)%2 ==0:
                        _payoff = math.ceil(int(price)*1.9)
                        _tempmoney+=_payoff
                        print("成功! 獲得金錢")
                        _reply+="成功! 獲得金錢 : "+str(_payoff)
                    else:
                        print("猜測失敗")
                        _reply+="猜測失敗"
            _reply+="\n"
        _reply+="\n"
        sql ="""UPDATE users SET user_money = (%(money)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'money':_tempmoney,'line_id':_player_id}
        cursor.execute(sql,params)
        conn.commit()
    conn.close()
    clearGame(user_line_id)
    print(_reply)
    _reply=str(_dice_result)+"|"+_reply
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


def checkPlayerMoney(user_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    sql = "SELECT user_money from users WHERE user_line_id = '"+user_id+"'"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    row = cursor.fetchone()
    conn.close()
    return row[0]



if __name__ == "__main__":
    #print(checkUserIsHosting("1"))
    #createGame("2")
    #print(checkUserIsHosting("1"))
    #createGame("shane1")
    #joinGame("shane","6:200","-3")
    #StartGame("shane1")
    #joinGame("shane","1:1","0")
    checkPlayerMoney('U8d0f4dfe21ccb2f1dccd5c80d5bb20fe')

