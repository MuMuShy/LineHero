import math
import random
from unittest import result
def test(player_money):
    wather_money = 1000000
    _isjp = False
    if wather_money > 1000:
        _resultlist =['jp','none']
        _result = random.choices(_resultlist,weights=[1,1000])[0]
        if _result == 'jp':
            print("jp!")
            player_money = wather_money
            return player_money
        else:
            _resultlist =['loose','little','middle','big']
            _result = random.choices(_resultlist,weights=[51,47,1,1])[0]
            print(_result)
            if _result =='loose':
                _rtp = random.randrange(80,89)/100
            elif _result =='little': #105%~ 110%
                _rtp = random.randrange(105,110)/100
            elif _result =='middle': #150~200
                _rtp = random.randrange(150,200)/100
            elif _result =='big': #20%~30%的彩池
                _present = random.randrange(20,30)
                _win = int(wather_money*_present/100)
                _rtp = _win/player_money
            print("result:"+_result)
            print("rtp:"+str(_rtp))
            player_money*=_rtp
            player_money = math.ceil(player_money)
            print(player_money)
    else:
        _resultlist =['loose','little','middle']
        _result = random.choices(_resultlist,weights=[51,47,1])[0]
        print(_result)
        if _result =='loose':
            _rtp = random.randrange(90,97)
        elif _result =='little': #105%~ 110%
            _rtp = random.randrange(105,110)
        elif _result =='middle': #150~200
            _rtp = random.randrange(150,200)
        print("result:"+_result)
        print("rtp:"+str(_rtp))
        player_money*=_rtp
        player_money = int(player_money)
        print(player_money)
    return player_money
    

if __name__ == "__main__":
    #print(test(20))
    _win = 0
    _loose =0
    for i in range(10000):
        _result = test(10)
        if _result > 10:
            _win+=1
        else:
            _loose+=1

    print("w:"+str(_win))
    print("l:"+str(_loose))