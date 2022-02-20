from asyncio.log import logger
from BybitWebsocket import BybitWebsocket
from threading import Thread
import time
from pybit import HTTP, WebSocket
from dotenv import load_dotenv
import os
load_dotenv()
class MyThread(Thread):
    def __init__(self, name):
        super(MyThread, self).__init__()  # 重構run函式必須要寫
        self.subscribeSymbolList=["BTCUSDT","BITUSDT"]
        self.priceList={}
        self.name = name
        self.initWebSocket()
    
    def initWebSocket(self):
        self.session = HTTP(
            endpoint='https://api.bybit.com', 
            api_key=os.getenv("BY_BIT_API_KEY"),
            api_secret=os.getenv("BY_BIT_API_SECRET")
        )
        self.ws = WebSocket(
            endpoint='wss://stream.bybit.com/realtime', 
            subscriptions=['order', 'position'], 
            api_key=os.getenv("BY_BIT_API_KEY"),
            api_secret=os.getenv("BY_BIT_API_SECRET")
        )

    def run(self):
        # while True:
        #     #print("list:")
        #     #print(self.subscribeSymbolList)
        #     for subscribeSymbol in self.subscribeSymbolList:
        #         _str = "instrument_info.100ms."+subscribeSymbol
        #         #print("find data:"+_str)
        #         data = self.ws.get_data(_str)
        #         #print("交易對:"+subscribeSymbol+"結果:")
        #         print(data)
        #         if len(data) != 0:
        #             try:
        #                 price_data = data['update'][0]
        #                 #print(price_data['last_price'])
        #                 price = price_data['last_price']
        #                 self.priceList[subscribeSymbol] = price
        #                 print(self.priceList)
        #             except:
        #                 None
        #         else:
        #             None
        #             #print("交易對:"+subscribeSymbol+"還未有新價格")
        #             #print(data)
        #     time.sleep(1)
        print("start")
    
    def subScribe(self,symbol):
        symbol = symbol.replace(" ","")
        if symbol in self.subscribeSymbolList:
            print("此交易對已存在訂閱")
            return "此交易對已存在訂閱目錄"
        else:
            self.subscribeSymbolList.append(symbol)
            #print("訂閱:"+symbol+"\n"+"目前訂閱目錄:")
            _str = "訂閱:"+symbol+"成功!\n"+"目前訂閱目錄:\n"
            for item in self.subscribeSymbolList:
                _str+=item+"\n"
            return _str
    
    def unSubScribe(self,symbol):
        symbol = symbol.replace(" ","")
        try:
            del self.priceList[symbol]
        except:
            print("")
        try:
            index = self.subscribeSymbolList.index(symbol)
            del self.subscribeSymbolList[index]
            _str = "移除訂閱:"+symbol+"\n"+"目前訂閱目錄:\n"
            for item in self.subscribeSymbolList:
                _str+=item+"\n"
            return _str
        except:
            print("無訂閱此貨幣")
            return "無訂閱此貨幣"


    def getSubscribeList(self):
        _str = "目前訂閱目錄:\n"
        for item in self.subscribeSymbolList:
            _str+=item+"\n"
        return _str


    def getPrice(self):
        
        for item in self.subscribeSymbolList:
            self.priceList[item] = self.session.last_traded_price(symbol=item)['result']['price']
        print("price:")
        print(self.priceList)
        return self.priceList        
