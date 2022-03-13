from cgitb import reset
import os
from pydoc import describe
import random
from unittest import result
import psycopg2
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
from Games import rpgDictionary
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']


class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    def checkUser(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM users where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            return True
        else:
            return False
    
    def createUser(self,user_line_id,user_line_name,user_img_link):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""INSERT INTO users (user_line_name, user_line_id,user_img,user_money,locked_money) VALUES (%(user_line_name)s, %(user_line_id)s, %(user_img)s, %(user_money)s,%(locked_money)s)"""
        params = {'user_line_name':user_line_name, 'user_line_id':user_line_id,'user_img':user_img_link,'user_money':100000,'locked_money':0}
        self.cursor.execute(sql,params)
        self.conn.commit()
    

    def getUser(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        json={"user_line_name":"","user_img_link":"","user_money":123}
        if row is not None:
            json["user_line_name"] = row[0]
            json["user_info_id"] = row[2]
            json["user_img_link"] = row[3]
            json["user_money"] = str(row[4])
            json["locked_money"] = str(row[5])
            json["user_type"] = str(row[8])
            return json
    
    def getUserById(self,user_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT user_line_id from users WHERE user_id = '"+str(user_id)+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        json={}
        if row is not None:
            id = row[0]
            return id

    
    def getUserMoney(self,user_line_id):
        return self.getUser(user_line_id)["user_money"]
    
    def getUserName(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return row[0]

    def getCommandList(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM commands"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        commandlist = {}
        if row is not None:
            for item in row:
                commandlist[item[0]]=[item[1]]
        return commandlist
    
    def getUserRank(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * from users order by user_money DESC"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        commandlist = {}
        rank = 1
        if row is not None:
            for item in row:
                if item[1] == user_line_id:
                    return rank
                rank+=1
        return rank
    
    def getUserRpgRank(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * from users_job order by level DESC"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        rank = 1
        if row is not None:
            for item in row:
                if item[0] == user_line_id:
                    return rank
                rank+=1
        return rank

    def SetUserMoneyByIndex(self,user_index_id,money):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET user_money = """+str(money)+"""WHERE user_id = """+str(user_index_id)
        self.cursor.execute(sql)
        self.conn.commit()


    def SetUserMoneyByLineId(self,user_line_id,money):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET user_money = (%(money)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'money':money,'line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def AddUserMoneyByLineId(self,user_lind_id,money):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET user_money = user_money+(%(money)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'money':money,'line_id':user_lind_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
        print("增加:"+user_lind_id+"金錢:"+str(money))
    
    def SetUserLockedMoneyByLineId(self,user_line_id,money):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET locked_money = (%(money)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'money':money,'line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def GetUserLockedMoneyLineId(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT locked_money from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return row[0]
    

    def getTop5Ranking(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="Select user_line_name, user_money from users ORDER BY user_money desc"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchmany(5)
        result=[]
        for col in row:
            _reply =str(col[0])+" : $"+str(col[1])
            print(col[0])
            print(col[1])
            result.append(_reply)
        return result
    
    def getTop5RpgRanking(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="Select * from users_job ORDER BY level desc"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchmany(5)
        result=[]
        for col in row:
            _name = self.getUserName(col[0])
            _money = int(self.getUserMoney(col[0]))
            _money = str("{:,}".format(_money))
            _parser = {"warrior":"戰士","majic":"法師","rog":"盜賊"}
            _job = _parser[col[1]]
            _reply =str(_name)+" : LV"+str(col[5])+_job+" $: "+str(_money)
            result.append(_reply)
        return result
    
    def getHobbyBet(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM users where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return int(row[6])

    def setHobbyBet(self,user_line_id,new_hobbybet):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE users SET hobby_bet = %s WHERE user_line_id = %s"""
        data = (new_hobbybet, user_line_id)
        self.cursor.execute(sql,data)
        self.conn.commit()


    def getDiceHistory(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """SELECT dice_history from gameinfo"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _historystr = row[0]
        _parse = list(_historystr)
        print(_parse)
        return _historystr

    def setDiceHistory(self,new):
        old = self.getDiceHistory()
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        _new =str(str(old)+new)
        lis = list(_new)
        if len(lis) > 10:
            print("太長了 把第一個砍掉")
            lis.pop(0)
        _strtodb = ''.join(lis)
        sql = """UPDATE gameinfo SET dice_history = """+_strtodb
        self.cursor.execute(sql)
        self.conn.commit()
    
    def getWatherMoney(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """select wather_money from gameinfo"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _wathermoney = row[0]
        print("目前水錢")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    def setWatherMoney(self,new):
        print("目前水錢"+str(new))
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE gameinfo SET wather_money = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def addWatherMoney(self,add):
        now_wather_money = self.getWatherMoney()
        if add < 0:
            new_wather_money = now_wather_money-int(add)
        else:
            new_wather_money = int(add)+now_wather_money
        self.setWatherMoney(new_wather_money)
        print("目前水錢:"+str(new_wather_money))
    
    def getGrand(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """select grand from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _wathermoney = row[0]
        print("目前Grand:")
        print(int(_wathermoney))
        return int(_wathermoney)

    def getMajor(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """select major from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _wathermoney = row[0]
        print("目前Major:")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    def getMinor(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """select minor from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _wathermoney = row[0]
        print("目前Minor:")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    def getMini(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """select mini from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _wathermoney = row[0]
        print("目前Mini:")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    
    def setGrand(self,new):
        print("設定jackpot Grand"+str(new))
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET grand = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def setMajor(self,new):
        print("設定jackpot Major"+str(new))
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET major = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def setMinor(self,new):
        print("設定jackpot Minor"+str(new))
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET minor = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def setMini(self,new):
        print("設定jackpot Mini"+str(new))
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET mini = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def getAllJackpot(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """select * from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        print("GRAND:"+str(row[0])+" MAJOR:"+str(row[1])+" MINOR:"+str(row[2])+" MINI:"+str(row[3])+" LASTWIN:"+str(row[4])+" LASTWINprice:"+str(row[5]))
        return row
    
    def setAllJackpot(self,grand,major,minor,mini):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET grand = %s , major = %s , minor = %s , mini = %s """
        data = (grand, major,minor,mini)
        self.cursor.execute(sql,data)
        self.conn.commit()
        print("更新jp:"+str(grand)+","+str(major)+","+str(minor)+","+str(mini))
    
    def setJpLastWin(self,_winnername,_winmoney):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET last_winner = %s , last_winprice = %s"""
        data = (_winnername, _winmoney)
        self.cursor.execute(sql,data)
        self.conn.commit()
        print("更新jp中獎者:"+str(_winnername)+":"+str(_winmoney))
    
    def addAllJp(self,grand,major,minor,mini):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET grand = grand+ %s , major = major+ %s , minor = minor+%s , mini = mini+ %s """
        data = (grand, major,minor,mini)
        self.cursor.execute(sql,data)
        self.conn.commit()
        print("增加jp:"+str(grand)+","+str(major)+","+str(minor)+","+str(mini))
    
    


    def checkUserDaily(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT daily_request_done FROM users where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return bool(row[0])
    
    def checkDailyBroadcast(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT broadcast from daily_broadcast"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return row[0]
    
    def setUserDaily(self,user_line_id,bool):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        if bool == True:
            bool = "true"
        else:
            bool ="false"
        sql = "UPDATE users SET daily_request_done = %s where user_line_id = %s"
        data = (bool, user_line_id)
        self.cursor.execute(sql,data)
        self.conn.commit()
    
    def setAllUserDaily(self,bool):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        if bool == True:
            bool = "true"
        else:
            bool ="false"
        sql = "UPDATE users SET daily_request_done = %s"
        data = (bool)
        self.cursor.execute(sql,data)
        self.conn.commit()
    
    def checkUserHasJob(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM users_job where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            return True
        else:
            return False
    
    #初始
    def createUserJob(self,user_line_id,jobs):
        from Games import rpgGame
        maxhp = rpgGame.getMaxHp(jobs,1)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        _pet = 2
        if jobs =="rog":
            _pet = 1
        elif jobs =="majic":
            _pet = 3

        if jobs == 'warrior':
            hassame,loc = self.checkUserPackMaxLoc(user_line_id,"weapon",1)
            self.addToUserBackPack(user_line_id,"weapon",1,1,hassame,loc)
            self.addToUserWeapon(user_line_id,1,loc,0,0,0,0)
            self.addSkillToUser(user_line_id,0,"warrior",1,0)
            self.addSkillToUser(user_line_id,1,"warrior",1,0)
        elif jobs == 'rog':
            hassame,loc = self.checkUserPackMaxLoc(user_line_id,"weapon",2)
            self.addToUserBackPack(user_line_id,"weapon",2,1,hassame,loc)
            self.addToUserWeapon(user_line_id,2,loc,0,0,0,0)
            self.addSkillToUser(user_line_id,0,"rog",1,0)
            self.addSkillToUser(user_line_id,1,"rog",1,0)
        else:
            hassame,loc = self.checkUserPackMaxLoc(user_line_id,"weapon",3)
            self.addToUserBackPack(user_line_id,"weapon",3,1,hassame,loc)
            self.addToUserWeapon(user_line_id,3,loc,0,0,0,0)
            self.addSkillToUser(user_line_id,0,"majic",1,0)
            self.addSkillToUser(user_line_id,1,"majic",1,0)


        sql ="""INSERT INTO users_job (user_line_id, jobs, str, dex, intelligence, level, hp, exp, equipment_weapon,equipment_pet) VALUES (%(user_line_id)s, %(jobs)s,10,10,10,1,%(maxhp)s,0,%(weapon)s,%(pet)s)"""
        params = {'user_line_id':user_line_id, 'jobs':jobs,'maxhp':maxhp,'weapon':loc,'pet':_pet}
        self.cursor.execute(sql,params)
        self.conn.commit()
        
    
    def getUserJob(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM users_job where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _json = {}
        _json={"job":row[1],"str":row[2],"dex":row[3],"int":row[4],"level":row[5],"hp":row[6],"exp":row[7],"weapon":row[8],"pet":row[9],"skill_point":row[10],"word":row[11]}
        print("玩家職業資料")
        print(_json)
        return _json
    
    def getPetInfo(self,pet_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM pets_list where pet_id = '" +str(pet_id)+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        print(row)
        _json = {}
        _other_effect={}
        for _line in row[3]:
            _type = _line.split(":")[0]
            _value = _line.split(":")[1]
            _other_effect[_type] = _value
        _json={"pet_id":row[0],"rare":row[2],"pet_name":row[1],"img_type":row[4],"other_effect":_other_effect}
        print(_json)
        return _json
    
    def getWeaponInfo(self,weapon_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """SELECT * FROM weapon_list where weapon_id = %s"""
        self.cursor.execute(sql,(weapon_id,))
        self.conn.commit()
        row = self.cursor.fetchone()
        print(row)
        _json = {}
        _weapon_other_effect={}
        # print(row[8])
        # print(type(row[8]))
        for _line in row[8]:
            _type = _line.split(":")[0]
            _value = _line.split(":")[1]
            _weapon_other_effect[_type] = _value
        _json={"weapon_id":row[0],"str_add":row[1],"int_add":row[2],"dex_add":row[3],"atk_add":row[4],"rare":row[5],"weapon_name":row[6],"img_type":row[7],"other_effect":_weapon_other_effect}
        print(_json)
        return _json        

    def addExpForPlayer(self,user_line_id,exp):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "UPDATE users_job SET exp = exp+{exp} where user_line_id = '{user_line_id}'".format(exp=exp,user_line_id=user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def setUserJobStatus(self,user_line_id,user_job_json):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE users_job SET str = %s , dex = %s ,intelligence = %s , hp = %s,level = %s,exp = %s,skill_point = %s,word=%s Where user_line_id = %s"""
        data = (user_job_json["str"], user_job_json["dex"],user_job_json["int"],user_job_json["hp"],user_job_json["level"],user_job_json["exp"],user_job_json["skill_point"],user_job_json["word"],user_line_id)
        self.cursor.execute(sql,data)
        self.conn.commit()
        print("更新使用者狀態:")
        print(user_job_json)
    
    def joinUserWord(self,user_line_id,word,money_give=0,exp_give=0):
        word = "word"+str(word)+"_users_status"
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="INSERT INTO {word} (user_line_id, money_give,exp_give) VALUES ('{user_line_id}',{money_give},{exp_give})".format(word=word,user_line_id=user_line_id,money_give=money_give,exp_give=exp_give)
        self.cursor.execute(sql)
        self.conn.commit()

    def updateUserWordStatus(self,user_line_id,word,money_give=0,exp_give=0):
        word = "word"+str(word)+"_users_status"
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="UPDATE {word} SET money_give = {money_give},exp_give={exp_give} where user_line_id = '{user_line_id}'".format(word=word,user_line_id=user_line_id,money_give=money_give,exp_give=exp_give)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def addUserWordStatus(self,user_line_id,word,money_give=0,exp_give=0):
        word = "word"+str(word)+"_users_status"
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="UPDATE {word} SET money_give = money_give+{money_give},exp_give = exp_give+{exp_give} where user_line_id = '{user_line_id}'".format(word=word,user_line_id=user_line_id,money_give=money_give,exp_give=exp_give)
        self.cursor.execute(sql)
        self.conn.commit()

    
    def updateWordStatus(self,word_id,word_level,word_exp,word_money):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "UPDATE word_list SET word_level = {word_level}, word_exp = {word_exp} ,word_money = {word_money} Where word_id = {word_id}".format(word_level=word_level,word_exp=word_exp,word_money=word_money,word_id=word_id)
        data = (word_level, word_exp,word_money,word_id)
        self.cursor.execute(sql,data)
        self.conn.commit()
    
    def addWordMoneyExp(self,word_id,word_exp,word_money):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "UPDATE word_list SET word_exp = word_exp+{word_exp} ,word_money = word_money+{word_money} Where word_id = {word_id}".format(word_exp=word_exp,word_money=word_money,word_id=word_id)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def getWordStatus(self,word_id):
        word_id = int(word_id)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT word_name,word_god,word_level,word_exp,word_money FROM word_list WHERE word_id = {word_id}".format(word_id=word_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        json = {"word_name":result[0],"word_god":result[1],"word_level":result[2],"word_exp":result[3],"word_money":result[4],"word_id":word_id}
        print(json)
        self.conn.commit()
        return json
    
    def getUserWordStatus(self,user_line_id,word):
        word = "word"+str(word)+"_users_status"
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT user_line_id,money_give,exp_give FROM {word} WHERE user_line_id = '{user_line_id}'".format(word=word,user_line_id=user_line_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        json = {"user_line_id":result[0],"money_give":result[1],"exp_give":result[2]}
        print(json)
        self.conn.commit()
        return json
    
    def getWordRank1(self,word):
        word = "word"+str(word)+"_users_status"
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM {word} order by money_give desc".format(word=word)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[0]
        self.conn.commit()
        if result is not None:
            return result
        else:
            return None
        


    def setUserMaxHp(self,user_line_id,hp):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE users_job SET hp = %s Where user_line_id = %s"""
        data = (hp,user_line_id)
        self.cursor.execute(sql,data)
        self.conn.commit()
        print("補滿血:")

    
    def getMapInfo(self,map_command_name):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM maps where map_command_name = '" +map_command_name+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _json = {}
        _json={"map_id":row[0],"content_monster":row[1],"map_name":row[2],"monster_weight":row[4]}
        print(_json)
        return _json
    
    def getAdventureMapInfo(self,map_command_name):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM adventure_map_list where map_command_name = '" +map_command_name+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _json = {}
        _json={"map_id":row[0],"exp_min":row[1],"money_min":row[2],"map_name":row[3],"map_command_name":row[4]}
        print(_json)
        return _json
    
    def getAdventureMapInfoById(self,map_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM adventure_map_list where adventure_map_id = '" +str(map_id)+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _json = {}
        _json={"map_id":row[0],"exp_min":row[1],"money_min":row[2],"map_name":row[3],"map_command_name":row[4]}
        print(_json)
        return _json
    
    def UserIsInCombat(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM battle_status_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            return True
        else:
            return False
    
    def UserIsInAdventure(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM users_adventure_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            return True
        else:
            return False
    
    def ClearUserBattle(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="DELETE FROM battle_status_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        # 事物提交
        self.conn.commit()
        print("清空戰鬥:"+user_line_id)
    
    def getMonsterInfo(self,monster_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT * FROM monsters where monster_id = '"+str(monster_id)+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        print("怪物基礎資料:")
        print(row)
        # 事物提交
        _json = {}
        _json={"monster_id":row[0],"monster_name":row[4],"attack":row[1],"speed":row[2],"exp":row[3],"defend":row[5],"hp":row[6],"description":row[7],"image_type":row[8],"drop_item":row[9]}
        return _json
    
    def setUserbattleStatus(self,user_line_id,monster_id,now_turn,monster_hp):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""INSERT INTO battle_status_list (user_line_id, target_monster_id,now_turn,monster_hp) VALUES (%(user_line_id)s, %(target_monster_id)s, %(now_turn)s, %(monster_hp)s)"""
        params = {'user_line_id':user_line_id, 'target_monster_id':monster_id,'now_turn':now_turn,'monster_hp':monster_hp,}
        self.cursor.execute(sql,params)
        self.conn.commit()
        print("進入對戰列表:"+user_line_id)
    
    def setUserAdventureStatus(self,user_line_id,map_id):
        current =  datetime.now()
        str_todatabase = (current.strftime("%m/%d/%Y %H:%M:%S"))
        _user_pet = self.getUserJob(user_line_id)["pet"]
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""INSERT INTO users_adventure_list (user_line_id, adventure_map_id,pet_id,start_time) VALUES (%(user_line_id)s, %(adventure_map_id)s, %(pet_id)s, %(start_time)s)"""
        params = {'user_line_id':user_line_id, 'adventure_map_id':map_id,'pet_id':_user_pet,'start_time':str_todatabase,}
        self.cursor.execute(sql,params)
        self.conn.commit()
        print("進入探險隊列表:"+user_line_id)
    
    def getUserAdventureStatus(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT * FROM users_adventure_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        print(row)
        _json ={"user_line_id":row[0],"map_id":row[1],"pet_id":row[2],"start_time":row[3]}
        return _json
    
    def ClearUserAdventureStatus(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="DELETE FROM users_adventure_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        # 事物提交
        self.conn.commit()
        print("清空探險隊:"+user_line_id)
    
    def UpdateUserBattleStatus(self,user_line_id,monster_id,now_turn,monster_hp):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE battle_status_list SET target_monster_id = (%(target_monster_id)s),monster_hp =(%(monster_hp)s)  WHERE user_line_id = (%(line_id)s)"""
        params = {'line_id':user_line_id, 'target_monster_id':monster_id,'monster_hp':monster_hp,}
        self.cursor.execute(sql,params)
        self.conn.commit()
        print("更新對戰列表:"+user_line_id)
    
    def getUserRoundInfo(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT * FROM battle_status_list where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        print(row)
        _json ={"user_line_id":row[0],"target_monster_id":row[1],"now_turn":row[2],"monster_hp":row[3],"use_run_chance":row[4]}
        return _json
    
    def setUserRoundRunChance(self,user_line_id,bool):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE battle_status_list SET use_run_chance = (%(use_run_chance)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'line_id':user_line_id, 'use_run_chance':bool}
        self.cursor.execute(sql,params)
        self.conn.commit()
        print("更新對戰逃跑列表:"+user_line_id)
    
    def clearDailyRequest(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET daily_request_done = false"""
        self.cursor.execute(sql)
        self.conn.commit()
        print("0.00 DAILY CLEAR REQUEST DONE")
    
    def checkUserPackMaxLoc(self,user_line_id,item_type,item_id):###有修改###
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""select max(backpack_loc) from user_backpack where user_line_id =(%(line_id)s) """
        params = {'line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
        row = self.cursor.fetchone()
        num = row[0]
        print("目前玩家背包序列index到達:"+str(num))
        if item_type == 'weapon':
            if num == None:
                return False,0
            else:
                return False,num+1
        else:
            print("item id:")
            print(item_id)
            sql ="""select max(backpack_loc) from user_backpack where user_line_id = '{line_id}' and item_type = '{item_type}' and item_id = {item_id} """.format(line_id = user_line_id,item_type=item_type,item_id=item_id)
            self.cursor.execute(sql)
            self.conn.commit()
            row = self.cursor.fetchone()[0]
            if row == None:
                if num == None:
                    return False,0
                else:
                    return False,num+1
            else:
                return True,row
    
    def addToUserBackPack(self,user_line_id,item_type,item_id,quantity,IS_EXIST,loc=-1):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        if IS_EXIST == False:
            if loc ==-1:
                hassame,_nowpackindex = self.checkUserPackMaxLoc(user_line_id,item_type,item_id)
            else:
                _nowpackindex = loc
            sql ="""INSERT INTO user_backpack (user_line_id, backpack_loc,item_type,item_id,quantity) VALUES (%(user_line_id)s, %(backpack_loc)s, %(item_type)s, %(item_id)s,%(quantity)s)"""
            params = {'user_line_id':user_line_id,'backpack_loc':_nowpackindex,'item_type':item_type,'item_id':item_id,'quantity':quantity}
            self.cursor.execute(sql,params)
            self.conn.commit()
        else:
            sql ="""SELECT quantity FROM user_backpack WHERE user_line_id = '{user_line_id}' and item_type = '{item_type}' and item_id = {item_id}""".format(user_line_id=user_line_id,item_type=item_type,item_id=item_id)
            self.cursor.execute(sql)
            self.conn.commit()
            row_quantity = self.cursor.fetchone()[0]
            sql = """UPDATE user_backpack SET quantity={quantity} WHERE user_line_id = '{user_line_id}' and item_type = '{item_type}' and item_id = {item_id}""".format(quantity=quantity+row_quantity,user_line_id=user_line_id,item_type=item_type,item_id=item_id)
            self.cursor.execute(sql)
            self.conn.commit()
    
    #會移除玩家背包某個位置的東西 如果是武器會再幫她清除user_Weapon
    def removeUserBackPack(self,user_line_id,backpack_loc,quantity = 1):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT item_type,item_id,quantity FROM user_backpack where user_line_id = '{user_line_id}' and backpack_loc = {backpack_loc}".format(user_line_id = user_line_id,backpack_loc = backpack_loc)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()
        self.conn.commit()
        if _result is None:
            print("玩家此格背包沒有東西")
            return
        else:
            itemtype = _result[0]
            itemid = _result[1]
            quantity = _result[2]
            print("準備移除:"+itemtype+"物品位置:"+str(backpack_loc)+" 物品編號:"+str(itemid)+" 數量:"+str(quantity))
            #武器因為沒有堆疊 還有user_Weapon表需要去刪除
            if itemtype == "weapon":
                self.removeUserWeapon(user_line_id,backpack_loc)
                self.removeFromUserBackPack(user_line_id,backpack_loc)
            else:
                self.removeUsefulItemFromPack(user_line_id,backpack_loc,quantity)
    
    def removeFromUserBackPack(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""DELETE FROM user_backpack where user_line_id = %s and backpack_loc = %s """
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        self.conn.commit()
    
    #確定某格欄位有多少個物品
    def checkItemNumFromLoc(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """SELECT quantity FROM user_backpack WHERE user_line_id = %s and backpack_loc = %s"""
        self.cursor.execute(sql,(user_line_id,backpack_loc,))
        try:
            num = int(self.cursor.fetchone()[0])
        except:
            num = -999
        self.conn.commit()
        return num
    
    #消耗品會在同一格 所以要修改他的quantity
    def removeUsefulItemFromPack(self,user_line_id,backpack_loc,quantity):
        _numorigin = self.checkItemNumFromLoc(user_line_id,backpack_loc)
        #消耗品同種類還有庫存 只要修改他的quantity
        if _numorigin - quantity > 0:
            _finalquantity = _numorigin - quantity
            sql = """UPDATE user_backpack SET quantity = %s WHERE user_line_id = %s and backpack_loc = %s"""
            self.cursor.execute(sql,(_finalquantity,user_line_id,backpack_loc,))
            self.conn.commit()
        else:
            print("這個物品用光了 把她拔掉")
            sql = """DELETE from user_backpack WHERE user_line_id = %s and backpack_loc = %s"""
            self.cursor.execute(sql,(user_line_id,backpack_loc,))
            self.conn.commit()

    
    def getItemFromUserBackPack(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """SELECT * FROM user_backpack where user_line_id = %s and backpack_loc = %s"""
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        _result = self.cursor.fetchone()
        self.conn.commit()
        if _result == None or len(_result) ==0:
            return None
        else:
            print("result 在這")
            print(_result)
            _json ={"user_line_id":_result[0],"backpack_loc":_result[1],"item_type":_result[2],"item_id":_result[3],"quantity":_result[4]}
            return _json
    

    
    
    def addToUserWeapon(self,user_line_id,weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        #empty='{}'
        sql ="""INSERT INTO user_weapon (user_line_id, weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add) VALUES (%(user_line_id)s, %(weapon_id)s, %(backpack_loc)s, %(str_add)s, %(int_add)s,%(dex_add)s,%(atk_add)s)"""
        params = {'user_line_id':user_line_id,'weapon_id':weapon_id,'backpack_loc':backpack_loc,'str_add':str_add,'int_add':int_add,'dex_add':dex_add,'atk_add':atk_add}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def addToUserWeaponWithEnhanced(self,user_line_id,weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add,uses_reel,available_reeltime,description,success_time):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        #empty='{}'
        if description == [] or len(description) == 0 or description is None:
            description = '{}'
        sql ="""INSERT INTO user_weapon (user_line_id, weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add,uses_reel,available_reeltime,description,success_time) VALUES (%(user_line_id)s, %(weapon_id)s, %(backpack_loc)s, %(str_add)s, %(int_add)s,%(dex_add)s,%(atk_add)s,%(uses_reel)s,%(available_reeltime)s,%(description)s,%(success_time)s)"""
        params = {'user_line_id':user_line_id,'weapon_id':weapon_id,'backpack_loc':backpack_loc,'str_add':str_add,'int_add':int_add,'dex_add':dex_add,'atk_add':atk_add,
        'uses_reel':uses_reel,'available_reeltime':available_reeltime,'description':description,'success_time':success_time}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def getValueFromUserWeapon(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        print("back pac loc:"+str(backpack_loc))
        sql = """SELECT user_line_id,weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add,uses_reel,available_reeltime,success_time,description FROM user_weapon where user_line_id = %s and backpack_loc = %s"""
        self.cursor.execute(sql,(user_line_id,backpack_loc,))
        _result = self.cursor.fetchone()
        self.conn.commit()
        print("武器加乘東西在這")
        print(_result)
        if _result[10] == ['None']:
            _otherdescription = None
        else:
            _otherdescription = _result[10]
        _json ={"user_line_id":_result[0],"weapon_id":_result[1],"backpack_loc":_result[2],"str_add":_result[3],"int_add":_result[4],"dex_add":_result[5],"atk_add":_result[6],"uses_reel":_result[7],"available_reeltime":_result[8],"success_time":_result[9],"description":_otherdescription}
        return _json

    def removeUserWeapon(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""DELETE FROM user_weapon where user_line_id = %s and backpack_loc = %s """
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        self.conn.commit()

    #gm 用
    def givePlayerItem(self,user_lind_id,item_type,item_id,quantity=1):
        hassame,loc = self.checkUserPackMaxLoc(user_lind_id,item_type,item_id)    
        if item_type == "weapon":
            quantity = 1
            self.addToUserWeapon(user_lind_id,item_id,loc,0,0,0,0)
        self.addToUserBackPack(user_lind_id,item_type,item_id,quantity,hassame,loc)
    
    
    def getUserEquipmentWeapon(self,user_line_id):
        user_job = self.getUserJob(user_line_id)
        equipment_back_loc = user_job["weapon"]
        equipment_back_loc = int(equipment_back_loc)
        print("loc:"+str(equipment_back_loc))
        #取得武器基本資料 透過bag
        _basic_item = self.getItemFromUserBackPack(user_line_id,equipment_back_loc)
        _id = _basic_item["item_id"]
        print("id在這"+str(_id))
        _basic_weapon_info = self.getWeaponInfo(_id)
        #取得玩家對這個武器的加乘資料
        _weapon_add_info = self.getValueFromUserWeapon(user_line_id,equipment_back_loc)
        print("加成資料")
        print(_weapon_add_info)
        #_json={"weapon_id":row[0],"str_add":row[1],"int_add":row[2],"dex_add":row[3],"atk_add":row[4],"rare":row[5],"weapon_name":row[6],"img_type":row[7],"other_effect":_weapon_other_effect}
        _basic_weapon_info["str_add"]+=_weapon_add_info["str_add"]
        _basic_weapon_info["int_add"]+=_weapon_add_info["int_add"]
        _basic_weapon_info["dex_add"]+=_weapon_add_info["dex_add"]
        _basic_weapon_info["atk_add"]+=_weapon_add_info["atk_add"]
        _basic_weapon_info["uses_reel"] = _weapon_add_info["uses_reel"]
        _basic_weapon_info["available_reeltime"] = _weapon_add_info["available_reeltime"]
        _basic_weapon_info["backpack_loc"] = _weapon_add_info["backpack_loc"]
        _basic_weapon_info["success_time"] = _weapon_add_info["success_time"]
        #基本武器沒有任何加乘 直接套用addinfo
        if _basic_weapon_info["other_effect"] is None or _basic_weapon_info['other_effect'] == "None":
            _basic_weapon_info["other_effect"] = _weapon_add_info["description"]
        #基本武器有加乘 看weapon_add有沒有特殊加乘 要拿來加
        else:
            #weapon_add 沒有特殊加乘 照舊
            if _weapon_add_info["description"] is None or _weapon_add_info["description"] == "None":
                _basic_weapon_info["other_effect"] = _basic_weapon_info["other_effect"]
            else:
                for _effect in _weapon_add_info["description"]:
                    print(_effect)
                    _effect_type = _effect.split(":")[0]
                    _value = _effect.split(":")[1]
                    if _effect_type in _basic_weapon_info["other_effect"].keys():
                        _originvalue = _basic_weapon_info["other_effect"][_effect_type]
                        if "%" in _originvalue:
                            _ogvalue = int(_originvalue.split("%")[0])
                            if "%" in _value == False:
                                print("數值怪怪的 一個有%一個沒有")
                            else:
                                temp = int(_value.split("%")[0])
                                _ogvalue+=temp
                            _basic_weapon_info["other_effect"][_effect_type] = str(_ogvalue)+"%"
                        else:
                            _originvalue = int(_originvalue)
                            _value = int(_value)
                            _originvalue+=_value
                            _basic_weapon_info["other_effect"][_effect_type]=str(_originvalue)
                    else:
                        _basic_weapon_info["other_effect"][_effect_type] = str(_value)
        return _basic_weapon_info

    def getWeaponWithUserValue(self,weapon_id,user_weapon_value):
        print("get weapon info:"+str(weapon_id))
        _basic_weapon_info = self.getWeaponInfo(weapon_id)
        #取得玩家對這個武器的加乘資料
        _weapon_add_info = user_weapon_value
        print("加成資料")
        print(_weapon_add_info)
        #_json={"weapon_id":row[0],"str_add":row[1],"int_add":row[2],"dex_add":row[3],"atk_add":row[4],"rare":row[5],"weapon_name":row[6],"img_type":row[7],"other_effect":_weapon_other_effect}
        _basic_weapon_info["str_add"]+=_weapon_add_info["str_add"]
        _basic_weapon_info["int_add"]+=_weapon_add_info["int_add"]
        _basic_weapon_info["dex_add"]+=_weapon_add_info["dex_add"]
        _basic_weapon_info["atk_add"]+=_weapon_add_info["atk_add"]
        _basic_weapon_info["uses_reel"] = _weapon_add_info["uses_reel"]
        _basic_weapon_info["available_reeltime"] = _weapon_add_info["available_reeltime"]
        _basic_weapon_info["success_time"] = _weapon_add_info["success_time"]
        #基本武器沒有任何加乘 直接套用addinfo
        if _basic_weapon_info["other_effect"] is None or _basic_weapon_info['other_effect'] == "None":
            _basic_weapon_info["other_effect"] = _weapon_add_info["description"]
        #基本武器有加乘 看weapon_add有沒有特殊加乘 要拿來加
        else:
            #weapon_add 沒有特殊加乘 照舊
            if _weapon_add_info["description"] is None or _weapon_add_info["description"] == "None":
                _basic_weapon_info["other_effect"] = _basic_weapon_info["other_effect"]
            else:
                for _effect in _weapon_add_info["description"]:
                    print(_effect)
                    _effect_type = _effect.split(":")[0]
                    _value = _effect.split(":")[1]
                    if _effect_type in _basic_weapon_info["other_effect"].keys():
                        _originvalue = _basic_weapon_info["other_effect"][_effect_type]
                        if "%" in _originvalue:
                            _ogvalue = int(_originvalue.split("%")[0])
                            if "%" in _value == False:
                                print("數值怪怪的 一個有%一個沒有")
                            else:
                                temp = int(_value.split("%")[0])
                                _ogvalue+=temp
                            _basic_weapon_info["other_effect"][_effect_type] = str(_ogvalue)+"%"
                        else:
                            _originvalue = int(_originvalue)
                            _value = int(_value)
                            _originvalue+=_value
                            _basic_weapon_info["other_effect"][_effect_type]=str(_originvalue)
                    else:
                        _basic_weapon_info["other_effect"][_effect_type] = str(_value)
        return _basic_weapon_info
    
    def changeEquipmentWeapon(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE users_job SET equipment_weapon = %s WHERE user_line_id = %s"""
        self.cursor.execute(sql,(backpack_loc,user_line_id,))
        self.conn.commit()
    
    def getUserEquipmentList(self,user_line_id):
        user_job = self.getUserJob(user_line_id)
        equipment_back_loc = user_job["weapon"]
        equipment_back_loc = int(equipment_back_loc)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT backpack_loc,item_id FROM user_backpack where user_line_id = %s and item_type = 'weapon'"
        self.cursor.execute(sql,(user_line_id,))
        _result = self.cursor.fetchall()
        self.conn.commit()
        _weaponlist = []
        _now_weapon = {}
        for i in _result:
            loc = i[0]
            id = i[1]
            #取得武器基本資料
            _basic_weapon_info = self.getWeaponInfo(id)
            #取得玩家對這個武器的加乘資料
            _weapon_add_info = self.getValueFromUserWeapon(user_line_id,loc)
            #_json={"weapon_id":row[0],"str_add":row[1],"int_add":row[2],"dex_add":row[3],"atk_add":row[4],"rare":row[5],"weapon_name":row[6],"img_type":row[7],"other_effect":_weapon_other_effect}
            _basic_weapon_info["str_add"]+=_weapon_add_info["str_add"]
            _basic_weapon_info["int_add"]+=_weapon_add_info["int_add"]
            _basic_weapon_info["dex_add"]+=_weapon_add_info["dex_add"]
            _basic_weapon_info["atk_add"]+=_weapon_add_info["atk_add"]
            _basic_weapon_info["uses_reel"] = _weapon_add_info["uses_reel"]
            _basic_weapon_info["available_reeltime"] = _weapon_add_info["available_reeltime"]
            _basic_weapon_info["backpack_loc"] = loc
            _basic_weapon_info["success_time"] = _weapon_add_info["success_time"]
            #基本武器沒有任何加乘 直接套用addinfo
            if _basic_weapon_info["other_effect"] is None or _basic_weapon_info['other_effect'] == "None":
                _basic_weapon_info["other_effect"] = _weapon_add_info["description"]
            #基本武器有加乘 看weapon_add有沒有特殊加乘 要拿來加
            else:
                #weapon_add 沒有特殊加乘 照舊
                if _weapon_add_info["description"] is None or _weapon_add_info["description"] == "None":
                    _basic_weapon_info["other_effect"] = _basic_weapon_info["other_effect"]
                else:
                    for _effect in _weapon_add_info["description"]:
                        print(_effect)
                        _effect_type = _effect.split(":")[0]
                        _value = _effect.split(":")[1]
                        if _effect_type in _basic_weapon_info["other_effect"].keys():
                            _originvalue = _basic_weapon_info["other_effect"][_effect_type]
                            if "%" in _originvalue:
                                _ogvalue = int(_originvalue.split("%")[0])
                                if "%" in _value == False:
                                    print("數值怪怪的 一個有%一個沒有")
                                else:
                                    temp = int(_value.split("%")[0])
                                    _ogvalue+=temp
                                _basic_weapon_info["other_effect"][_effect_type] = str(_ogvalue)+"%"
                            else:
                                _originvalue = int(_originvalue)
                                _value = int(_value)
                                _originvalue+=_value
                                _basic_weapon_info["other_effect"][_effect_type]=str(_originvalue)
                        else:
                            _basic_weapon_info["other_effect"][_effect_type] = str(_value)
                            
            print("位置:"+str(loc)+" 編號:"+str(id))
            print(_basic_weapon_info)
            print("加成資料")
            print(_weapon_add_info)
            _weaponlist.append(_basic_weapon_info)
        index = 0
        for _weapon in _weaponlist:
            if _weapon["backpack_loc"] == equipment_back_loc:
                break
            else:
                index+=1
        _weaponlist = self.swapPositions(_weaponlist,index,0)
        print(_weaponlist)
        return _weaponlist

    # Swap function
    def swapPositions(self,list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list
    
    #給卷軸id 判斷玩家有沒有這個卷軸
    def getUserPackReelInfo(self,user_line_id,reel_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT backpack_loc,item_id,quantity FROM user_backpack WHERE user_line_id = %s and item_type = 'reel' and item_id = %s"
        self.cursor.execute(sql,(user_line_id,reel_id,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        if rows == None:
            return None
        else:
            return {"backpack_loc":rows[0],"item_id":rows[1],"quantity":rows[2]}
    
    #使用時勿必先判斷玩家有沒有該卷軸
    def setUserPackReelNum(self,user_line_id,reel_id,quantity):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE user_backpack SET quantity={quantity} WHERE user_line_id = '{user_line_id}' and item_type = 'reel' and item_id = {reel_id}""".format(quantity=quantity,user_line_id=user_line_id,reel_id=reel_id)
        self.cursor.execute(sql)
        self.conn.commit()

    
    def getUserUsingWeapon(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT equipment_weapon FROM users_job WHERE user_line_id = '" + user_line_id + "'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchone()
        self.conn.commit()
        if rows is not None:
            equipment_weapon = rows[0]
            #
            sql = "SELECT str_add,int_add,dex_add,atk_add,uses_reel,description,available_reeltime FROM user_weapon WHERE user_line_id = '" + user_line_id + "' and backpack_loc = '" + equipment_weapon + "'"
            self.cursor.execute(sql)
            rows = self.cursor.fetchone()
            if rows is not None:
                usingWeaponData = {'equipment_weapon':equipment_weapon,'str_add':rows[0],'int_add':rows[1],'dex_add':rows[2],
                                   'atk_add':rows[3],'uses_reel':rows[4],'description':rows[5],'available_reeltime':rows[6]}
                return usingWeaponData
        return {}
    
    def addWeaponReelSuccessTime(self,user_line_id,backpack_loc):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """UPDATE user_weapon SET success_time = success_time+1 WHERE user_line_id = %s and backpack_loc = %s"""
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        self.conn.commit()
    
    def getUserUsingReel(self,reel_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT reel_id,plus_str,plus_int,plus_dex,plus_atk,description,probability,image_type,reel_name FROM reel_list WHERE reel_id = '" + str(reel_id) + "'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchone()
        self.conn.commit()
        if rows is not None:
            reelData = {'reel_id':rows[0],'plus_str':rows[1],'plus_int':rows[2],'plus_dex':rows[3],
                        'plus_atk':rows[4],'description':rows[5],'probability':rows[6],'image_type':rows[7],'reel_name':rows[8]}
            return reelData
        return {}
    

    
    def getUserReelList(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """SELECT user_line_id,backpack_loc,item_type,item_id,quantity from user_backpack where user_line_id = %s and item_type = 'reel'"""
        self.cursor.execute(sql,(user_line_id,))
        _result = self.cursor.fetchall()
        self.conn.commit()
        if _result is not None:
            print(_result)
            _result_json = []
            for reel in _result:
                _id = reel[3]
                _reelbasic_info = self.getUserUsingReel(_id)
                _json={"reel_info_json":_reelbasic_info,"quantity":reel[4]}
                _result_json.append(_json)
            return _result_json
        else:
            return None
    
    def setEnhancedResult(self,enhancedData):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        if enhancedData['description'] is not None:
            sql = """UPDATE user_weapon SET str_add = '{0}',int_add = '{1}',dex_add = '{2}',atk_add = '{3}',uses_reel = '{4}',description = '{5}',available_reeltime = '{6}'
                     WHERE user_line_id = '{7}' and backpack_loc = '{8}'
            """.format(enhancedData['str_add'],enhancedData['int_add'],enhancedData['dex_add'],enhancedData['atk_add'],
            enhancedData['uses_reel'],enhancedData['description'],enhancedData['available_reeltime'],enhancedData['user_line_id'],enhancedData['equipment_weapon'])
        else:
            sql = """UPDATE user_weapon SET str_add = '{0}',int_add = '{1}',dex_add = '{2}',atk_add = '{3}',uses_reel = '{4}',available_reeltime = '{5}'
                     WHERE user_line_id = '{6}' and backpack_loc = '{7}'
            """.format(enhancedData['str_add'],enhancedData['int_add'],enhancedData['dex_add'],enhancedData['atk_add'],
            enhancedData['uses_reel'],enhancedData['available_reeltime'],enhancedData['user_line_id'],enhancedData['equipment_weapon'])
        self.cursor.execute(sql)
        self.conn.commit()
    
    def getSkillInfo(self,skill_id,job):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        table_name = "skill_list_"+job
        sql = "SELECT skill_id,skill_name,skill_description,skill_effect_description,max_level,max_book_time,leveladd_one_book,skill_type,own_level,own_job_level,skill_effect_addlv_description,image_type FROM {table_name} where skill_id = {skill_id}".format(table_name = table_name,skill_id = skill_id)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()
        self.conn.commit()
        
        if _result is not None:
            return {"skill_id":_result[0],"skill_name":_result[1],"skill_description":_result[2],"skill_effect_description":_result[3],"max_level":_result[4],"max_book_time":_result[5],"leveladd_one_book":_result[6],
            "skill_type":_result[7],"own_level":_result[8],"own_job_level":_result[9],"skill_effect_addlv_description":_result[10],"image_type":_result[11]}
        else:
            return None

    def addSkillToUser(self,user_line_id,skill_id,skill_job,skill_level,used_book_time):
        if self.checkUserHasSkill(user_line_id,skill_id,skill_job):
            print("已有此技能")
            return
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = """INSERT INTO public.user_skill(user_line_id, skill_id, skill_job, skill_level, used_book_time) VALUES ( %(user_line_id)s,%(skill_id)s,%(skill_job)s,%(skill_level)s,%(used_book_time)s)"""
        params = {'user_line_id':user_line_id, 'skill_id':skill_id,'skill_job':skill_job,'skill_level':skill_level,'used_book_time':used_book_time}
        self.cursor.execute(sql,params)
        self.conn.commit()

    def getLevelSkillList(self,level,job):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        table_name = "skill_list_"+job
        sql = "SELECT skill_id FROM {table_name} where own_level <= {level}".format(table_name = table_name,level = level)
        self.cursor.execute(sql)
        _result = self.cursor.fetchall()
        self.conn.commit()
        list = []
        if _result is not None:
            for id in _result:
                list.append(int(id[0]))
            print(list)
            return list
        else:
            return None
    
    def getUserSkillList(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT skill_id,skill_job FROM user_skill where user_line_id = '{user_line_id}'".format(user_line_id = user_line_id)
        self.cursor.execute(sql)
        _result = self.cursor.fetchall()
        _skills = {}
        _userskill_list = []
        for _id in _result:
            _skillid = int(_id[0])
            _skilljob = _id[1]
            _skills[_skillid] = _skilljob
        for skill in _skills:
            _job = _skills[skill]
            _id = skill
            skilljson = self.getSkillFromUser(user_line_id,_id,_job)
            _userskill_list.append(skilljson)
        return _userskill_list
    
    def checkUserHasSkill(self,user_line_id,skill_id,skill_job):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT skill_id FROM user_skill where user_line_id = '{user_line_id}' and skill_id = {skill_id} and skill_job = '{skill_job}'".format(user_line_id = user_line_id,skill_id = skill_id,skill_job=skill_job)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()
        if _result is not None:
            return True
        else:
            return False
    
    def getUserActiveSkillList(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT skill_id,skill_job FROM user_skill where user_line_id = '{user_line_id}'".format(user_line_id = user_line_id)
        self.cursor.execute(sql)
        _result = self.cursor.fetchall()
        _skills = {}
        _userskill_list = []
        for _id in _result:
            _skillid = int(_id[0])
            _skilljob = _id[1]
            _skills[_skillid] = _skilljob
        for skill in _skills:
            _job = _skills[skill]
            _id = skill
            skilljson = self.getSkillFromUser(user_line_id,_id,_job)
            if skilljson["skill_type"] == "active":
                _userskill_list.append(skilljson)
        #print("skill list")
        #這樣就是沒技能
        #print(_userskill_list == [] and len(_userskill_list) == 0)
        return _userskill_list
        
    
    def getSkillFromUser(self,user_line_id,skill_id,job):
        _skillbasic = self.getSkillInfo(skill_id,job)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT skill_id,skill_level,used_book_time FROM user_skill where user_line_id = '{user_line_id}' and skill_id = {skill_id} and skill_job = '{skill_job}'".format(user_line_id = user_line_id,skill_id = skill_id,skill_job=job)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()
        self.conn.commit()
        if _result == None:
            return None
        _skillfromUser =  {"skill_id":_result[0],"skill_level":_result[1],"used_book_time":_result[2]}
        #確認技能等級
        _skilllevel = _skillfromUser["skill_level"]
        _used_book_time = _skillfromUser["used_book_time"]
        _max_book_time = _skillbasic["max_book_time"]
        _one_book_addlv = _skillbasic["leveladd_one_book"]
        _max_level = _skillbasic["max_level"]
        _skillbasic["_skilllevel"] = _skilllevel
        _skillbasic["job"] = job
        _skillbasic["used_book_time"] = _used_book_time

        if _used_book_time > _max_book_time or _skilllevel > _max_level+_used_book_time*_one_book_addlv:
            print("三小 有問題 這人技能書吃的比最大還多本 外掛")
            return
        #依照skill的基本資料 透過技能等級 把狀態附加上去
        if _skillbasic["skill_effect_addlv_description"] != [] and len(_skillbasic["skill_effect_addlv_description"]) > 0:
            for _effect_addlv in _skillbasic["skill_effect_addlv_description"]:
                _type = _effect_addlv.split(":")[0]
                _value = _effect_addlv.split(":")[1]
                _ispesent = False
                if "%" in _value:
                    _value = int(_value.split("%")[0])
                else:
                    _value = int(_value)
                _index = 0
                for _basiceffect in _skillbasic["skill_effect_description"]:
                    _otype = _basiceffect.split(":")[0]
                    _ovalue = _basiceffect.split(":")[1]
                    #找到那筆資料ㄌ
                    if _otype == _type:
                        _origin_value = _ovalue
                        if "%" in _origin_value:
                            _ispesent = True
                            _origin_value_num = int(_origin_value.split("%")[0])
                        else:
                            _origin_value_num = int(_origin_value_num)
                        _origin_value_num+=_value*_skilllevel
                        if _ispesent:
                            _origin_value_num = str(_origin_value_num)+"%"
                        else:
                            _origin_value_num = str(_origin_value_num)
                        _skillbasic["skill_effect_description"][_index] = _otype+":"+_origin_value_num
                    else:
                        _index+=1
               
        if "*" in _skillbasic["skill_description"]:
            _sym = '*'
            lst = []
            for pos,char in enumerate(_skillbasic["skill_description"]):
                if(char == _sym):
                    lst.append(pos)
            index = 0
            for _effect in _skillbasic["skill_effect_description"]:
                _type = _effect.split(":")[0]
                _value = _effect.split(":")[1]
                _type = rpgDictionary.getChineseEffectName(_type)
                _skillbasic["skill_description"] = _skillbasic["skill_description"][0:lst[index]] + _type + _value +_skillbasic["skill_description"][lst[index]+1:]
                index +=1
        
        return _skillbasic

    def addUserSkillLevel(self,user_line_id,skill_id,skill_job):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "UPDATE user_skill SET skill_level = skill_level+1 where skill_id = {skill_id} and skill_job ='{skill_job}' and user_line_id = '{user_line_id}'".format(skill_id=skill_id,skill_job=skill_job,user_line_id=user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def decUserSkillPoint(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "UPDATE users_job SET skill_point = skill_point-1 where user_line_id = '{user_line_id}'".format(user_line_id=user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
    
    #轉蛋
    def getGashaponPrizeList(self,gashapon_num):
        
        _NumTable = ['zero','one','two','three']#數字英文表
        
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        gashapon_tableName = _NumTable[gashapon_num]
        sql = "SELECT * FROM gashapon_list_{gashapon_tableName}".format(gashapon_tableName=gashapon_tableName)
        self.cursor.execute(sql)
        self.conn.commit()
        prizeList=[]
        prizeList = self.cursor.fetchall()
        return prizeList
    
    #查詢玩家有的類型 type不傳就是所有的背包疊加數量 (卷軸等消耗道具會疊加,佔一格) type 可船 weapon reel
    def getUserBackItemNum(self,user_line_id,item_type="all"):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        if item_type == "all":
            sql = "SELECT count(*) FROM user_backpack where user_line_id = '{user_line_id}'".format(user_line_id = user_line_id)
        else:
            sql = "SELECT count(*) FROM user_backpack where user_line_id = '{user_line_id}' and item_type = '{item_type}'".format(user_line_id = user_line_id,item_type = item_type)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()[0]
        self.conn.commit()
        print(int(_result))
        return int(_result)
    
    def createNewWeapon(self,str_add,int_add,dex_add,atk_add,rare,weapon_name,image_type,other_description,available_reeltime):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        try:
            sql ="""INSERT INTO weapon_list (str_add, int_add,dex_add,atk_add,rare,weapon_name,image_type,other_description,available_reeltime) VALUES (%(str_add)s, %(int_add)s, %(dex_add)s, %(atk_add)s,%(rare)s,%(weapon_name)s,%(image_type)s,%(other_description)s,%(available_reeltime)s)"""
            params = {'str_add':str_add, 'int_add':int_add,'dex_add':dex_add,'atk_add':atk_add,'rare':rare,'weapon_name':weapon_name,'image_type':image_type,'other_description':other_description,'available_reeltime':available_reeltime}
            self.cursor.execute(sql,params)
            self.conn.commit()
            self.conn.close()
            return True
        except:
            return False
    
    def getMaxWeaponNow(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT max(weapon_id) FROM weapon_list"
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()[0]
        self.conn.commit()
        print(int(_result))
        return int(_result)

    def addAuction(self,user_line_id,item_type,item_id,list_price,weapon_json = {}):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        if item_type == "weapon":
            current =  datetime.now()
            str_time = current.strftime("%m/%d/%Y %H:%M:%S")
            print("time:")
            print(str_time)
            _str_add = weapon_json["str_add"]
            _int_add = weapon_json["int_add"]
            _dex_add = weapon_json["dex_add"]
            _atk_add = weapon_json["atk_add"]
            _description = str(weapon_json["description"]).replace("'", "").replace(" ","").replace("[","{").replace("]","}")
            if _description == 'None' or _description is None:
                _description = "{}"
            _uses_reel = str(weapon_json["uses_reel"]).replace("'", "").replace(" ","")
            print(_uses_reel)
            print(type(_uses_reel))
            available_reeltime = weapon_json["available_reeltime"]
            success_time = weapon_json["success_time"]
            sql = """INSERT INTO public.auction_list(
            user_line_id, item_type, item_id, list_price, auction_start_time, 
            str_add, int_add, dex_add, atk_add, uses_reel, available_reeltime, description, success_time) 
            VALUES (
            '{user_line_id}', '{item_type}', {item_id}, {list_price}, '{auction_start_time}'
            , {str_add}, {int_add}, {dex_add}, {atk_add}, '{uses_reel}', {available_reeltime}, '{_description}', {success_time}
            )""".format(user_line_id=user_line_id,item_type=item_type,item_id=item_id,list_price=list_price,auction_start_time = str_time,
                str_add = _str_add,int_add = _int_add,dex_add = _dex_add,atk_add = _atk_add,uses_reel = _uses_reel,available_reeltime = available_reeltime,
                _description = _description,success_time = success_time
            )
            self.cursor.execute(sql)
            self.conn.commit()
    
    def getAuction(self,auction_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT auction_id,user_line_id,item_id,list_price,auction_start_time,str_add,int_add,dex_add,atk_add,available_reeltime,description,success_time,uses_reel FROM auction_list where auction_id = '{auction_id}'".format(auction_id = auction_id)
        self.cursor.execute(sql)
        _auction = self.cursor.fetchone()
        self.conn.commit()
        owner_name = self.getUser(_auction[1])["user_line_name"]
        _auction_json = {"auction_id":_auction[0],"auction_line_id":_auction[1],"auction_owner":owner_name,"item_id":_auction[2],"list_price":_auction[3],
        "auction_start_time":_auction[4],"str_add":_auction[5],"int_add":_auction[6],"dex_add":_auction[7],"atk_add":_auction[8],"available_reeltime":_auction[9],
        "description":_auction[10],"success_time":_auction[11],"uses_reel":_auction[12]}
        _user_weapon_value = {"weapon_id":_auction[2],"str_add":_auction[5],"int_add":_auction[6],"dex_add":_auction[7],"atk_add":_auction[8],"available_reeltime":_auction[9],
        "description":_auction[10],"success_time":_auction[11],"uses_reel":_auction[12]}
        print(_user_weapon_value)
        _weapon = self.getWeaponWithUserValue(_auction[2],_user_weapon_value)
        auctions = {"weapon_json":_weapon,"auction_info":_auction_json}
        return auctions
    
    def removeAuction(self,auction_id,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "DELETE FROM auction_list where auction_id = '{auction_id}' AND user_line_id = '{user_line_id}'".format(auction_id = auction_id,user_line_id = user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
        print("remove auction:"+str(auction_id)+"done")
    
    def getAuctionList(self,item_type):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT auction_id,user_line_id,item_id,list_price,auction_start_time,str_add,int_add,dex_add,atk_add,available_reeltime,description,success_time,uses_reel FROM auction_list where item_type = '{item_type}'".format(item_type = item_type)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result is None or len(result) ==0:
            return None
        self.conn.commit()
        auctions = []
        for _auction in result:
            #print(_auction)
            #透過加成資料獲取武器數值
            #_json ={"user_line_id":_result[0],"weapon_id":_result[1],"backpack_loc":_result[2],"str_add":_result[3],"int_add":_result[4],"dex_add":_result[5],"atk_add":_result[6],"uses_reel":_result[7],"available_reeltime":_result[8],"success_time":_result[9],"description":_otherdescription}
            owner_name = self.getUser(_auction[1])["user_line_name"]
            _auction_json = {"auction_id":_auction[0],"auction_line_id":_auction[1],"auction_owner":owner_name,"item_id":_auction[2],"list_price":_auction[3],
            "auction_start_time":_auction[4],"str_add":_auction[5],"int_add":_auction[6],"dex_add":_auction[7],"atk_add":_auction[8],"available_reeltime":_auction[9],
            "description":_auction[10],"success_time":_auction[11],"uses_reel":_auction[12]}
            _user_weapon_value = {"weapon_id":_auction[2],"str_add":_auction[5],"int_add":_auction[6],"dex_add":_auction[7],"atk_add":_auction[8],"available_reeltime":_auction[9],
            "description":_auction[10],"success_time":_auction[11],"uses_reel":_auction[12]}
            print(_user_weapon_value)
            _weapon = self.getWeaponWithUserValue(_auction[2],_user_weapon_value)
            auctions.append({"weapon_json":_weapon,"auction_info":_auction_json})
            #print(_auction)
        return auctions
    
    def startWordBoss(self,boss_id):
        if self.getWordBossStatus() is not None:
            print("已有世界王進行中")
            return
        bossinfo = self.getWordBossInfo(boss_id)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        current =  datetime.now()
        str_database = (current.strftime("%m/%d/%Y %H:%M:%S"))
        sql = "INSERT INTO word_boss_status(boss_id,start_time,hp) VALUES({boss_id},'{start_time}',{hp})".format(boss_id = boss_id,start_time = str_database,hp = bossinfo["boss_hp"])
        self.cursor.execute(sql)
        self.conn.commit()

    def getWordBossStatus(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "select boss_id,start_time,hp from word_boss_status"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is None:
            print("目前沒有世界boss喔")
            return None
        self.conn.commit()
        _json ={"boss_id":result[0],"start_time":result[1],"hp":result[2]}
        return _json
    
    def getWordBossInfo(self,boss_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "select boss_id,boss_name,boss_hp,boss_drop_weapon,boss_image_url,boss_atk,boss_drop_reel from word_boss_list where boss_id = {boss_id}".format(boss_id = boss_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.conn.commit()
        if result is None:
            return None
        _json = {"boss_id":result[0],"boss_name":result[1],"boss_hp":result[2],"boss_drop_weapon":result[3],"boss_image_url":result[4],
        "boss_atk":result[5],"boss_drop_reel":result[6]}
        print(_json)
        return _json
    
    def getUserWordBossStatus(self,user_line_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "select user_line_id,total_damage,word_guide,last_atack_time from user_word_boss_status where user_line_id = '{user_line_id}'".format(user_line_id = user_line_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.conn.commit()
        if result is None:
            return None
        _json = {"user_line_id":result[0],"total_damage":result[1],"word_guide":result[2],"last_atack_time":result[3]}
        print(_json)
        return _json
    
    def setUserWordBossStatus(self,user_line_id):
        if self.getUserWordBossStatus(user_line_id) is not None:
            print("此玩家已有世界王資料不能使用set")
            return
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        
        user_word = self.getUserJob(user_line_id)["word"]
        if user_word is None:
            user_word = -1
        sql = "INSERT INTO user_word_boss_status(user_line_id,total_damage,word_guide) VALUES('{user_line_id}',{total_damage},{word_guide})".format(user_line_id = user_line_id,total_damage = 0,word_guide =user_word)
        self.cursor.execute(sql)
        self.conn.commit()
        print("玩家加入世界王")
    
    def addUserWordBossDamage(self,user_line_id,damage):
        if self.getUserWordBossStatus(user_line_id) is None:
            self.setUserWordBossStatus(user_line_id)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        current =  datetime.now()
        current = (current.strftime("%m/%d/%Y %H:%M:%S"))
        sql = "UPDATE user_word_boss_status SET total_damage = total_damage+{damage}, last_atack_time = '{current}' where user_line_id ='{user_line_id}' ".format(user_line_id = user_line_id,damage = damage,current = current)
        self.cursor.execute(sql)
        self.conn.commit()
        print("玩家攻擊世界王")


    def getWordBossUserList(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * FROM user_word_boss_status order by total_damage desc"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        players=[]
        for player in result:
            _username = self.getUser(player[0])["user_line_name"]
            players.append({"user_line_id":player[0],"total_damage":player[1],"word_guide":player[2],"player_name":_username})
        return players
    
    def getWordBossNowTotalDamage(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "select sum(total_damage) from user_word_boss_status"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.conn.commit()
        result = int(result[0])
        return result
    
    def damageWordBoss(self,totaldamage):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        now_boss_status = self.getWordBossStatus()
        if now_boss_status is None:
            print("目前沒有世界王")
            return None
        if now_boss_status["hp"] > totaldamage:
            now_boss_status["hp"] -= totaldamage
            sql = "UPDATE word_boss_status SET hp = {hp}".format(hp = now_boss_status["hp"])
            self.cursor.execute(sql)
            self.conn.commit()
        else:
            print("世界boss已陣亡")
            now_boss_status = self.getWordBossStatus()
            _bossinfo = self.getWordBossInfo(now_boss_status["boss_id"])
            _weaponlist = _bossinfo["boss_drop_weapon"]
            _reel = _bossinfo["boss_drop_reel"][0]
            #武器得獎主
            _userlist = self.getWordBossUserList()
            weights = []
            for user in _userlist:
                self.givePlayerItem(user["user_line_id"],"reel",_reel)
                weights.append(user["total_damage"])
            print("總遊戲玩家")
            print(_userlist)
            print("權重:")
            print(weights)
            weaponwinner = random.choices(_userlist,weights=weights)[0]
            weapon = random.choice(_weaponlist)
            _weaponid = int(weapon)
            _id = weaponwinner["user_line_id"]
            print("得獎主:"+str(_id))
            print("獲得武器:"+str(_weaponid))
            self.givePlayerItem(_id,"weapon",_weaponid)
            sql = "delete from word_boss_status"
            self.cursor.execute(sql)
            self.conn.commit()
            sql = "delete from user_word_boss_status"
            self.cursor.execute(sql)
            self.conn.commit()
        return result

        
if __name__ == "__main__":
    id = 'U8d0f4dfe21ccb2f1dccd5c80d5bb20fe'
    database = DataBase()
    # _weapon = database.getUserEquipmentWeapon(id)
    # user_weapon = database.getValueFromUserWeapon(id,_weapon["backpack_loc"])
    # database.addAuction(id,"weapon",user_weapon["weapon_id"],125555,user_weapon)
    database.startWordBoss(0)
    # database.getWordBossStatus()
    # database.addUserWordBossDamage(id,100)
    # # print(database.getUserWordBossStatus(id))
    # print(database.getWordBossUserList())
    # #print(database.damageWordBoss(999999999))
    # print(database.getWordBossStatus())
    # for auction in list:
    #     print("weapon info:\n")
    #     print(auction["weapon_json"])
    #     print("\nauction info:\n")
    #     print(auction["auction_info"])
    #print(database.getAuction(5))