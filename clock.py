from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun',hour='0')
def scheduled_job():
    from DataBase import DataBase
    dataBase = DataBase()
    print("12.00過後每日任務重置")
    dataBase.clearDailyRequest


sched.start()