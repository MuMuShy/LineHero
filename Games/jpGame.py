import sys
from unittest import result
sys.path.insert(0, '../')
import random
import math
from DataBase import DataBase
dataBase = DataBase()
def spinJp(betmoney,user_line_id):
    _origin = int(dataBase.getUserMoney(user_line_id))
    _origin-=betmoney #先把下注的錢扣掉
    _beforeBet = _origin
    #betmoney使用這那邊會先扣掉 所以回傳的money要示小於當初投入 等於使用者虧錢
    #進彩池機率 每分 0.00001
    _jpPersent = 0.00001 
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
    _inToJp = _jpPersent*betmoney
    print("投入金額:"+str(betmoney)+" 次數:"+str(betmoney/_oneTimeBet)+" 進彩池機率:"+str(_inToJp*100)+"%")
    _result = {}
    _payoff=0
    if _inToJp >= 1:
        print("進入彩池!")
        _nowJp = dataBase.getAllJackpot()
        _grand = _nowJp[0]
        _major = _nowJp[1]
        _minor = _nowJp[2]
        _mini = _nowJp[3]
        _username = dataBase.getUserName(user_line_id)
        _money = 0
        _resultlist =['grand','major','minor','mini']
        _result = random.choices(_resultlist,weights=[_grandweight,_majorweight,_minorweight,_miniweight])[0]
        print("彩池獲得:"+_result)
        if _result =='grand':
            print("Grand!")
            _money = dataBase.getGrand()
            dataBase.setGrand(10000000)
            _result={"type":"grand","money":_money}
        elif _result == 'major':
            print("Major!!")
            _money = dataBase.getMajor()
            dataBase.setMajor(1000000)
            _result={"type":"major","money":_money}
        elif _result =='minor':
            print("minor!!")
            _money = dataBase.getMinor()
            dataBase.setMinor(100000)
            _result={"type":"minor","money":_money}
        elif _result =='mini':
            print("mini!")
            _money = dataBase.getMini()
            dataBase.setMini(10000)
            _result={"type":"mini","money":_money}
        #更新資料庫
        dataBase.setJpLastWin(_username,_money)
    else:
        print("沒進彩池 正常派獎")
        _rtp = random.randrange(85,110)/100
        if _rtp == 100:
            _rtp = 98
        print("RTP: "+str(_rtp))
        _money = int(_origin*_rtp)
        _result={"type":"normal","money":_money}

    _payoff = _origin + _money
    dataBase.SetUserMoneyByLineId(user_line_id,_payoff)

    #解析回傳
    _returnstr="投入金額:"+str(betmoney)+" 次數:"+str(betmoney/_oneTimeBet)
    _payoff = _result["money"]  
    _payoff = int(_payoff) 
    if _result["type"] == "grand":
        _returnstr+="\n恭喜中GRAND!! :"+str("${:,.2f}".format(_result["money"]))
        print("中grand!"+str(_result["money"]))
    elif _result["type"] == "major":
        _returnstr+="\n恭喜中MAJOR!! :"+str("${:,.2f}".format(_result["money"]))
        print("major!"+str(_result["money"]))
    elif _result["type"] == "minor":
        _returnstr+="\n恭喜中MINOR!! :"+str("${:,.2f}".format(_result["money"]))
        print("中minor!"+str(_result["money"]))
    elif _result["type"] == "mini":
        _returnstr+="\n恭喜中MINI!! :"+str("${:,.2f}".format(_result["money"]))
        print("中mini!"+str("${:,.2f}".format(_result["money"])))
    elif _result["type"] == "normal":
        _payoff = int(_payoff)
    if _payoff < _beforeBet:
        _loose = _origin-_payoff
        _returnstr+="\n虧損:"+str("${:,.2f}".format(_loose))+"\n餘額: "+str("${:,.2f}".format(_payoff))
        print("增加水錢:"+str(_loose))
        dataBase.addWatherMoney(_loose)
        dataBase.addAllJp(int(_loose*0.5),int(_loose*0.3),int(_loose*0.05),int(_loose*0.03))
        print("輸 :"+str(_loose)+"餘額:"+str(_payoff))
    else:
        _win = _payoff-_origin
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
        