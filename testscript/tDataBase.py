from ast import parse
from cgitb import reset
from dataclasses import dataclass
import os
from re import S
import re
from select import select
import psycopg2
from dotenv import load_dotenv
import random

import rpgDictionary
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
        sql = "SELECT user_line_id,jobs,level FROM users_job"
        self.cursor.execute(sql)
        _result = self.cursor.fetchall()
        self.conn.commit()
        for i in _result:
            _id = i[0]
            _job = i[1]
            _level = i[2]
            if _job == 'warrior':
                # self.addSkillToUser(_id,0,'warrior',1,0)
                # self.addSkillToUser(_id,1,'warrior',1,0)
                if _level >= 30:
                    self.addSkillToUser(_id,2,'warrior',1,0)
            elif _job == 'rog':
                # self.addSkillToUser(_id,0,'rog',1,0)
                # self.addSkillToUser(_id,1,'rog',1,0)
                if _level >= 30:
                    self.addSkillToUser(_id,2,'rog',1,0)
            else:
                # self.addSkillToUser(_id,0,'majic',1,0)
                # self.addSkillToUser(_id,1,'majic',1,0)
                if _level >= 30:
                    self.addSkillToUser(_id,2,'majic',1,0)
            print("done")
    
    def getLevelSkillList(self,level,job):
        self.cursor = self.conn.cursor()
        table_name = "skill_list_"+job
        sql = "SELECT skill_id FROM {table_name} where own_level >= {level}".format(table_name = table_name,level = level)
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
    
    def getSkillInfo(self,skill_id,job):
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
    
    def getUserSkillList(self,user_line_id):
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
        
    
    def getSkillFromUser(self,user_line_id,skill_id,job):
        _skillbasic = self.getSkillInfo(skill_id,job)
        self.cursor = self.conn.cursor()
        sql = "SELECT skill_id,skill_level,used_book_time FROM user_skill where user_line_id = '{user_line_id}' and skill_id = {skill_id} and skill_job = '{skill_job}'".format(user_line_id = user_line_id,skill_id = skill_id,skill_job=job)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()
        self.conn.commit()
        _skillfromUser =  {"skill_id":_result[0],"skill_level":_result[1],"used_book_time":_result[2]}
        #確認技能等級
        _skilllevel = _skillfromUser["skill_level"]
        _used_book_time = _skillfromUser["used_book_time"]
        _max_book_time = _skillbasic["max_book_time"]
        _one_book_addlv = _skillbasic["leveladd_one_book"]
        _max_level = _skillbasic["max_level"]
        _skillbasic["_skilllevel"] = _skilllevel
        _skillbasic["job"] = job
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
    
    def checkUserHasSkill(self,user_line_id,skill_id,skill_job):
        self.cursor = self.conn.cursor()
        sql = "SELECT skill_id FROM user_skill where user_line_id = '{user_line_id}' and skill_id = {skill_id} and skill_job = '{skill_job}'".format(user_line_id = user_line_id,skill_id = skill_id,skill_job=skill_job)
        self.cursor.execute(sql)
        _result = self.cursor.fetchone()
        if _result is not None:
            return True
        else:
            return False
    
    def addUserSkillLevel(self,user_line_id,skill_id,skill_job):
        self.cursor = self.conn.cursor()
        sql = "UPDATE user_skill SET skill_level = skill_level+1 where skill_id = {skill_id} and skill_job ='{skill_job}' and user_line_id = '{user_line_id}'".format(skill_id=skill_id,skill_job=skill_job,user_line_id=user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def decUserSkillPoint(self,user_line_id):
        self.cursor = self.conn.cursor()
        sql = "UPDATE users_job SET skill_point = skill_point-1 where user_line_id = '{user_line_id}'".format(user_line_id=user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
    
    def addSkillToUser(self,user_line_id,skill_id,skill_job,skill_level,used_book_time):
        if self.checkUserHasSkill(user_line_id,skill_id,skill_job):
            print("已有此技能")
            return
        self.cursor = self.conn.cursor()
        sql = """INSERT INTO public.user_skill(user_line_id, skill_id, skill_job, skill_level, used_book_time) VALUES ( %(user_line_id)s,%(skill_id)s,%(skill_job)s,%(skill_level)s,%(used_book_time)s)"""
        params = {'user_line_id':user_line_id, 'skill_id':skill_id,'skill_job':skill_job,'skill_level':skill_level,'used_book_time':used_book_time}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def addExpForPlayer(self,user_line_id,exp):
        self.cursor = self.conn.cursor()
        sql = "UPDATE users_job SET exp = exp+{exp} where user_line_id = '{user_line_id}'".format(exp=exp,user_line_id=user_line_id)
        self.cursor.execute(sql)
        self.conn.commit()
    


if __name__ == "__main__":
    _id = 'U8d0f4dfe21ccb2f1dccd5c80d5bb20fe'
    database = DataBase()
    #database.addExpForPlayer(_id,1000)
    #database.addSkillToUser(_id,3,"rog",1,0)
    #_id = 'U0b37a9d05272a9e82d0ee60ba10bdd72'
    # loc = database.checkUserPackMaxLoc(_id)
    #database.addToUserBackPack(_id,"weapon",5,1,loc)
    #database.addToUserWeapon(_id,5,loc,0,0,0,0)
    # local = {}
    # id1 = '123'
    # id2 = '2344'
    # print(id1 in local.keys())
    # if (id1 in local.keys()) is False:
    #     local[id1] = 1
    # else:
    #     _time = local[id1]
    #     _time+=1
    # if (id1 in local.keys()) is False:
    #     local[id1] = 1
    # else:
    #     _time = local[id1]
    #     _time+=1
    #     local[id1] = _time
    # print(local[id1])
    #loc = database.checkUserPackMaxLoc(_id)
    # json = database.getUserReelList(_id)
    # print(json)
    #print(database.getSkillInfo(2,'rog'))
    # database.addUserSkillLevel(_id,2,'rog')
    # database.decUserSkillPoint(_id)
    # print(database.checkUserHasSkill(_id,2,"rog"))
    #database.addSkillToUser(_id,2,"warrior",1,0)
    #database.getLevelSkillList(1,"rog")

