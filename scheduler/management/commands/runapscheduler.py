import logging

from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from app.models import Stock, StockInfo, PredictPrice
import yfinance as yf
from tqdm import tqdm
from django.utils.timezone import make_aware
from pandas import Timestamp

from scheduler.ml.train_regression_model import predict, train_model, train


logger = logging.getLogger(__name__)

def load_daily_stock_info():
    stocks = Stock.objects.all()
    for stock in stocks:
        print(stock.symbol)
        data = yf.download(stock.symbol, period="2d", interval="1d")
        for pdtimestamp, price_dict in tqdm(data.to_dict('index').items()):
            timestamp = Timestamp(pdtimestamp, tz='UTC')
            stockInfo = StockInfo(
                id="{}_{}".format(timestamp, stock.symbol),
                open_price=price_dict['Open'],
                high_price=price_dict['High'],
                low_price=price_dict['Low'],
                close_price=price_dict['Close'],
                adj_close_price=price_dict['Adj Close'],
                volume=price_dict['Volume'],
                date=timestamp
            )

            stockInfo.stock = stock
            stockInfo.save()

def download_or_update_last_3year_stock_info():
    stocks = Stock.objects.all()
    for stock in stocks:
        print(stock.symbol)
        data = yf.download(stock.symbol, period="3y", interval="1d")
        for pdtimestamp, price_dict in tqdm(data.to_dict('index').items()):
            timestamp = Timestamp(pdtimestamp, tz='UTC')
            stockInfo = StockInfo(
                id="{}_{}".format(timestamp, stock.symbol),
                open_price=price_dict['Open'],
                high_price=price_dict['High'],
                low_price=price_dict['Low'],
                close_price=price_dict['Close'],
                adj_close_price=price_dict['Adj Close'],
                volume=price_dict['Volume'],
                date=timestamp
            )

            stockInfo.stock = stock
            stockInfo.save()

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def predict_next_5days():
    model_types =["RNN", "LSTM"]
    stocks = Stock.objects.all()
    for stock in stocks:
        for model_type in model_types:
            next5days = predict(stock.symbol, model_type)
            for day in next5days:
                print(day)
                timestamp = str(day[0])
                predictPrice = PredictPrice(
                    id="{}_{}_{}".format(timestamp, stock.symbol, model_type),
                    model_type = model_type,
                    price = float(day[1]),
                    date = Timestamp(timestamp, tz='UTC')
                )
                predictPrice.stock = stock
                predictPrice.save()


def test_task():
    print("the task has been called")

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            test_task,
            trigger=CronTrigger(second="*/10"),  # Every 
            id="test_task",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'test_job'.")

        scheduler.add_job(
            load_daily_stock_info,
            trigger=CronTrigger(hour=23, minute=59),  # Every 
            id="load_daily_stock_price",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            predict_next_5days,
            trigger=CronTrigger(hour=23, minute=59),  # Every 
            id="predict_next_5days",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added Job: predict_next_5days")


        scheduler.add_job(
            download_or_update_last_3year_stock_info,
            trigger=CronTrigger(
                month="12", day="31", hour="00", minute="00"
            ),  # Midnight on the last of the December, before start of the next work week.
            id="download_or_update_last_3year_stock_info",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added yearly job: 'download_or_update_last_3year_stock_info'."
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
