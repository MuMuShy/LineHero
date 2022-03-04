from ast import parse
from cgitb import reset
import os
from re import S
import re
from select import select
import psycopg2
from dotenv import load_dotenv
import random
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']


class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    
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
        row = self.cursor.fetchone()
        print(row)
        self.conn.close()

    def getUserJob(self,user_line_id):
        self.cursor = self.conn.cursor()
        sql = "SELECT * FROM users_job where user_line_id = '" +user_line_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        _json = {}
        _json={"job":row[1],"str":row[2],"dex":row[3],"int":row[4],"level":row[5],"hp":row[6],"exp":row[7],"weapon":row[8],"pet":row[9]}
        print(_json)
        return _json
    
    def getWeaponInfo(self,weapon_id):
        self.cursor = self.conn.cursor()
        sql = """SELECT * FROM weapon_list where weapon_id = %s"""
        self.cursor.execute(sql,(weapon_id,))
        self.conn.commit()
        row = self.cursor.fetchone()
        print(row)
        _json = {}
        _weapon_other_effect={}
        for _line in row[8]:
            _type = _line.split(":")[0]
            _value = _line.split(":")[1]
            _weapon_other_effect[_type] = _value
        _json={"weapon_id":row[0],"str_add":row[1],"int_add":row[2],"dex_add":row[3],"atk_add":row[4],"rare":row[5],"weapon_name":row[6],"img_type":row[7],"other_effect":_weapon_other_effect}
        print(_json)
        return _json

    def checkUserPackMaxLoc(self,user_line_id):
        self.cursor = self.conn.cursor()
        sql ="""select max(backpack_loc) from user_backpack where user_line_id =(%(line_id)s) """
        params = {'line_id':user_line_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
        row = self.cursor.fetchone()
        num = row[0]
        print("目前玩家背包序列index到達:"+str(num))
        if num == None:
            return 0
        else:
            return num+1
    
    def addToUserBackPack(self,user_line_id,item_type,item_id,quantity,loc=-1):
        if loc ==-1:
            _nowpackindex = self.checkUserPackMaxLoc(user_line_id)
        else:
            _nowpackindex = loc
        self.cursor = self.conn.cursor()
        sql ="""INSERT INTO user_backpack (user_line_id, backpack_loc,item_type,item_id,quantity) VALUES (%(user_line_id)s, %(backpack_loc)s, %(item_type)s, %(item_id)s,%(quantity)s)"""
        params = {'user_line_id':user_line_id,'backpack_loc':_nowpackindex,'item_type':item_type,'item_id':item_id,'quantity':quantity}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def removeFromUserBackPack(self,user_line_id,backpack_loc):
        self.cursor = self.conn.cursor()
        sql ="""DELETE FROM user_backpack where user_line_id = %s and backpack_loc = %s """
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        self.conn.commit()
    
    def getItemFromUserBackPack(self,user_line_id,backpack_loc):
        self.cursor = self.conn.cursor()
        sql = """SELECT * FROM user_backpack where user_line_id = %s and backpack_loc = %s"""
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        _result = self.cursor.fetchone()
        self.conn.commit()
        print("result 在這")
        print(_result)
        _json ={"user_line_id":_result[0],"backpack_loc":_result[1],"item_type":_result[2],"item_id":_result[3],"quantity":_result[4]}
        return _json
    
    def getReelInfo(self,reel_id):
        self.cursor = self.conn.cursor()
        sql = "SELECT reel_id,plus_str,plus_int,plus_dex,plus_atk,description,probability,image_type,reel_name FROM reel_list WHERE reel_id = '" + str(reel_id) + "'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchone()
        if rows is not None:
            reelData = {'reel_id':rows[0],'plus_str':rows[1],'plus_int':rows[2],'plus_dex':rows[3],
                        'plus_atk':rows[4],'description':rows[5],'probability':rows[6],'image_type':rows[7],'reel_name':rows[8]}
            return reelData
        return {}
    
    def getUserReelList(self,user_line_id):
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
                _reelbasic_info = self.getReelInfo(_id)
                _json={"reel_info_json":_reelbasic_info,"quantity":reel[4]}
                _result_json.append(_json)
            return _result_json
        else:
            return None
    
    def addToUserWeapon(self,user_line_id,weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add):
        self.cursor = self.conn.cursor()
        sql ="""INSERT INTO user_weapon (user_line_id, weapon_id,backpack_loc,str_add,int_add,dex_add,atk_add) VALUES (%(user_line_id)s, %(weapon_id)s, %(backpack_loc)s, %(str_add)s, %(int_add)s,%(dex_add)s,%(atk_add)s)"""
        params = {'user_line_id':user_line_id,'weapon_id':weapon_id,'backpack_loc':backpack_loc,'str_add':str_add,'int_add':int_add,'dex_add':dex_add,'atk_add':atk_add}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def getValueFromUserWeapon(self,user_line_id,backpack_loc):
        self.cursor = self.conn.cursor()
        sql = """SELECT * FROM user_weapon where user_line_id = %s and backpack_loc = %s"""
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        _result = self.cursor.fetchone()
        self.conn.commit()
        print(_result)
        _json ={"user_line_id":_result[0],"weapon_id":_result[1],"backpack_loc":_result[2],"str_add":_result[3],"int_add":_result[4],"dex_add":_result[5],"atk_add":_result[6]}
        return _json

    def removeUserWeapon(self,user_line_id,backpack_loc):
        self.cursor = self.conn.cursor()
        sql ="""DELETE FROM user_weapon where user_line_id = %s and backpack_loc = %s """
        self.cursor.execute(sql,(user_line_id,backpack_loc))
        self.conn.commit()    
    
    def getUserEquipmentWeapon(self,user_line_id):
        user_job = self.getUserJob(user_line_id)
        equipment_back_loc = user_job["weapon"]
        equipment_back_loc = int(equipment_back_loc)
        print("loc:"+str(equipment_back_loc))
        #取得武器基本資料 透過bag
        _basic_item = self.getItemFromUserBackPack(user_line_id,equipment_back_loc)
        _id = _basic_item["item_id"]
        _basic_weapon_info = self.getWeaponInfo(_id)
        #取得玩家對這個武器的加乘資料
        _weapon_add_info = self.getValueFromUserWeapon(user_line_id,equipment_back_loc)
        #_json={"weapon_id":row[0],"str_add":row[1],"int_add":row[2],"dex_add":row[3],"atk_add":row[4],"rare":row[5],"weapon_name":row[6],"img_type":row[7],"other_effect":_weapon_other_effect}
        _basic_weapon_info["str_add"]+=_weapon_add_info["str_add"]
        _basic_weapon_info["int_add"]+=_weapon_add_info["int_add"]
        _basic_weapon_info["dex_add"]+=_weapon_add_info["dex_add"]
        _basic_weapon_info["atk_add"]+=_weapon_add_info["atk_add"]
        return _basic_weapon_info

    def changeEquipmentWeapon(self,user_line_id,backpack_loc):
        self.cursor = self.conn.cursor()
        sql = """UPDATE users_job SET equipment_weapon = %s WHERE user_line_id = %s"""
        self.cursor.execute(sql,(backpack_loc,user_line_id,))
        self.conn.commit()

    def updateall(self):
        self.cursor = self.conn.cursor()
        sql = "SELECT user_line_id,jobs FROM users_job"
        self.cursor.execute(sql)
        _result = self.cursor.fetchall()
        self.conn.commit()
        for i in _result:
            _id = i[0]
            _job = i[1]
            loc = self.checkUserPackMaxLoc(_id)
            if _job == 'warrior':
                self.addToUserBackPack(_id,"weapon",7,1,loc)
                self.addToUserWeapon(_id,7,loc,0,0,0,0)
            elif _job == 'rog':
                self.addToUserBackPack(_id,"weapon",6,1,loc)
                self.addToUserWeapon(_id,6,loc,0,0,0,0)
            else:
                self.addToUserBackPack(_id,"weapon",5,1,loc)
                self.addToUserWeapon(_id,5,loc,0,0,0,0)

    def getUserEquipmentList(self,user_line_id):
        user_job = self.getUserJob(user_line_id)
        equipment_back_loc = user_job["weapon"]
        equipment_back_loc = int(equipment_back_loc)
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
            print("位置:"+str(loc)+" 編號:"+str(id))
            if loc == equipment_back_loc:
                _now_weapon = _basic_weapon_info
            else:
                _weaponlist.append(_basic_weapon_info)
        _weaponlist.insert(0,_now_weapon)
        print(_weaponlist)
        return _weaponlist
    
    def getUserPackReelInfo(self,user_line_id,reel_id):
        self.cursor = self.conn.cursor()
        sql = "SELECT backpack_loc,item_id,quantity FROM user_backpack WHERE user_line_id = %s and item_type = 'reel' and item_id = %s"
        self.cursor.execute(sql,(user_line_id,reel_id,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        if len(rows) == 0:
            return None
        else:
            return {"backpack_loc":rows[0],"item_id":rows[1],"quantity":rows[2]}
    
    #確定某格欄位有多少個物品
    def checkItemNumFromLoc(self,user_line_id,backpack_loc):
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
        _numorigin = self.checkUsefulItemNum(user_line_id,backpack_loc)
        #消耗品同種類還有庫存 只要修改他的quantity
        if _numorigin - quantity > 0:
            _finalquantity = _numorigin - quantity
            sql = """UPDATE user_backpack SET quantity = %s WHERE user_line_id = %s and backpack_loc = %s"""
            self.cursor.execute(sql,(_finalquantity,user_line_id,backpack_loc,))
            self.conn.commit()
        else:
            print("這個物品用光了 把她拔掉")
            sql = """DELETE from user_backpack WHERE user_line_id = %s and backpack_loc = %s"""
            self.cursor.execute(sql,(_finalquantity,user_line_id,backpack_loc,))
            self.conn.commit()
    
    def giveAllPlayerUsefulItem(self,item_type,item_id,number):
        self.cursor = self.conn.cursor()
        sql = "SELECT user_line_id,jobs FROM users_job"
        self.cursor.execute(sql)
        _result = self.cursor.fetchall()
        self.conn.commit()
        for i in _result:
            _id = i[0]
            loc = self.checkUserPackMaxLoc(_id)
            self.addToUserBackPack(_id,item_type,item_id,number,loc)

if __name__ == "__main__":
    database = DataBase()
    _id = 'U8d0f4dfe21ccb2f1dccd5c80d5bb20fe'
    #loc = database.checkUserPackMaxLoc(_id)
    # database.addToUserBackPack(_id,"weapon",4,1,loc)
    # database.addToUserWeapon(_id,4,loc,0,0,0,0)
    database.giveAllPlayerUsefulItem("reel",2,10)
    #loc = database.checkUserPackMaxLoc(_id)
    #database.addToUserBackPack(_id,"reel",5,20,loc)
    # json = database.getUserReelList(_id)
    # print(json)
    #print(database.getUserPackReelInfo(_id,1))
    #print(database.checkItemNumFromLoc(_id,100))
    #database.checkUserPackMaxLoc(_id)
    #database.removeFromUserBackPack(_id,1)
    #database.checkUserPackMaxLoc(_id)
    #print(database.getItemFromUserBackPack(_id,0))
    #database.removeUserWeapon(_id,999)
    #print(database.getUserEquipmentWeapon(_id))
    #database.updateall()
    #database.changeEquipmentWeapon(_id,0)
    #database.getUserEquipmentList(_id)

