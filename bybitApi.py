from asyncio.log import logger
from BybitWebsocket import BybitWebsocket
from threading import Thread
import time
from pybit import HTTP, WebSocket
from dotenv import load_dotenv
import os
load_dotenv()
class BybitApi(Thread):
    def __init__(self, name):
        super(BybitApi, self).__init__()  # 重構run函式必須要寫
        self.subscribeSymbolList=["BTCUSDT","BITUSDT"]
        self.priceList={}
        self.allSymbolList=[]
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
        #init all symbol
        print("get all legal symbol ...")
        _allsymbol = self.session.query_symbol()['result']
        for _sym in _allsymbol:
            self.allSymbolList.append(_sym['name'])
        print(self.allSymbolList)
    
    def subScribe(self,symbol):
        symbol = symbol.replace(" ","")
        if symbol in self.subscribeSymbolList:
            print("此交易對已存在訂閱")
            return "此交易對已存在訂閱目錄"
        else:
            if symbol in self.allSymbolList:
                self.subscribeSymbolList.append(symbol)
                #print("訂閱:"+symbol+"\n"+"目前訂閱目錄:")
                _str = "訂閱:"+symbol+"成功!\n"+"目前訂閱目錄:\n"
                for item in self.subscribeSymbolList:
                    _str+=item+"\n"
                return _str
            else:
                _str = "此交易對不存在 請確定輸入內容"
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
            try:
                _price = self.session.last_traded_price(symbol=item)['result']['price']
                self.priceList[item] = _price
            except:
                self.priceList[item] = "此交易對沒有現貨資料 可使用!unsubscribe "+item+" 來移除訂閱!"
        print("price:")
        print(self.priceList)
        return self.priceList        
