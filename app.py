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
    if user_send =="!create":
        user_id = event.source.user_id
        _reply = diceGame.createGame(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    if user_send.startswith('!join'):
        user_id = event.source.user_id
        content =  user_send.split(" ")
        try:
            room_id = content[1]
            bet_info = content[2]
            if diceGame.checkGameIsExist(room_id) is False:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請房間不存在! 請確定房號"))
                return
            profile = line_bot_api.get_profile(user_id)
            user_line_name = profile.display_name
            _reply = diceGame.joinGame(user_id,bet_info,room_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="玩家:"+user_line_name+_reply))
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請使用格式 !join 房號 數字:金額 使用&區隔多個數字 ex 5:100&6:200"))
    if user_send.startswith('!room'):
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
    if user_send =="!dice":
        user_id = event.source.user_id
        _reply = diceGame.StartGame(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    if user_send =="!info":
        user_id = event.source.user_id
        profile = line_bot_api.get_profile(user_id)
        user_line_name = profile.display_name
        user_line_img = profile.picture_url
        if database.checkUser(user_id) is True:
            _userjson = database.getUser(user_id)
            flex_message = FlexSendMessage(
            alt_text='玩家資料來囉~',
            contents=lineMessagePacker.getInfoFlexJson(_userjson["user_line_name"],_userjson["user_img_link"],_userjson["user_money"],_userjson["locked_money"]))
            line_bot_api.reply_message(event.reply_token, flex_message)
        else:
            database.createUser(user_id,user_line_name,user_line_img)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已成功創建資料 可用 !info 查詢"))
       
    #回傳價格表
    elif user_send == "!price":
        price = apiThread.getPrice()
        str=""
        for symbol in price:
            str+= symbol+" : "+price[symbol]+"\n"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str))
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
        str=""
        list = database.getCommandList()
        for command in list:
            str+=command+"\n"+list[command][0]+"\n"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str))
    else:
        None


if __name__ == "__main__":
    apiThread = bybitApi.BybitApi("apithread")
    apiThread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    