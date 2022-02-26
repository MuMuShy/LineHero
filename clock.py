from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun',hour='0')
def scheduled_job():
    print("12.00過後每日任務重置")
    url = "https://bybitline.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()