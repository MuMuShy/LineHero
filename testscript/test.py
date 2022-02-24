import time
from datetime import datetime, timedelta
t1 = time.localtime()
current =  datetime.now()
print(current)
strtodatabase = (current.strftime("%m/%d/%Y, %H:%M:%S"))
print(type(strtodatabase))
fromdatabase = datetime.strptime(strtodatabase,"%m/%d/%Y, %H:%M:%S")
print(fromdatabase)
target =current+ timedelta(minutes=5)
print(target)

time_elapsed = (target-current)
print(time_elapsed.total_seconds())

s="!spin"
print(int(s.split(" ")[1]))