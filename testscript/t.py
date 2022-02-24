import random
from unittest import result
def test(player_money,time=1):
    wather_money = 100000
    playermone = 1000
    cost = 10*time
    _isjp = False
    
    if wather_money > 1000:
        _resultlist =['jp','none']
        _result = random.choices(_resultlist,weights=[1,1000])[0]
        if _result == 'jp':
            print("jp!")
            return
        else:
            _resultlist =['loose','little','middle','big']
            _result = random.choices(_resultlist,weights=[51,47,1,1])[0]
            print(_result)
            if result =='loose':
                player_money-=10*time
            elif result =='little':
                None

if __name__ == "__main__":
    #print(test(20))
    test(1,1)