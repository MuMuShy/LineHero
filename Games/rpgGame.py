from ctypes.wintypes import INT
import decimal
from attr import dataclass
import psycopg2
from psycopg2.extras import Json
import sys
import json
import random
import os
import time
import math
from decimal import Decimal
import copy
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
    _maps = ["forest","elfforest","barbarian","ghostroad","shogunate"]
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
        return level*150+4*level*10
    elif job =="majic":
        return level*100+level*10*2.5+1*level*10
    elif job =="rog":
        return level*70+level*10*1.5+2*level*10

def getMaxExp(level):
    level = int(level)
    return 100*level*level


def getMapInfo(command_map_name):
    print("冒險囉")
    print(dataBase.getMapInfo(command_map_name))

def checkAdventureResult(adventure_json):
    current =  datetime.now()
    _begintime = datetime.strptime(adventure_json["start_time"],"%m/%d/%Y %H:%M:%S")
    time_elapsed = (current-_begintime) #經過的掛機時間
    time_elapsed = math.floor(time_elapsed.total_seconds())
    if time_elapsed > 86400: #如果超過24小時 設定為一小時
        time_elapsed = 86400
    print(time_elapsed)
    _monster_info = dataBase.getPetInfo(adventure_json["pet_id"])
    _adventure_map_info = dataBase.getAdventureMapInfoById(adventure_json["map_id"])
    _exp = _adventure_map_info["exp_min"]
    _money =  _adventure_map_info["money_min"]
    time_elapsed = math.floor(time_elapsed/60)
    _pet_exp_value = int(_monster_info["other_effect"]["exp_add"].split("%")[0])
    _pet_money_value = int(_monster_info["other_effect"]["money_add"].split("%")[0])
    _pet_exp_percent = Decimal(_pet_exp_value/100)
    _pet_money_percent = Decimal(_pet_money_value/100)
    _pet_add_exp =_exp*time_elapsed*_pet_exp_percent
    _pet_add_money = _exp*time_elapsed*_pet_money_percent
    print("pet add:")
    _pet_add_exp = math.ceil(_pet_add_exp)
    _pet_add_money = math.ceil(_pet_add_money)
    print(_pet_add_exp)
    print(_pet_add_money)
    _totalexp = _exp*time_elapsed+_pet_add_exp
    _totalmoney = _money*time_elapsed+_pet_add_money
    _result_json = {"pass_min":time_elapsed,"total_exp":_totalexp,"total_money":_totalmoney,"map_name":_adventure_map_info["map_name"],"pet_add_exp":_pet_add_exp,"pet_add_money":_pet_add_money}
    return _result_json

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

def getJobCreditResult(_job,weapon_info):
    #基礎爆擊率  戰士: 10% 盜賊 30% 法師 15%
    #基礎爆擊傷害 1.3
    if _job == "warrior":
        _basic = 10
    elif _job =="majic":
        _basic = 15
    elif _job =="rog":
        _basic = 30
    _addcredit = 0
    _addcreditdmg = 0
    _creditdmg = 1.3

    try:
        _weapon_credit = decimal.Decimal(weapon_info["other_effect"]["credit_add"].split("%")[0])
        print("武器增加爆擊機率:"+str(_weapon_credit))
        _addcredit+=_weapon_credit
    except:
        _addcredit = 0
        
    try:
        _addcreditdmg_percent = int(weapon_info["other_effect"]["credit_damage_add"])
        _addcreditdmg_percent = _addcreditdmg_percent/100
        print("武器增加爆商:"+str(_addcreditdmg_percent))
        _creditdmg+=_addcreditdmg_percent
        print("爆擊傷害:"+str(_creditdmg))
    except:
        _creditdmg = 1.3

    _basic+=_addcredit
    _basic = 100-_basic
    if _basic<=0:
        _basic = 0
    _result = random.randrange(0,100)
    print("爆擊 要骰大於:"+str(_basic)+" 骰出:"+str(_result))
    if _result >= _basic:
        #爆擊
        return _creditdmg
    else:
        return 1
        

def getJobAttackByjson(_user_job_json):
    _job = _user_job_json["job"]
    print(_job)
    if _job == "warrior":
        return _user_job_json["str"]*1.3
    elif _job =="majic":
        return _user_job_json["int"]*1.6
    elif _job =="rog":
        return _user_job_json["dex"]*1.7

def getJobWeaponAttackByjson(_user_job_json,weapon_atk):
    _job = _user_job_json["job"]
    print(_job)
    _random = random.randrange(90,110)
    _random/=100
    if _job == "warrior":
        return 1+(weapon_atk/100)*weapon_atk*1.3*_random
    elif _job =="majic":
        return 1+(weapon_atk/100)*weapon_atk*1.7*_random
    elif _job =="rog":
        return 1+(weapon_atk/100)*weapon_atk*1.5*_random

def addPlayerExp(_user_job_json,_exp):
    _user_job_json["exp"]+=_exp
    _now_max_exp = getMaxExp(_user_job_json["level"])
    while _user_job_json["exp"] >= _now_max_exp:
        _user_job_json["exp"] -= _now_max_exp
        _user_job_json["level"]+=1
        _user_job_json["skill_point"]+=1
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



def attackround(_user_line_id,_user_job_json,_target_monster_id,monster_hp,skill=None):
    _isCredit = False
    _playerjob = _user_job_json["job"]
    print("職業:"+_playerjob)
    skill_effec = "無觸發交戰技能"
    _weapon_info = dataBase.getUserEquipmentWeapon(_user_line_id)
    _user_job_temp = copy.deepcopy(_user_job_json)
    _user_job_temp["str"]+=_weapon_info["str_add"]
    _user_job_temp["int"]+=_weapon_info["int_add"]
    _user_job_temp["dex"]+=_weapon_info["dex_add"]
    #確認武器加乘血量
    try:
        hp_add = _weapon_info["other_effect"]["hp_add"]
        if "%" in hp_add:
            hp_add = int(hp_add.split("%")[0])
            hp_add/=100
            hp_add = getMaxHp(_playerjob,_user_job_json["level"])*hp_add
        else:
            hp_add = int(hp_add)
            hp_add = hp_add
    except:
        hp_add = 0 
    #依照四維的基礎傷害
    baseAttack = getJobAttackByjson(_user_job_temp)
    if _playerjob == "majic":
        _skill_active = random.randrange(0,100)
        if _skill_active >= 31:
            _afterjson = copy.deepcopy(_user_job_temp)
            print(_afterjson)
            _afterint = int(_afterjson["int"]*0.3)
            _afterjson["int"] = _afterjson["int"]+_afterint
            print(_afterjson)
            skill_effec = "觸發法師被動技能! 賢者之力 增加INT30% 目前INT:"+str(_afterjson["int"])
            baseAttack = getJobAttackByjson(_afterjson)
    #BASE ATTACK 戰士STR*1.3 法師INT*2 盜賊DEX*1.5
    #基礎傷害 -> 骰子 * 能力點   
    attackpow = getJobRollResult(_playerjob)
    #基礎爆擊率  戰士: 10% 盜賊 30% 法師 20% 基礎爆擊傷害: 1.3
    _credit = getJobCreditResult(_playerjob,_weapon_info)
    if _credit > 1:
        _isCredit = True
    #武器數值計算
    _weaponpow = getJobWeaponAttackByjson(_user_job_temp,_weapon_info["atk_add"])
    
    
    #法師武器攻擊會另外算魔法傷害
    if _playerjob == "majic":
        try:
            _majic_weaponpower = int(_weapon_info["other_effect"]["matk_add"])
            _majic_weaponpower = _majic_weaponpower/100
            _weaponpow += 1+(1*_majic_weaponpower)
            print("法師Weapon power"+str(_majic_weaponpower))
        except:
            _weaponpow = _weaponpow

    print("武器傷害:"+str(_weaponpow))
    _attack_result = int(int(baseAttack*attackpow)+int(_weaponpow)*_credit)
    #查看技能
    _skilldes = ""
    if skill is not None:
        _effects = skill["skill_effect_description"][0]
        _type = _effects.split(":")[0]
        _value = _effects.split(":")[1]
        #傷害性技能
        if _type == "damage":
            if "%" in _value:
                _value = int(_value.split("%")[0])
                _value = _value/100
            else:
                _value = int(_value)
            _skilldamage = int(baseAttack*attackpow)*_value*_credit
            _skilldamage = math.ceil(_skilldamage)
            print("技能傷害:"+str(_skilldamage))
            
            _attack_result = _skilldamage

    
    #取得stability屬性 3號技能固定式精準之x的技能
    _stability = dataBase.getSkillFromUser(_user_line_id,3,_playerjob)
    _stabilityValueBasic = 85 # 基礎浮動率下限
    if _stability is not None:
        _stabilityValue = _stability["skill_effect_description"][0].split(":")[1]
        _stabilityValue = int(_stabilityValue.split("%")[0])
        _stabilityValueBasic = _stabilityValueBasic + int(_stabilityValueBasic*(_stabilityValue/100))
        print("穩定度最終下限結果:"+str(_stabilityValueBasic))
    #浮動率 85~120%
    _random = random.randrange(_stabilityValueBasic,120)

    _attack_result*=_random/100
    _attack_result = int(_attack_result)
    if skill is not None:
        _skilldes = "\n使用技能 "+skill["skill_name"]+" 傷害: "+str(_skilldamage)

    _monster_base_info = dataBase.getMonsterInfo(_target_monster_id)
    _monster_hp = monster_hp-_attack_result
    _monsterAttack = int(random.randrange(int(_monster_base_info["attack"]*0.7),int(_monster_base_info["attack"])))

    #盜賊閃避機制
    if _playerjob =="rog":
        _avoid_str=""
        _avoid_damage = random.randrange(0,100)
        if _avoid_damage >= 70:
            _avoid_str="\n盜賊觸發閃避!(30%) 免疫此輪傷害"
            _monsterAttack = 0


    _playerhp = _user_job_json["hp"] - _monsterAttack
    if _playerjob =="rog" and skill is None:
        _playerhp+=int(_attack_result*0.1)
        if _playerhp > getMaxHp(_playerjob,_user_job_json["level"])+hp_add:
            _playerhp = getMaxHp(_playerjob,_user_job_json["level"])+hp_add
        skill_effec = "觸發盜賊被動技能! 嗜血如命 回復HP:"+str(int(_attack_result*0.1))+_avoid_str
        
    skill_effec+=_skilldes
    _result={}
    if _playerhp <= 0:
        _playerhp = 0
    if _monster_hp<=0:
        _monster_hp = 0
    print("怪物攻擊:"+str(_monsterAttack)+"玩家剩餘血量:"+str(_playerhp))
    print("玩家傷害:"+str(_attack_result)+" 怪物剩餘血量:"+str(_monster_hp))
    
    if dataBase.getUserRoundInfo(_user_line_id)["use_run_chance"] == True:
        dataBase.setUserRoundRunChance(_user_line_id,False)
    if _monster_hp > 0:
        #怪物沒有死亡 把怪物的攻擊結果一起帶回
        _user_job_json["hp"] = _playerhp
        if _playerhp <= 0:
            #輸囉
            _result={"Result":"loose"}
            _user_job_json["hp"] = 0
            _tempexp = _user_job_json["exp"]
            _maxexp = getMaxExp(_user_job_json["level"])
            _tempexp = _tempexp-(_maxexp*0.1)
            if _tempexp<=0:
                _tempexp = 0
            _user_job_json["exp"] = _tempexp
            dataBase.ClearUserBattle(_user_line_id)
            dataBase.setUserJobStatus(_user_line_id,_user_job_json)
            print("die")
        else:
            #玩家沒死 怪物也沒死 
            #更新status
            dataBase.UpdateUserBattleStatus(_user_line_id,_target_monster_id,"player",_monster_hp)
            dataBase.setUserJobStatus(_user_line_id,_user_job_json)
            _monster_base_info["hp"] = _monster_hp
            _result={"Result":"monster_alive","dice_result":attackpow,"mosnter_damage":_monsterAttack,"player_damage":_attack_result,"monster_result_json":_monster_base_info,"player_result_json":_user_job_json,"skill_efect":skill_effec,"is_credit":_isCredit,"weapon_info":_weapon_info}
    else:
        if _playerjob =="rog":
            _temp = _user_job_json["hp"]
            _temp+=int(_attack_result*0.1)
            if _temp > getMaxHp(_playerjob,_user_job_json["level"])+hp_add:
                _temp = getMaxHp(_playerjob,_user_job_json["level"])+hp_add
            _user_job_json["hp"] = _temp
        #統計職業效果觸發
        _end_job_result = ""
        #掉落金錢 先隨機
        if _user_job_json["job"] == "warrior":
            _maxhp = getMaxHp(_user_job_json["job"],_user_job_json["level"])+hp_add
            print("max: "+str(_maxhp))
            _health = _maxhp*0.1
            if _user_job_json["hp"] + _health <= _maxhp:
                _user_job_json["hp"] +=_health
            else:
                _user_job_json["hp"] = _maxhp
            _end_job_result ="觸發戰士被動效果 戰士精神 回復血量:"+str(int(_health))
        _money = random.randrange(500,2000)
        _money+=_user_job_json["level"]*30
        _originmoney = int(dataBase.getUserMoney(_user_line_id))+_money
        dataBase.SetUserMoneyByLineId(_user_line_id,_originmoney)
        dataBase.ClearUserBattle(_user_line_id)
        _origlevel = _user_job_json["level"]
        _user_job_json = addPlayerExp(_user_job_json,_monster_base_info["exp"])
        _islevelup = False
        print( _user_job_json["level"])
        print(_origlevel)
        if _user_job_json["level"] > _origlevel:
            _islevelup = True
            skilllist = dataBase.getLevelSkillList(_user_job_json["level"],_user_job_json["job"])
            print("現在等級應該要有的id:")
            print(skilllist)
            for skillid in skilllist:
                if dataBase.checkUserHasSkill(_user_line_id,skillid,_user_job_json["job"]) == False:
                    print("玩家沒有這招:"+str(skillid))
                    dataBase.addSkillToUser(_user_line_id,skillid,_user_job_json["job"],1,0)
        dataBase.setUserJobStatus(_user_line_id,_user_job_json)
        _strtext ="戰鬥勝利! 獲得 exp:"+str(_monster_base_info["exp"])+ "金幣:" + str(_money)+"\n"+"剩餘血量:"+str(_user_job_json["hp"])+"/"+str(getMaxHp(_user_job_json["job"],_user_job_json["level"])+hp_add)
        _result={"Result":"win","dice_result":attackpow,"player_damage":_attack_result,"monster_result_json":_monster_base_info,"player_result_json":_user_job_json,"is_level_up":_islevelup,"get_money":_money,"end_job_result":_end_job_result,"skill_efect":skill_effec,"is_credit":_isCredit,"weapon_info":_weapon_info,"win_txt":_strtext}

    return _result
    
def WeaponEnhancement(user_line_id,reel_id):
    import random
    #----------------------------------------------------------------------------------------------------------------#
    #資料庫讀取#
    usingWeaponData = dataBase.getUserUsingWeapon(user_line_id)
    
    reelData = dataBase.getUserUsingReel(reel_id)
    
    if usingWeaponData != {} and reelData != {}:
        if usingWeaponData['available_reeltime'] <= 0:
            return False,'強化次數不足，強化失敗!!'
        usingWeaponData['available_reeltime'] = usingWeaponData['available_reeltime'] - 1
        print(usingWeaponData['available_reeltime'])
        #----------------------------------------------------------------------------------------------------------------#
        #處理卷軸機率#
        probability = reelData['probability']
        if probability == 1.0:
            checksucess = True
        else:
            deno = 1
            mole = 1
            while probability < 1.0:
                mole*=10
                probability*=10
            deno = mole-int(probability)
            check = [True,False]
            checksucess = random.choices(check,weights=[mole-deno,deno])[0]
            print(checksucess,deno,mole-deno)
        
        if checksucess:
            str_add = usingWeaponData['str_add'] + reelData['plus_str']
            int_add = usingWeaponData['int_add'] + reelData['plus_int']
            dex_add = usingWeaponData['dex_add'] + reelData['plus_dex']
            atk_add = usingWeaponData['atk_add'] + reelData['plus_atk']
        #----------------------------------------------------------------------------------------------------------------#
        #處理紀錄卷軸數
            if usingWeaponData['uses_reel'] is None or usingWeaponData['uses_reel'] == "None":
                usingWeaponData['uses_reel'] = ""
                usingWeaponData['uses_reel'] = "{}".format(str(reelData['reel_id'])) + ":1"
            else:
                uses_reel = usingWeaponData['uses_reel'].split(',')
                result = []
                IS_HAVE = False
                for s in uses_reel:
                    print("s 內容")
                    print(s)
                    if s.split(':')[0] == str(reelData['reel_id']):
                        result.append(s.split(':')[0] + ':' + str(int(s.split(':')[1])+1))
                        IS_HAVE = True
                    else:
                        result.append(s.split(':')[0] + ':' + s.split(':')[1])
                if IS_HAVE != True:
                    result.append(str(reelData['reel_id']) + ':' + '1')
                usingWeaponData['uses_reel'] = ','.join(result)
        
        #----------------------------------------------------------------------------------------------------------------#
        #處理description
            if reelData['description'] is not None:
                if usingWeaponData['description'] is None or usingWeaponData['description'] == ['None']:
                    real_description = ""
                    for i in reelData['description']:
                        real_description = "{"+i.split(":")[0]+":"+i.split(":")[1]+"}"
                    usingWeaponData['description'] = str(real_description).replace("'",'').replace(' ','')
                else:
                    real_description = reelData['description']
                    temp_dict_real = {}
                    temp_dict_weapon = {}
                    for i in real_description:
                        temp_dict_real[i.split(':')[0]] = i.split(':')[1]
                    
                    weapon_description = usingWeaponData['description']
                    for i in weapon_description:
                        temp_dict_weapon[i.split(':')[0]] = i.split(':')[1]
                    
                    for key in temp_dict_real.keys():
                        if key in temp_dict_weapon.keys():
                            #計算如果是%數
                            if '%' in temp_dict_weapon[key]:
                                temp_dict_weapon[key] = str(int(temp_dict_weapon[key].replace('%','')) + int(temp_dict_real[key].replace('%',''))) + '%'
                            else:
                                temp_dict_weapon[key] = str(int(temp_dict_weapon[key]) + int(temp_dict_real[key]))
                        else:
                            #如果沒衝過此屬性
                            temp_dict_weapon[key] = temp_dict_real[key]
                    result=[]
                    for key in temp_dict_weapon.keys():
                        result.append(key+':'+temp_dict_weapon[key])

                    
                    #usingWeaponData['description'] = '{'+','.join(result)+'}'
                    usingWeaponData['description'] = str(temp_dict_weapon).replace("'", "").replace(" ","")
            else:
                usingWeaponData['description'] = "{" + str(usingWeaponData['description']).replace("'", "").replace(" ","").replace("[", "").replace("]","") + "}"
                #print(usingWeaponData['description'])
        #----------------------------------------------------------------------------------------------------------------#
        #UPDATE DB
            enhancedData = {'user_line_id':user_line_id,'equipment_weapon':usingWeaponData['equipment_weapon'],
                            'str_add':str_add,'int_add':int_add,'dex_add':dex_add,'atk_add':atk_add,'uses_reel':usingWeaponData['uses_reel'],
                            'description':usingWeaponData['description'],'available_reeltime':usingWeaponData['available_reeltime']}

            dataBase.setEnhancedResult(enhancedData)
            
            return True,'強化成功!!'
        else:
            usingWeaponData['description'] = "{" + str(usingWeaponData['description']).replace("'", "").replace(" ","").replace("[", "").replace("]","") + "}"
            enhancedData = {'user_line_id':user_line_id,'equipment_weapon':usingWeaponData['equipment_weapon'],
                            'str_add':usingWeaponData['str_add'],'int_add':usingWeaponData['int_add'],'dex_add':usingWeaponData['dex_add'],'atk_add':usingWeaponData['atk_add'],
                            'uses_reel':usingWeaponData['uses_reel'],'description':usingWeaponData['description'],'available_reeltime':usingWeaponData['available_reeltime']}

            dataBase.setEnhancedResult(enhancedData)
            return False,'機率強化失敗!!'
    else:
        return False,'沒有卷軸或沒有武器而強化失敗'

def GashaponPlay(user_line_id,gashapon_num):
    import random
    
    prizeList = dataBase.getGashaponPrizeList(gashapon_num)
    prizeWeights = []
    for i in prizeList:
        prizeWeights.append(i[-1])
        
    winPrize = random.choices(prizeList,weights=prizeWeights)[0]
    
    print(winPrize)
    
    dataBase.givePlayerItem(user_line_id,winPrize[1],winPrize[0],winPrize[2])
    return winPrize