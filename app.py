from cgitb import text
from modulefinder import replacePackageMap
import random
from time import sleep
from flask import Flask, request, abort
from flask import render_template
from dotenv import load_dotenv
import lineMessagePacker
import lineMessagePackerRpg
from DataBase import DataBase
from Games import diceGame, jpGame,rpgGame
load_dotenv()
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
import os
import bybitApi
import sys

app = Flask(__name__)


environment = os.getenv("ENVIRONMENT")
print("environment: "+environment)

local_storage={}

if environment =="DEV":
    print("本地開發 使用本地開發版本機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_DEV"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET_DEV"))  
else:
    print("線上heroku環境 預設線上版機器人")
    line_bot_api = LineBotApi(os.getenv("LINE_BOT_API"))
    handler = WebhookHandler(os.getenv("LINE_BOT_SECRET"))

database = DataBase()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#訪問網站
@app.route("/")
def home():
    return render_template("home.html")


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    user_send =event.message.text
    if user_send.strip().startswith("!"):
        _command_check = "!"+user_send.strip().split("!")[1].strip().lower()
    else:
        _command_check = user_send
    if _command_check.startswith("!") and _command_check != "!info" and database.checkUser(event.source.user_id) == False:
        print("此玩家沒加入好友 傳送提示訊息")
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="看來你還沒有加我好友或是創建個人資料呢!\n請先加我好友 然後使用 !info 指令"))
        return
    group_id =" "
    try:
        group_id =event.source.group_id
    except:
        group_id =" "
        print("no group")
    print(user_send)
    if _command_check =="!respawn":
        print("測試期間復活 $10000")
        _money = database.getUserMoney(event.source.user_id)
        print(_money)
        _money = int(_money)
        if _money > 0:
            _reply = "妳的餘額還沒有歸0 不能浴火重生喔!"
        elif database.GetUserLockedMoneyLineId(event.source.user_id) > 0:
            _reply ="請先把正在進行的遊戲結算"
        else:
            database.SetUserMoneyByLineId(event.source.user_id,10000)
            _reply = "已幫您復活 充值 $10000"
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=_reply))
    if user_send =="@bugreport":
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage("BUG回報",contents=lineMessagePacker.getBugReport()))
        return
    if user_send =="!ranking":
        top5 = database.getTop5Ranking()
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage("財力排行",contents=lineMessagePacker.getRanking(top5[0],top5[1],top5[2],top5[3],top5[4])))
        return
    if user_send =="@ranking":
        top5 = database.getTop5RpgRanking()
        print(top5)
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage("LV排行",contents=lineMessagePackerRpg.getRpgTop5Rank(top5)))
        return
    elif user_send =="!dailyrequest":
        if database.checkUserDaily(event.source.user_id) == True:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你已領取過每日獎賞囉"))
            return
        else:
            _nowmoney = int(database.getUserMoney(event.source.user_id))
            _nowmoney+=10000
            database.SetUserMoneyByLineId(event.source.user_id,_nowmoney)
            database.setUserDaily(event.source.user_id,True)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("每日獎賞已到帳!"))
            return
    elif _command_check.startswith("!initjob"):
        try:
            _job = user_send.split(" ")[1]
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="資料格式錯誤"))
            return
        if database.checkUserHasJob(event.source.user_id) == True:
            _userjson = database.getUser(event.source.user_id)
            _jobjson = database.getUserJob(event.source.user_id)
            _flex = lineMessagePackerRpg.getCheckJobButton()
            _reply = "你已經有職業囉"
            print("已經有職業!")
            print(_flex)
            line_bot_api.reply_message(
                        event.reply_token,
                        [TextSendMessage(text="你已經有職業囉"),
                        FlexSendMessage("確認職業",_flex)]
            )
            return
        else:
            if rpgGame.checkstrjobLegal(_job) == True:
                _reply = rpgGame.createrJob(event.source.user_id,_job)
                _userjson = database.getUser(event.source.user_id)
                _jobjson = database.getUserJob(event.source.user_id)
                _imglink = _userjson["user_img_link"]
                _rank = database.getUserRpgRank(event.source.user_id)
                _weapon = database.getUserEquipmentWeapon(event.source.user_id)
                _flex = lineMessagePackerRpg.getJobInfo(_imglink,_jobjson,_rank,_weapon)
                _flex_sub_menu = lineMessagePackerRpg.getJobInfoSubMenu()
                line_bot_api.reply_message(
                        event.reply_token,
                        [TextSendMessage(text=_reply),
                        FlexSendMessage("職業資訊",contents=_flex),
                        FlexSendMessage("職業資訊",contents=_flex_sub_menu),
                        ])
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="資料格式錯誤"))
            return
    elif user_send =="@pet":
        user_id = event.source.user_id
        try:
            profile = line_bot_api.get_profile(user_id)
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="看來你沒有加我好友! 請先加我好友喔"))
        _player_jobinfo = database.getUserJob(user_id)
        _pet_info = database.getPetInfo(_player_jobinfo["pet"])
        _flex_pet = lineMessagePackerRpg.getEquipmentPet(_pet_info)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("寵物資訊",contents=_flex_pet)
            )
    elif user_send =="@pet_adventure":
        user_id = event.source.user_id
        try:
            profile = line_bot_api.get_profile(user_id)
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="看來你沒有加我好友! 請先加我好友喔"))
            return
        #已經在掛機了 進入結算畫面 
        if database.UserIsInAdventure(event.source.user_id) == True:
            _nowstatus = database.getUserAdventureStatus(event.source.user_id)
            _adventure_result = rpgGame.checkAdventureResult(_nowstatus)
            _pet_info = database.getPetInfo(_nowstatus["pet_id"])
            _flex_adventure_result = lineMessagePackerRpg.getAdventureNowStatus(_pet_info,_adventure_result)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage("目前遠征資訊",contents=_flex_adventure_result)
                )
            return
        _flex_adventure = lineMessagePackerRpg.getAdventureMap()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("遠征團地圖資訊",contents=_flex_adventure)
            )
    elif user_send == "@petadventureback":
        if database.UserIsInAdventure(event.source.user_id) == False:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="沒有派處遠征軍喔!"))
            return
        _nowstatus = database.getUserAdventureStatus(event.source.user_id)
        _adventure_result = rpgGame.checkAdventureResult(_nowstatus)
        _user_job_json = database.getUserJob(event.source.user_id)
        _user_job_json = rpgGame.addPlayerExp(_user_job_json,_adventure_result["total_exp"])
        database.setUserJobStatus(event.source.user_id,_user_job_json)
        database.AddUserMoneyByLineId(event.source.user_id,_adventure_result["total_money"])
        database.ClearUserAdventureStatus(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已招回遠征軍隊!!\n獲得EXP : "+str(_adventure_result["total_exp"])+"\n獲得金錢 : "+str(_adventure_result["total_money"])))
    elif user_send.startswith("@petadventureGoto"):
        if database.UserIsInAdventure(event.source.user_id) == True:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="遠征隊已經出發了喔 要查看詳請可以進入寵物資訊頁面"))
            return
        try:
            _map = user_send.split(" ")[1]
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("指令格式有問題"))
            return
        _map_info = database.getAdventureMapInfo(_map)
        database.setUserAdventureStatus(event.source.user_id,_map_info["map_id"])
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="掛機成功 記得要按時來領取冒險隊獎勵,最多累積24HR"))
    elif user_send == "@jobinfo":
        user_id = event.source.user_id
        try:
            profile = line_bot_api.get_profile(user_id)
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="看來你沒有加我好友! 請先加我好友喔"))
        if database.checkUserHasJob(event.source.user_id) == False:
            _replyflex = lineMessagePackerRpg.getCreaterJobList()
            line_bot_api.reply_message(
            event.reply_token,[
            TextSendMessage(text="看來你好像還沒成為冒險家呢 請選擇職業吧!"),
            FlexSendMessage("職業資料",contents=_replyflex)])
            return
        _jobjson = database.getUserJob(event.source.user_id)
        profile = line_bot_api.get_profile(event.source.user_id)
        user_line_img = profile.picture_url
        _rank = database.getUserRpgRank(event.source.user_id)
        _weapon = database.getUserEquipmentWeapon(event.source.user_id)
        _packagejson = lineMessagePackerRpg.getJobInfo(user_line_img,_jobjson,_rank,_weapon)
        _flex_sub_menu = lineMessagePackerRpg.getJobInfoSubMenu()
        line_bot_api.reply_message(
            event.reply_token,[
            FlexSendMessage("職業資料",contents=_packagejson),
            FlexSendMessage("職業資料",contents=_flex_sub_menu)
            ])
    elif user_send =="@exper":
        if database.checkUserHasJob(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你還沒有創建冒險者喔\n請先使用 !info 裡面的冒險者之旅按鈕開始旅程"))
            return
        if database.getUserJob(event.source.user_id)["hp"] <= 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你沒有錢了... 想辦法賺錢復活吧 復活指令: @health"))
            return
        _reply = lineMessagePackerRpg.getExperList()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("冒險列表",contents=_reply))
    elif user_send == "@equipment":
        _weapon_json_list = database.getUserEquipmentList(event.source.user_id)
        _flex_equipment = lineMessagePackerRpg.getEquipmentList(_weapon_json_list)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("裝備列表",contents=_flex_equipment))
        return
    elif user_send.startswith("@changeequipment"):
        try:
            loc = int(user_send.split(" ")[1])
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="裝備編號好像有問題呢.."))
            return
        _checkitem = database.getItemFromUserBackPack(event.source.user_id,loc)
        if _checkitem == None:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您並沒有這個裝備喔"))
            return
        elif _checkitem["item_type"] != "weapon":
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="這個編號不是可裝備武器 請在確認!"))
            return
        database.changeEquipmentWeapon(event.source.user_id,loc)
        _user_job = database.getUserJob(event.source.user_id)
        _noweapon = database.getUserEquipmentWeapon(event.source.user_id)
        _maxhp = rpgGame.getMaxHp(_user_job["job"],_user_job["level"])
        #確認武器加乘血量
        try:
            hp_add = _noweapon["other_effect"]["hp_add"]
            if "%" in hp_add:
                hp_add = int(hp_add.split("%")[0])
                hp_add/=100
                hp_add = _maxhp*hp_add
            else:
                hp_add = int(hp_add)
                hp_add = hp_add
        except:
            hp_add = 0
        _maxhp+=hp_add
        if _user_job["hp"] >= _maxhp:
            _user_job["hp"] = _maxhp
        database.setUserJobStatus(event.source.user_id,_user_job)
        _weapon_json_list = database.getUserEquipmentList(event.source.user_id)
        _flex_equipment = lineMessagePackerRpg.getEquipmentList(_weapon_json_list)
        line_bot_api.reply_message(
            event.reply_token,[
            TextSendMessage(text="切換裝備成功"),
            FlexSendMessage("切換裝備",contents=_flex_equipment)])
    elif user_send =="@skill":
        _skillpoint = database.getUserJob(event.source.user_id)["skill_point"]
        _skilllist = database.getUserSkillList(event.source.user_id)
        _skillflex = lineMessagePackerRpg.getSkillList(_skilllist)
        line_bot_api.reply_message(
            event.reply_token,[
            TextSendMessage(text="可用技能點數:"+str(_skillpoint)),
            FlexSendMessage("玩家技能",contents=_skillflex)])
        return
    elif user_send.startswith("@skilllevelup"):
        try:
            _info = user_send.split(" ")[1]
            _skilljob = _info.split(":")[0]
            _skillid = _info.split(":")[1]
            print("skill job:"+_skilljob+"     id:"+str(_skillid))
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="格式好像有問題ㄛ"))
            return
        if database.checkUserHasSkill(event.source.user_id,_skillid,_skilljob) == True:
            _skillnow = database.getSkillFromUser(event.source.user_id,_skillid,_skilljob)
            _nowlevel = _skillnow["_skilllevel"]
            _skillpoint = database.getUserJob(event.source.user_id)["skill_point"]
            #可以升級
            if _nowlevel < _skillnow["max_level"]+_skillnow["used_book_time"]*_skillnow["leveladd_one_book"] and _skillpoint > 1:
                database.addUserSkillLevel(event.source.user_id,_skillid,_skilljob)
                database.decUserSkillPoint(event.source.user_id)
                _skilllist = database.getUserSkillList(event.source.user_id)
                _skillflex = lineMessagePackerRpg.getSkillList(_skilllist)
                line_bot_api.reply_message(
                    event.reply_token,[
                    TextSendMessage(text="升級成功 目前可用技能點數:"+str(_skillpoint-1)),
                    FlexSendMessage("玩家技能",contents=_skillflex)])
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="這個技能好像無法升級... 有些技能可以使用技能書 使用後可以突破上限")
                    )
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="是不是點到別人的技能去了 你沒這招")
                    )


    elif user_send =="@bag":
        _bag_flex = lineMessagePackerRpg.getUsefulItemMenu()

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("背包類別",contents=_bag_flex))
        return
    elif user_send =="@showreelList":
        _user_reel_lists = database.getUserReelList(event.source.user_id)
        if _user_reel_lists == None or len(_user_reel_lists) ==0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你一張卷軸都沒有喔~"))
            return
        else:
            _flex = lineMessagePackerRpg.getUserReelList(_user_reel_lists)
            _nowweaponname = database.getUserEquipmentWeapon(event.source.user_id)["weapon_name"]
            line_bot_api.reply_message(
                event.reply_token,[
                TextSendMessage("注意 使用卷軸會直接使用在目前裝備武器上 目前裝備武器為:"+_nowweaponname),
                FlexSendMessage("背包卷軸",contents=_flex)])
            return
    elif user_send.startswith("@useReel"):
        try:
            _reel_id = user_send.split(" ")[1]
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("卷軸id好像有問題 請使用背包裏面的按鈕進行互動~"))
            return
        _reelinfo = database.getUserPackReelInfo(event.source.user_id,_reel_id)
        if _reelinfo == None:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你沒有此卷軸喔"))
            return
        else:
            _loc = _reelinfo["backpack_loc"]
        _has_reel_num = database.checkItemNumFromLoc(event.source.user_id,_loc)
        _noweapon = database.getUserEquipmentWeapon(event.source.user_id)
        if _noweapon["available_reeltime"] <= 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("強化次數已經用完了ㄛ"))
            return
        #移除一張 此卷軸 開始強化
        if _has_reel_num > 0:
            database.removeUsefulItemFromPack(event.source.user_id,_loc,1)
            _result,_description = rpgGame.WeaponEnhancement(event.source.user_id,_reel_id)
            _weapon = database.getUserEquipmentWeapon(event.source.user_id)
            _user_reel_lists = database.getUserReelList(event.source.user_id)
            _flex = lineMessagePackerRpg.getUserReelList(_user_reel_lists)
            if _result == True:
                database.addWeaponReelSuccessTime(event.source.user_id,_weapon["backpack_loc"])
                _weapon = database.getUserEquipmentWeapon(event.source.user_id)
                _weaponflex = lineMessagePackerRpg.getEquipmentList([_weapon])
                line_bot_api.reply_message(
                event.reply_token,[
                TextSendMessage(_description),
                FlexSendMessage("強化結果",contents=_weaponflex),
                FlexSendMessage("強化結果",contents=_flex)])
                return
            else:
                _weaponflex = lineMessagePackerRpg.getEquipmentList([_weapon])
                line_bot_api.reply_message(
                event.reply_token,[
                TextSendMessage(_description),
                FlexSendMessage("強化結果",contents=_weaponflex),
                FlexSendMessage("強化結果",contents=_flex)])
                return
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你的卷軸數量不夠喔"))
            return
    elif user_send == "@showusefullist":
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("敬請期待..."))
        return
    elif user_send.startswith("@goto"):
        
        try:
            _map = user_send.split(" ")[1]
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("指令格式有問題"))
            return
        if database.checkUserHasJob(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你還沒有創建冒險者喔\n請先使用 !info 裡面的冒險者之旅按鈕開始旅程"))
            return
        if rpgGame.checkstrMapLegal(_map) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("地圖有問題... 可能還未開放"))
            return
        if database.getUserJob(event.source.user_id)["hp"] <= 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("請先復活 復活指令: @health"))
            return
        
        _result = rpgGame.goToMap(_map,event.source.user_id)
        if _result["intobattle"] == False:
            _reply = _result["reply_text"]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=_reply))
            return
        else:
            _monster_json = _result["_monster"]
            _flex = lineMessagePackerRpg.getMonsterPacker(_monster_json,_monster_json["hp"]) 
            _activeskills = database.getUserActiveSkillList(event.source.user_id)
            _skillflex = lineMessagePackerRpg.getUserActiveSkills(_activeskills)
            line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=_result["reply_text"]),
                    FlexSendMessage("遭遇怪物!",contents=_flex),
                    FlexSendMessage("遭遇怪物!",contents=_skillflex)
                    ])
    elif user_send =="@run":
        if database.UserIsInCombat(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="沒戰鬥是要跑去哪~"))
            return
        else:
            _status = database.getUserRoundInfo(event.source.user_id)
            print(_status)
            _userjob = database.getUserJob(event.source.user_id)
            _monster = database.getMonsterInfo(_status["target_monster_id"])
            if rpgGame.getMaxHp(_userjob["job"],_userjob["level"]) < _monster["attack"]:
                database.ClearUserBattle(event.source.user_id)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="這個怪物似乎對你不削一顧 就任由你離開"))
                return
            if _status["use_run_chance"] == False:
                database.setUserRoundRunChance(event.source.user_id,True)
                _escape = random.randrange(0,10)
                print("escape result:"+str(_escape))
                _reply = ""
                if _escape > 5:
                    database.ClearUserBattle(event.source.user_id)
                    _reply = "運氣很好 跑掉了"
                else:
                    _reply ="逃跑失敗..."
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=_reply))
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="逃跑已經失敗了 請認命吧\n撐到下回合還可以再次逃跑"))
            return
    elif user_send =="@health":
        if database.checkUserHasJob(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你還沒有創建冒險者喔\n請先使用 !info 裡面的冒險者之旅按鈕開始旅程"))
            return
        print("花費10000回滿血")
        _money =  int(database.getUserMoney(event.source.user_id))
        if _money - 1500 < 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="沒錢還敢補血啊...."))
            return
        _money-=1500
        _user_job = database.getUserJob(event.source.user_id)
        _noweapon = database.getUserEquipmentWeapon(event.source.user_id)
        #確認武器加乘血量
        try:
            hp_add = _noweapon["other_effect"]["hp_add"]
            if "%" in hp_add:
                hp_add = int(hp_add.split("%")[0])
                hp_add/=100
                hp_add = rpgGame.getMaxHp(_user_job["job"],_user_job["level"])*hp_add
            else:
                hp_add = int(hp_add)
                hp_add = hp_add
        except:
            hp_add = 0 
        _maxhp = rpgGame.getMaxHp(_user_job["job"],_user_job["level"])+hp_add
        database.setUserMaxHp(event.source.user_id,_maxhp)
        database.SetUserMoneyByLineId(event.source.user_id,_money)
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已補滿狀態"))

    elif user_send =="@attack":
        if database.checkUserHasJob(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你還沒有創建冒險者喔\n請先使用 !info 裡面的冒險者之旅按鈕開始旅程"))
            return
        if database.UserIsInCombat(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="你還沒有進入戰鬥喔"))
            return
        else:
            _round_info = database.getUserRoundInfo(event.source.user_id)
            _palyer_job_info = database.getUserJob(event.source.user_id)
            _monsterbase = database.getMonsterInfo(_round_info["target_monster_id"])
            _game_result_json = rpgGame.attackround(event.source.user_id,_palyer_job_info,_monsterbase["monster_id"],_round_info["monster_hp"])
            try:
                _str_skill_text = _game_result_json["skill_efect"]
            except:
                print("no skill text")
            if _game_result_json["Result"] == "monster_alive":
                _attackbtnFlex = lineMessagePackerRpg.getAttackButton(_game_result_json["player_damage"],_game_result_json)
                _monsterFlex = lineMessagePackerRpg.getMonsterPacker(_monsterbase,_game_result_json["monster_result_json"]["hp"])
                _lastFlex = lineMessagePackerRpg.getRoundMonsterAliveButton(_game_result_json)
                _activeskills = database.getUserActiveSkillList(event.source.user_id)
                _skillflex = lineMessagePackerRpg.getUserActiveSkills(_activeskills)
                _strtext = "遭到怪物攻擊:"+ str(_game_result_json["mosnter_damage"]) +" 玩家剩餘血量:"+ str(_game_result_json["player_result_json"]["hp"])
                line_bot_api.reply_message(
                    event.reply_token,[
                    FlexSendMessage("攻擊!",contents=_attackbtnFlex),
                    TextSendMessage(text = _str_skill_text),
                    FlexSendMessage("怪物存活!",contents=_monsterFlex),
                    FlexSendMessage("怪物存活!",contents=_skillflex),
                    FlexSendMessage("怪物存活" ,contents= _lastFlex),])
            elif _game_result_json["Result"] =="win":
                _attackbtnFlex = lineMessagePackerRpg.getAttackButton(_game_result_json["player_damage"],_game_result_json)
                _strtext =_game_result_json["win_txt"]
                if _palyer_job_info["job"] == "warrior":
                    _strtext +=_game_result_json["end_job_result"]
                if _game_result_json["is_level_up"] == True:
                    _strtext+="\n恭喜升等!!"
                line_bot_api.reply_message(
                    event.reply_token,[
                    FlexSendMessage("最終一擊",contents=_attackbtnFlex),
                    TextSendMessage(text = _str_skill_text),
                    FlexSendMessage("戰鬥結束!",contents=lineMessagePackerRpg.getBattleEnd(_game_result_json)),
                    TextSendMessage(text = _strtext),])
            elif _game_result_json["Result"] == "loose":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("戰鬥結束! 很可惜你承受不住怪物的傷害 已死亡 -百分之10 exp 復活指令: @health"),
                    )
            return
    elif user_send.startswith("@useskill"):
        if database.checkUserHasJob(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("你還沒有創建冒險者喔\n請先使用 !info 裡面的冒險者之旅按鈕開始旅程"))
            return
        if database.UserIsInCombat(event.source.user_id) == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="你還沒有進入戰鬥喔"))
            return
        try:
            _skilljob = user_send.split(" ")[1]
            _skillid = user_send.split(" ")[2]
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="指令好像有問題ㄛ 請盡量用按鈕謝謝"))
            return
        if database.checkUserHasSkill(event.source.user_id,_skillid,_skilljob) == True:
            _skillinfo = database.getSkillFromUser(event.source.user_id,_skillid,_skilljob)
            _round_info = database.getUserRoundInfo(event.source.user_id)
            _palyer_job_info = database.getUserJob(event.source.user_id)
            _monsterbase = database.getMonsterInfo(_round_info["target_monster_id"])
            _game_result_json = rpgGame.attackround(event.source.user_id,_palyer_job_info,_monsterbase["monster_id"],_round_info["monster_hp"],_skillinfo)
            try:
                _str_skill_text = _game_result_json["skill_efect"]
            except:
                print("no skill text")
            if _game_result_json["Result"] == "monster_alive":
                _attackbtnFlex = lineMessagePackerRpg.getAttackButton(_game_result_json["player_damage"],_game_result_json)
                _monsterFlex = lineMessagePackerRpg.getMonsterPacker(_monsterbase,_game_result_json["monster_result_json"]["hp"])
                _activeskills = database.getUserActiveSkillList(event.source.user_id)
                _skillflex = lineMessagePackerRpg.getUserActiveSkills(_activeskills)
                _lastFlex = lineMessagePackerRpg.getRoundMonsterAliveButton(_game_result_json)
                _strtext = "遭到怪物攻擊:"+ str(_game_result_json["mosnter_damage"]) +" 玩家剩餘血量:"+ str(_game_result_json["player_result_json"]["hp"])
                line_bot_api.reply_message(
                    event.reply_token,[
                    FlexSendMessage("攻擊!",contents=_attackbtnFlex),
                    TextSendMessage(text = _str_skill_text),
                    FlexSendMessage("怪物存活!",contents=_monsterFlex),
                    FlexSendMessage("怪物存活!",contents=_skillflex),
                    FlexSendMessage("怪物存活" ,contents= _lastFlex),])
            elif _game_result_json["Result"] =="win":
                _attackbtnFlex = lineMessagePackerRpg.getAttackButton(_game_result_json["player_damage"],_game_result_json)
                _strtext =_game_result_json["win_txt"]
                if _palyer_job_info["job"] == "warrior":
                    _strtext +=_game_result_json["end_job_result"]
                if _game_result_json["is_level_up"] == True:
                    _strtext+="\n恭喜升等!!"
                line_bot_api.reply_message(
                    event.reply_token,[
                    FlexSendMessage("最終一擊",contents=_attackbtnFlex),
                    TextSendMessage(text = _str_skill_text),
                    FlexSendMessage("戰鬥結束!",contents=lineMessagePackerRpg.getBattleEnd(_game_result_json)),
                    TextSendMessage(text = _strtext),])
            elif _game_result_json["Result"] == "loose":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("戰鬥結束! 很可惜你承受不住怪物的傷害 已死亡 -百分之10 exp 復活指令: @health"),
                    )
            return
    elif user_send.startswith("!set"):
        if event.source.user_id != os.getenv("GM_LINE_ID"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無權限執行此指令"))
            return
        try:
            _user_id = user_send.split(" ")[1]
            _money = user_send.split(" ")[2]
            database.SetUserMoneyByIndex(_user_id,_money)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="成功到賬!"))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="錯誤 請確認id等資料"))
            return
    elif user_send.startswith("@giveitem"):
        if event.source.user_id != os.getenv("GM_LINE_ID"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無權限執行此指令"))
            return
        #try:
        _user_id = user_send.split(" ")[1]
        _item_type = user_send.split(" ")[2]
        _item_id = int(user_send.split(" ")[3])
        _quantity = int(user_send.split(" ")[4])
        _user_line_id = database.getUserById(_user_id)
        database.givePlayerItem(_user_line_id,_item_type,_item_id,_quantity)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="成功給予!"))
        return
        # except:
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text="錯誤 請確認id等資料"))
        #     return
    elif user_send.startswith("!wset"):
        if event.source.user_id != os.getenv("GM_LINE_ID"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無權限執行此指令"))
            return
        try:
            _money = user_send.split(" ")[1]
            database.setWatherMoney(_money)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="成功!"))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="錯誤 請確認等資料"))
            return
    elif user_send == "@gashtest":
        if event.source.user_id != os.getenv("GM_LINE_ID"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無權限執行此指令"))
            return
        _win = rpgGame.GashaponPlay(event.source.user_id,1)
        _id = _win[0]
        _type = _win[1]
        _num = _win[2]
        if _type == "weapon":
            _weaponinfo = database.getWeaponInfo(_id)
            _pricename = _weaponinfo["weapon_name"]
            url = "https://mumu.tw/images/weapons/"+str(_weaponinfo["weapon_id"])+"."+_weaponinfo["img_type"]
        elif _type == "reel":
            _reelinfo = database.getUserUsingReel(_id)
            _pricename = _reelinfo["reel_name"]
            url = "https://mumu.tw/images/reels/"+str(_reelinfo["reel_id"])+"."+_reelinfo["image_type"]
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="獎蛋機台好像怪怪的 抽到沒有的類型 請通知管理員"))
            return
        _flex = lineMessagePackerRpg.getGashsopResult(url,_pricename)
        line_bot_api.reply_message(
                event.reply_token,[
                TextSendMessage(text="恭喜抽中!: "),
                FlexSendMessage(_pricename,contents=_flex)
                ])
        return
    elif _command_check =="!create" or _command_check =="!c":
        if diceGame.checkGroupHasGame(group_id) is True:
            _inGamingRoom = diceGame.getGroupPlayingGame(group_id)
            _reply ="此群組已有房間 請先加入\n主持:"+_inGamingRoom["room_hoster"]
            try:
                _info = diceGame.getGameInfoStr(str(_inGamingRoom["room_id"]))
                _reply+=_info
            except:
                _reply+="\n房號:"+str(_inGamingRoom["room_id"])+"\n"
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=_reply))
            return
        user_id = event.source.user_id
        _reply = diceGame.createGame(user_id,group_id)

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=_reply),
            FlexSendMessage("下注囉",contents=lineMessagePacker.getDiceBetChoose()),
            FlexSendMessage("下注囉",contents=lineMessagePacker.getRollDiceFlex())])

    elif _command_check.startswith('!join') or _command_check.startswith('!j'):
        user_id = event.source.user_id
        content =  user_send.split(" ")
        try:
            bet_info = content[1]
            # if diceGame.checkGameIsExist(room_id) is False:
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text="請房間不存在! 請確定房號"))
            #     return
            if group_id != " ":
                if diceGame.checkGroupHasGame(group_id) is False:
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="此群組還沒開始遊戲喔! 請使用 !c or !create 開始遊戲"))
                    return
                else:
                    _room_id = diceGame.getGroupPlayingGame(group_id)["room_id"]
            else:
                try:
                    _room_id = diceGame.getRoomIdByUserId(event.source.user_id)
                    bet_info = content[1]
                except:
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="單人遊玩請輸入房號 謝謝"))
                    return
            bets = bet_info.split("&")
            _temp_money =0
            for bet_pair in bets:
                money = int(bet_pair.split(":")[1])
                if money < 0:
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="請勿輸入小於0的金額!"))
                    return
                else:
                    _temp_money+=money
            print("玩家總下注金額")
            print(_temp_money)
            if _temp_money > diceGame.checkPlayerMoney(user_id):
                print("下注金額過大 超出餘額 請重新下注")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="下注金額過大 超出餘額 請重新下注"))
                return
            profile = line_bot_api.get_profile(user_id)
            user_line_name = profile.display_name
            database.SetUserLockedMoneyByLineId(user_id,_temp_money)
            _reply = diceGame.joinGame(user_id,bet_info,str(_room_id),_temp_money)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="玩家:"+user_line_name+_reply))
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請使用格式 !join 房號 數字:金額 使用&區隔多個數字 ex 5:100&6:200"))
    elif _command_check.startswith('!room'):
        try:
            _roomid = user_send.split(" ")[1]
            reply = diceGame.getGameInfoStr(_roomid)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="好像沒有此資料喔"))
    elif _command_check =="!dice" or _command_check.startswith('!d'):
        user_id = event.source.user_id
        _reply = diceGame.StartGame(user_id)
        try:
            _dice = _reply.split("|")[0]
            _text = _reply.split("|")[1]
            line_bot_api.reply_message(
                event.reply_token,[
                FlexSendMessage("開獎囉!",contents=lineMessagePacker.getDiceResult(_dice)),
                TextSendMessage(text=_text)
                ])
        except:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=_reply))
    elif _command_check =="!rateinforofdicegame":
        line_bot_api.reply_message(
            event.reply_token,[
            FlexSendMessage("下注表!",contents=lineMessagePacker.getDiceBetChoose()),
            TextSendMessage(text="以上為下注種類")
            ])
    elif _command_check =="!info":
        user_id = event.source.user_id
        try:
            profile = line_bot_api.get_profile(user_id)
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="看來你沒有加我好友! 請先加我好友喔"))
        user_line_name = profile.display_name
        user_line_img = profile.picture_url
        if database.checkUser(user_id) is True:
            _userjson = database.getUser(user_id)
            _rank = database.getUserRank(user_id)
            flex_message = FlexSendMessage(
            alt_text='玩家資料來囉~',
            contents=lineMessagePacker.getInfoFlexJson(_userjson["user_line_name"],_userjson["user_type"],_userjson["user_img_link"],int(_userjson["user_money"]),int(_userjson["locked_money"]),_userjson["user_info_id"],_rank))
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:
            database.createUser(user_id,user_line_name,user_line_img)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已成功創建資料 可用 !info 查詢"))
    elif _command_check =="!gamelist":
        reply = diceGame.getRoomList()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
    elif _command_check =="!betlist":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("下注表來囉",contents=lineMessagePacker.getDiceBetChoose()))
    elif _command_check == "!rollhistory":
        _history = database.getDiceHistory()
        _parse = list(_history)
        _strtopackage = ""
        _index = 0
        _target = len(_parse)
        for history in _parse:
            _strtopackage+=history
            _index+=1
            if _index == _target:
                None
            else:
                _strtopackage+="-"
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("擲骰紀錄來囉",contents=lineMessagePacker.getDiceHistoryFlex(_strtopackage)))
    elif _command_check =="!watherprice":
        _jackpot = database.getAllJackpot()
        _jackpotjson ={"grand":_jackpot[0],"major":_jackpot[1],"minor":_jackpot[2],"mini":_jackpot[3],"last_winner":_jackpot[4],"last_win":_jackpot[5]}
        line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage("目前彩金!",contents=lineMessagePacker.getJackPotFlex(_jackpotjson)))
    elif _command_check.startswith("!spin"):
        try:
            _times = int(_command_check.split(" ")[1])
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="輸入格式好像有問題喔... !spin 次數"))
            return
        if _times < 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="轉負數次數是怎樣...?"))
            return
        user_id = event.source.user_id
        if int(database.getUserMoney(user_id)) < 100*_times:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="餘額小於 次數*100 無法進行"))
            return
        #_result = diceGame.StartSpinGame(user_id)
        _totalbet = 100*_times
        _result = jpGame.spinJp(_totalbet,user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_result))
    #回傳價格表
    elif user_send == "!price":
        price = apiThread.getPrice()
        _reply=""
        for symbol in price:
            _reply+= symbol+" : "+price[symbol]+"\n"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    #訂閱交易對
    elif user_send.startswith('!subscribe'):
        _symbol = user_send.split("!subscribe")[1].upper()
        _reply = apiThread.subScribe(_symbol+"USDT")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    #移除訂閱交易對
    elif user_send.startswith('!unsubscribe'):
        _symbol = user_send.split("!unsubscribe")[1].upper()
        _reply = apiThread.unSubScribe(_symbol+"USDT")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    #獲得目前交易對
    elif user_send == '!list':
        _reply = apiThread.getSubscribeList()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    elif user_send == '!help':
        print("send")
        line_bot_api.reply_message(
        event.reply_token,[
        FlexSendMessage("幫助",contents=lineMessagePacker.getHelpFlex()),
        ])
    else:
        None


if __name__ == "__main__":
    apiThread = bybitApi.BybitApi("apithread")
    apiThread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    if environment =="DEV":
        app.run(host='0.0.0.0', port=port,debug=True)
    else:
        app.run(host='0.0.0.0', port=port)
    