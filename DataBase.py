import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']


class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
    
    def checkUser(self,user_line_id):
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
        sql ="""INSERT INTO users (user_line_name, user_line_id,user_img,user_money,locked_money) VALUES (%(user_line_name)s, %(user_line_id)s, %(user_img)s, %(user_money)s,%(locked_money)s)"""
        params = {'user_line_name':user_line_name, 'user_line_id':user_line_id,'user_img':user_img_link,'user_money':10000,'locked_money':0}
        self.cursor.execute(sql,params)
        self.conn.commit()
    

    def getUser(self,user_line_id):
        sql = "SELECT * from users WHERE user_line_id = '"+user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        json={"user_line_name":"","user_img_link":"","user_money":123}
        if row is not None:
            json["user_line_name"] = row[0]
            json["user_img_link"] = row[3]
            json["user_money"] = str(row[4])
            json["locked_money"] = str(row[5])
            return json
    
    def getCommandList(self):
        sql = "SELECT * FROM commands"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        commandlist = {}
        if row is not None:
            for item in row:
                commandlist[item[0]]=[item[1]]
        return commandlist
               