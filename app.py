import threading
from time import sleep
from flask import Flask, request, abort
from flask import render_template
from dotenv import load_dotenv
import lineMessagePacker
from DataBase import DataBase
from Games import diceGame
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
    user_send =event.message.text
    group_id =" "
    try:
        group_id =event.source.group_id
    except:
        group_id =" "
        print("no group")
    print(user_send)
    if user_send =="!dev":
        diceGame.checkGroupHasGame(group_id)
    if user_send.startswith("!set"):
        if event.source.user_id != os.getenv("GM_LINE_ID"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無權限執行此指令"))
            return
        try:
            _user_id = user_send.split(" ")[1]
            _money = user_send.split(" ")[2]
            database.AddUserMoneyByIndex(_user_id,_money)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="成功到賬!"))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="錯誤 請確認id等資料"))
            return
    if user_send.strip().startswith("!"):
        _command_check = "!"+user_send.strip().split("!")[1].strip().lower()
    else:
        _command_check = user_send
    if _command_check =="!create" or _command_check =="!c":
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
            TextSendMessage(text=_reply))

    if _command_check.startswith('!join') or _command_check.startswith('!j'):
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
                    _room_id = content[1]
                    bet_info = content[2]
                except:
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="單人遊玩請輸入房號 謝謝"))
                    return
            bets = bet_info.split("&")
            _temp_money =0
            for bet_pair in bets:
                money = int(bet_pair.split(":")[1])
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
            _reply = diceGame.joinGame(user_id,bet_info,str(_room_id),_temp_money)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="玩家:"+user_line_name+_reply))
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請使用格式 !join 房號 數字:金額 使用&區隔多個數字 ex 5:100&6:200"))
    if _command_check.startswith('!room') or _command_check.startswith('!r'):
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
    if _command_check =="!dice" or _command_check.startswith('!d'):
        user_id = event.source.user_id
        _reply = diceGame.StartGame(user_id)
        _dice = _reply.split("|")[0]
        _text = _reply.split("|")[1]
        line_bot_api.reply_message(
            event.reply_token,[
            FlexSendMessage("開獎囉!",contents=lineMessagePacker.getDiceResult(_dice)),
            TextSendMessage(text=_text)
            ])
    if _command_check =="!info":
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
            flex_message = FlexSendMessage(
            alt_text='玩家資料來囉~',
            contents=lineMessagePacker.getInfoFlexJson(_userjson["user_line_name"],_userjson["user_img_link"],_userjson["user_money"],_userjson["locked_money"],_userjson["user_info_id"]))
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:
            database.createUser(user_id,user_line_name,user_line_img)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已成功創建資料 可用 !info 查詢"))
    if _command_check =="!gamelist":
        reply = diceGame.getRoomList()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
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
    