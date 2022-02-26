import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']


class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        self.conn.commit()
        self.conn.close()
    
    def checkUser(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM users where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        self.conn.close()
        if row is not None:
            return True
        else:
            return False
    
    def createUser(self,user_line_id,user_line_name,user_img_link):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="""INSERT INTO users (user_line_name, user_line_id,user_img,user_money,locked_money) VALUES (%(user_line_name)s, %(user_line_id)s, %(user_img)s, %(user_money)s,%(locked_money)s)"""
        params = {'user_line_name':user_line_name, 'user_line_id':user_line_id,'user_img':user_img_link,'user_money':100000,'locked_money':0}
        self.cursor.execute(sql,params)
        self.conn.commit()
        self.conn.close()
    

    def getUser(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT * from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        json={"user_line_name":"","user_img_link":"","user_money":123}
        self.conn.close()
        if row is not None:
            json["user_line_name"] = row[0]
            json["user_info_id"] = row[2]
            json["user_img_link"] = row[3]
            json["user_money"] = str(row[4])
            json["locked_money"] = str(row[5])
            json["user_type"] = str(row[8])
            return json

    
    def getUserMoney(self,user_line_id):
        return self.getUser(user_line_id)["user_money"]
    
    def getUserName(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT * from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return row[0]

    def getCommandList(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT * FROM commands"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        commandlist = {}
        self.conn.close()
        if row is not None:
            for item in row:
                commandlist[item[0]]=[item[1]]
        return commandlist
    
    def getUserRank(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT * from users order by user_money DESC"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        commandlist = {}
        self.conn.close()
        rank = 1
        if row is not None:
            for item in row:
                if item[1] == user_line_id:
                    return rank
                rank+=1
        return rank
    

    def SetUserMoneyByIndex(self,user_index_id,money):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET user_money = """+str(money)+"""WHERE user_id = """+str(user_index_id)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


    def SetUserMoneyByLineId(self,user_line_id,money):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET user_money = (%(money)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'money':money,'line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def SetUserLockedMoneyByLineId(self,user_line_id,money):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET locked_money = (%(money)s) WHERE user_line_id = (%(line_id)s)"""
        params = {'money':money,'line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def GetUserLockedMoneyLineId(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT locked_money from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        return row[0]
    

    def getTop5Ranking(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="Select user_line_name, user_money from users ORDER BY user_money desc"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        result=[]
        for col in row:
            _reply =str(col[0])+" : $"+str(col[1])
            print(col[0])
            print(col[1])
            result.append(_reply)
        return result
    
    def getHobbyBet(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT * FROM users where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        return int(row[6])

    def setHobbyBet(self,user_line_id,new_hobbybet):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE users SET hobby_bet = %s WHERE user_line_id = %s"""
        data = (new_hobbybet, user_line_id)
        self.cursor.execute(sql,data)
        self.conn.commit()
        self.conn.close()


    def getDiceHistory(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """SELECT dice_history from gameinfo"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _historystr = row[0]
        self.conn.close()
        _parse = list(_historystr)
        print(_parse)
        return _historystr

    def setDiceHistory(self,new):
        old = self.getDiceHistory()
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
        self.conn.close()
    
    def getWatherMoney(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """select wather_money from gameinfo"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        _wathermoney = row[0]
        print("目前水錢")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    def setWatherMoney(self,new):
        print("目前水錢"+str(new))
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE gameinfo SET wather_money = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def addWatherMoney(self,add):
        now_wather_money = self.getWatherMoney()
        if add < 0:
            new_wather_money = now_wather_money-int(add)
        else:
            new_wather_money = int(add)+now_wather_money
        self.setWatherMoney(new_wather_money)
        print("目前水錢:"+str(new_wather_money))
    
    def getGrand(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """select grand from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        _wathermoney = row[0]
        print("目前Grand:")
        print(int(_wathermoney))
        return int(_wathermoney)

    def getMajor(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """select major from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        _wathermoney = row[0]
        print("目前Major:")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    def getMinor(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """select minor from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        _wathermoney = row[0]
        print("目前Minor:")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    def getMini(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """select mini from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        _wathermoney = row[0]
        print("目前Mini:")
        print(int(_wathermoney))
        return int(_wathermoney)
    
    
    def setGrand(self,new):
        print("設定jackpot Grand"+str(new))
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET grand = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def setMajor(self,new):
        print("設定jackpot Major"+str(new))
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET major = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def setMinor(self,new):
        print("設定jackpot Minor"+str(new))
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET minor = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def setMini(self,new):
        print("設定jackpot Mini"+str(new))
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET mini = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def getAllJackpot(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """select * from jackpot"""
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        print("GRAND:"+str(row[0])+" MAJOR:"+str(row[1])+" MINOR:"+str(row[2])+" MINI:"+str(row[3])+" LASTWIN:"+str(row[4])+" LASTWINprice:"+str(row[5]))
        return row
    
    def setAllJackpot(self,grand,major,minor,mini):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET grand = %s , major = %s , minor = %s , mini = %s """
        data = (grand, major,minor,mini)
        self.cursor.execute(sql,data)
        self.conn.commit()
        self.conn.close()
        print("更新jp:"+str(grand)+","+str(major)+","+str(minor)+","+str(mini))
    
    def setJpLastWin(self,_winnername,_winmoney):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET last_winner = %s , last_winprice = %s"""
        data = (_winnername, _winmoney)
        self.cursor.execute(sql,data)
        self.conn.commit()
        self.conn.close()
        print("更新jp中獎者:"+str(_winnername)+":"+str(_winmoney))
    
    def addAllJp(self,grand,major,minor,mini):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE jackpot SET grand = grand+ %s , major = major+ %s , minor = minor+%s , mini = mini+ %s """
        data = (grand, major,minor,mini)
        self.cursor.execute(sql,data)
        self.conn.commit()
        self.conn.close()
        print("增加jp:"+str(grand)+","+str(major)+","+str(minor)+","+str(mini))
    

    def checkUserDaily(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT daily_request_done FROM users where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        return bool(row[0])
    
    def setUserDaily(self,user_line_id,bool):
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
        self.conn.close()
    
    def setAllUserDaily(self,bool):
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
        self.conn.close()
    
    def checkUserHasJob(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="SELECT user_line_id FROM users_job where user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        self.conn.close()
        if row is not None:
            return True
        else:
            return False
    
    #初始
    def createUserJob(self,user_line_id,jobs):
        from Games import rpgGame
        maxhp = rpgGame.getMaxHp(jobs,1)
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql ="""INSERT INTO users_job (user_line_id, jobs, str, dex, intelligence, level, hp, exp) VALUES (%(user_line_id)s, %(jobs)s,10,10,10,1,%(maxhp)s,0)"""
        params = {'user_line_id':user_line_id, 'jobs':jobs,'maxhp':maxhp}
        self.cursor.execute(sql,params)
        self.conn.commit()
        self.conn.close()
    
    def getUserJob(self,user_line_id):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = "SELECT * FROM users_job where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        self.conn.close()
        _json = {}
        _json={"job":row[1],"str":row[2],"dex":row[3],"int":row[4],"level":row[5],"hp":row[6],"exp":row[7]}
        print(_json)
        return _json