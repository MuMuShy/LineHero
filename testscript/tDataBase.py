from ast import parse
import os
from re import S
import psycopg2
from dotenv import load_dotenv
import random
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
        params = {'user_line_name':user_line_name, 'user_line_id':user_line_id,'user_img':user_img_link,'user_money':10000,'locked_money':0}
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
            json["user_img_link"] = row[3]
            json["user_money"] = str(row[4])
            json["locked_money"] = str(row[5])
            return json
    
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
        row = self.cursor.fetchone()
        print(row)
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
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        sql = """UPDATE gameinfo SET wather_money = """+str(new)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
    
    def addWatherMoney(self,add):
        now_wather_money = self.getWatherMoney()
        new_wather_money = int(add)+now_wather_money
        self.setWatherMoney(new_wather_money)
        
    def SetUserMoneyByLineId(self,user_line_id,money):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        # sql ="""UPDATE users SET user_money = """+str(money)+""" WHERE user_line_id = """+str(user_line_id)
        # self.cursor.execute(sql)
        # self.conn.commit()
        # self.conn.close()

        sql ="""UPDATE users SET user_money = """+str(money)+"""WHERE user_id = """+str(user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    database = DataBase()
    database.SetUserMoneyByLineId(10,10000)



