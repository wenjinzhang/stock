from django.shortcuts import render
from app.models import StockInfo, Stock


# Create your views here.
# register scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

try:
    # init scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    # run 8:30  every day
    @register_job(scheduler, 'cron', id='load_daily_stock_info', hour=12, minute=00)
    def test():

        print("................Now it is running")

    register_events(scheduler)
    scheduler.start()
    

except Exception as e:
    
    scheduler.shutdown()
