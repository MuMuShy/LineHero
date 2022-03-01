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
                _weapon = database.getWeaponInfo(_jobjson["weapon"])
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
    elif user_send == "@jobinfo":
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
        _weapon = database.getWeaponInfo(_jobjson["weapon"])
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
        #先未開放
        _user_weapon = database.getUserJob(event.source.user_id)["weapon"]
        print(_user_weapon)
        _weaponjson = database.getWeaponInfo(_user_weapon)
        _flex_equipment = lineMessagePackerRpg.getEquipmentNow(_weaponjson)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("裝備列表",contents=_flex_equipment))
        return
    elif user_send =="@skill":
        _status = database.getUserJob(event.source.user_id)
        _skillflex = lineMessagePackerRpg.getSkillList(_status)
        #先未開放
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("玩家技能",contents=_skillflex))
        return
    elif user_send =="@bag":
        #先未開放
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="敬請期待..."))
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
            line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text=_result["reply_text"]),
                    FlexSendMessage("遭遇怪物!",contents=_flex)
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
        if _money - 5000 < 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="沒錢還敢補血啊...."))
            return
        _money-=5000
        _user_job = database.getUserJob(event.source.user_id)
        _maxhp = rpgGame.getMaxHp(_user_job["job"],_user_job["level"])
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
                _strtext = "遭到怪物攻擊:"+ str(_game_result_json["mosnter_damage"]) +" 玩家剩餘血量:"+ str(_game_result_json["player_result_json"]["hp"])
                line_bot_api.reply_message(
                    event.reply_token,[
                    FlexSendMessage("攻擊!",contents=_attackbtnFlex),
                    TextSendMessage(text = _str_skill_text),
                    FlexSendMessage("怪物存活!",contents=_monsterFlex),
                    FlexSendMessage("怪物存活" ,contents= _lastFlex),])
            elif _game_result_json["Result"] =="win":
                _attackbtnFlex = lineMessagePackerRpg.getAttackButton(_game_result_json["player_damage"],_game_result_json)
                _strtext ="戰鬥勝利! 獲得 exp:"+str(_game_result_json["monster_result_json"]["exp"])+ "金幣:" + str(_game_result_json["get_money"])+"\n"+"剩餘血量:"+str(_game_result_json["player_result_json"]["hp"])+"/"+str(rpgGame.getMaxHp(_game_result_json["player_result_json"]["job"],_game_result_json["player_result_json"]["level"]))
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
    