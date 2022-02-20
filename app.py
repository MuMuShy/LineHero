import threading
from time import sleep
from flask import Flask, request, abort
from dotenv import load_dotenv

from DataBase import DataBase
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_send =event.message.text
    if user_send =="!info":
        user_id = event.source.user_id
        profile = line_bot_api.get_profile(user_id)
        user_line_name = profile.display_name
        user_line_img = profile.picture_url
        if database.checkUser(user_id) is True:
            _userjson = database.getUser(user_id)
            str = "名稱:"+_userjson["user_line_name"]+"\n圖片:"+_userjson["user_img_link"]+"\n金錢:"+_userjson["user_money"]
            flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": _userjson["user_img_link"],
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                    "type": "uri",
                    "uri": "http://linecorp.com/"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": _userjson["user_line_name"],
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "金錢",
                                "color": "#aaaaaa",
                                "size": "sm",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": _userjson["user_money"],
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }
                        
                        ]
                    }
                    ]
                }
            })
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
        _reply="指令\n!price : 獲得訂閱交易對最新價格\n!subscribe 交易對(大寫英文 ex. !subscribe BTC):訂閱交易對\n!unsubscribe交易對(大寫英文 ex. !unsubscribe BTC):取消訂閱交易對\n!list:列出交易對"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=_reply))
    else:
        None


if __name__ == "__main__":
    apiThread = bybitApi.BybitApi("apithread")
    apiThread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    