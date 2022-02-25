import time
from datetime import datetime, timedelta
import random
t1 = time.localtime()
current =  datetime.now()
print(current)
strtodatabase = (current.strftime("%m/%d/%Y %H:%M:%S"))
print("!"+strtodatabase)
fromdatabase = datetime.strptime(strtodatabase,"%m/%d/%Y %H:%M:%S")
print(fromdatabase)
target =current+ timedelta(minutes=5)
print(target)

time_elapsed = (target-current)
print(time_elapsed.total_seconds())

a = 100
b = 0.9
print(int(a*b))

