import time
from datetime import datetime, timedelta
import random
# t1 = time.localtime()
# current =  datetime.now()
# print(current)
# strtodatabase = (current.strftime("%m/%d/%Y, %H:%M:%S"))
# print(type(strtodatabase))
# fromdatabase = datetime.strptime(strtodatabase,"%m/%d/%Y, %H:%M:%S")
# print(fromdatabase)
# target =current+ timedelta(minutes=5)
# print(target)

# time_elapsed = (target-current)
# print(time_elapsed.total_seconds())

wather_money = 10000
bet = 10
_present = random.randrange(20,30)

print(_present)
_win = int(wather_money*_present/100)
print(_win)
_rtp = _win/bet
print(_rtp)
print(bet*_rtp)