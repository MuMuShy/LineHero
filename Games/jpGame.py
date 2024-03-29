import sys
from unittest import result
sys.path.insert(0, '../')
import random
import math
from DataBase import DataBase
dataBase = DataBase()
def spinJp(betmoney,user_line_id):
    _origin = int(dataBase.getUserMoney(user_line_id))
    _beforeBet = _origin
    _origin-=betmoney #先把下注的錢扣掉
    
    #betmoney使用這那邊會先扣掉 所以回傳的money要示小於當初投入 等於使用者虧錢
    #進彩池機率 每分 0.00001
    _jpPersent = 0.000001 
    #Grand中獎率 -> 0.005 起始金額: 1000萬
    _grandweight = 5
    #major中獎率 -> 0.02    起始金額: 100萬
    _majorweight = 20
    #minor中獎率 -> 0.2 起始金額: 10萬
    _minorweight = 200
    #mini中獎率 -> 0.7  起始金額: 1萬
    _miniweight = 700
    #rtp -> 90 ~ 110
    #假設一次固定 100塊錢
    _oneTimeBet = 100
    _playtime = int(betmoney/_oneTimeBet)
    _inToJp = _jpPersent*betmoney*100
    print("完之前的金額:"+str(_beforeBet))
    print("投入金額:"+str(betmoney)+" 次數:"+str(betmoney/_oneTimeBet)+" 進彩池機率:"+str(_inToJp)+"%")
    _result = {}
    _payoff=0
    _nointojp = 100-_inToJp
    if _nointojp <0:
        _nointojp*=-1
    print("weight in/no:"+str(_inToJp)+"/"+str(_nointojp))
    check = ['injp','notinjp']
    _checkintojp = random.choices(check,weights=[_inToJp,_nointojp])[0]
    print("彩池確認結果:"+_checkintojp)
    if _checkintojp == 'injp':
        print("進入彩池!")
        _nowJp = dataBase.getAllJackpot()
        _grand = _nowJp[0]
        _major = _nowJp[1]
        _minor = _nowJp[2]
        _mini = _nowJp[3]
        if _mini > 30000:
            _miniweight = _miniweight*2
        if _minor > 190000:
            _minorweight = _minorweight*2 
        if _major < 2000000:
            _majorweight = 0
        if _grand < 20000000:
            _grandweight = 0
        _username = dataBase.getUserName(user_line_id)
        _money = 0
        _resultlist =['grand','major','minor','mini']
        _result = random.choices(_resultlist,weights=[_grandweight,_majorweight,_minorweight,_miniweight])[0]
        print("彩池獲得:"+_result)
        if _result =='grand':
            print("Grand!")
            _money = dataBase.getGrand()
            #更新資料庫
            dataBase.setJpLastWin(_username,_money)
            dataBase.setGrand(10000000)
            _result={"type":"grand","jp":_money}
        elif _result == 'major':
            print("Major!!")
            _money = dataBase.getMajor()
            #更新資料庫
            dataBase.setJpLastWin(_username,_money)
            dataBase.setMajor(1000000)
            _result={"type":"major","jp":_money}
        elif _result =='minor':
            print("minor!!")
            _money = dataBase.getMinor()
            #更新資料庫
            dataBase.setJpLastWin(_username,_money)
            dataBase.setMinor(100000)
            _result={"type":"minor","jp":_money}
        elif _result =='mini':
            print("mini!")
            _money = dataBase.getMini()
            #更新資料庫
            dataBase.setJpLastWin(_username,_money)
            dataBase.setMini(10000)
            _temp = 0
            _result={"type":"mini","jp":_money}
            for i in range(_playtime):
                _rtp = random.randrange(60,120)
                _temp+=_rtp
            _money+=_temp
            

    else:
        print("沒進彩池 正常派獎")
        _temp = 0
        for i in range(_playtime):
            _rtp = random.randrange(60,140)
            _temp+=_rtp
        print("RTP: "+str(_temp/_oneTimeBet*_playtime))
        _money = int(_temp)
        print("派的錢:"+str(_money))
        _result={"type":"normal","money":_money}

    _payoff = _origin + _money
    print("payoff:"+str(_payoff))
    dataBase.SetUserMoneyByLineId(user_line_id,_payoff)

    #解析回傳
    _returnstr="投入金額:"+str(betmoney)+" 次數:"+str(betmoney/_oneTimeBet) 
    _payoff = int(_payoff) 
    if _result["type"] == "grand":
        _returnstr+="\n恭喜中GRAND!! :"+str("${:,.2f}".format(_result["jp"]))
        print("中grand!"+str(_payoff))
    elif _result["type"] == "major":
        _returnstr+="\n恭喜中MAJOR!! :"+str("${:,.2f}".format(_result["jp"]))
        print("major!"+str(_payoff))
    elif _result["type"] == "minor":
        _returnstr+="\n恭喜中MINOR!! :"+str("${:,.2f}".format(_result["jp"]))
        print("中minor!"+str(_payoff))
    elif _result["type"] == "mini":
        _returnstr+="\n恭喜中MINI!! :"+str("${:,.2f}".format(_result["jp"]))
        print("中mini!"+str("${:,.2f}".format(_payoff)))
    if _result["type"] !="normal" and _playtime>1:
        _returnstr+="\n其餘旋轉次數獎項總計:(總得分-總投入)"
    elif _result["type"] == "normal":
        _payoff = int(_payoff)
    if _payoff < _beforeBet:
        _loose = _beforeBet-_payoff
        _returnstr+="\n虧損:"+str("${:,.2f}".format(_loose))+"\n餘額: "+str("${:,.2f}".format(_payoff))
        print("增加水錢:"+str(_loose))
        dataBase.addWatherMoney(_loose)
        dataBase.addAllJp(int(_loose*0.5),int(_loose*0.3),int(_loose*0.05),int(_loose*0.03))
        print("輸 :"+str(_loose)+"餘額:"+str(_payoff))
    else:
        _win = _payoff-_beforeBet
        _returnstr+="\n贏得:"+str("${:,.2f}".format(_win))+"\n餘額"+str("${:,.2f}".format(_payoff))
        print("贏:"+str(_win)+"餘額:"+str(_payoff))
    return _returnstr


if __name__ == "__main__":
    _spintime = 10000
    _spent = _spintime*100
    dataBase.setGrand(12345655)
    dataBase.setMajor(789798)
    dataBase.setMinor(11111)
    dataBase.setMini(11111)
    print(dataBase.getAllJackpot())
    _result = spinJp(_spent)
    if _result["type"] == "grand":
        print("中grand!"+str(_result["money"]))
    elif _result["type"] == "major":
        print("major!"+str(_result["money"]))
    elif _result["type"] == "minor":
        print("中minor!"+str(_result["money"]))
    elif _result["type"] == "mini":
        print("中mini!"+str(_result["money"]))
    elif _result["type"] == "normal":
        if int(_result["money"]) > _result:
            print("輸 餘額:"+_result["money"])
        else:
            print("贏 餘額:"+_result["money"])
    dataBase.setJpLastWin("Lanlin",14564444)
    print(dataBase.getAllJackpot())
    dataBase.setAllJackpot(10000000,1000000,100000,10000)
    print(dataBase.getAllJackpot())
    dataBase.addAllJp(123,123,123,123)
    print(dataBase.getAllJackpot())
        