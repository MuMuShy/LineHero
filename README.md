# CryptoLineBot

**串接bybitapi的line機器人**


![markdown](https://mumu.tw/images/bybitbotimage.jpg "bybitbot")


加密貨幣機器人是一個使用python撰寫的Line bot,使用message api還有bybit api進行功能上的串接,目前提供了實時價格,訂閱表,等功能.


## 如何開發

*如果需要進行開發需要:
1.申請LINE DEVELOPER帳號,並且創建MESSAGE API機器人.
詳情可查詢官方文件: https://developers.line.biz/zh-hant/services/messaging-api/*
2.申請BYBIT帳號並啟用API.
可查詢: https://bybit-exchange.github.io/docs/spot/#t-introduction

> 此專案單純為開發學習使用,無任何商業用途。


### 配置開發環境

#### 安裝依賴項目


`pip install -r requirements.txt`
####創建.env檔案 並配置:
LINE_BOT_API_DEV = 你的linebot api key
LINE_BOT_SECRET_DEV = 你的linebot Channel secret
BY_BIT_API_KEY = 你的bybit api key
BY_BIT_API_SECRET = 你的bybit api secret
ENVIRONMENT=DEV`

#### 運行app.py

> 本地端需使用ngrok進行倒轉並填入line bot的webhook url
