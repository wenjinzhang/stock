from django.shortcuts import render


# Create your views here.
# register scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from app.models import Stock, StockInfo

import yfinance as yf
from tqdm import tqdm
from django.utils.timezone import make_aware
from pandas import Timestamp

try:
    # init scheduler
    # scheduler = BackgroundScheduler()
    # scheduler.add_jobstore(DjangoJobStore(), 'default')

    # # run 12:00pm  every day
    # @register_job(scheduler, 'cron', id='load_daily_stock_info', hour=12, minute=00)
    # def load_daily_stock_info():
    #     stocks = Stock.objects.all()
    #     print(stocks)
    #     for stock in stocks:
    #         print(stock.symbol)
    #         data = yf.download(stock.symbol, period = "3y", interval = "1d")
    #         for pdtimestamp, price_dict in tqdm(data.to_dict('index').items()):
    #             timestamp = Timestamp(pdtimestamp, tz = 'UTC')
    #             stockInfo = StockInfo(
    #                         id = "{}_{}".format(timestamp, stock.symbol),
    #                         open_price = price_dict['Open'],
    #                         high_price = price_dict['High'],
    #                         low_price = price_dict['Low'],
    #                         close_price = price_dict['Close'],
    #                         adj_close_price = price_dict['Adj Close'],
    #                         volume = price_dict['Volume'],
    #                         date = timestamp
    #                         )

    #             stockInfo.stock = stock
    #             stockInfo.save()
    #     print("................Now it is running")
    # register_events(scheduler)
    # scheduler.start()
    pass

except Exception as e:
    scheduler.shutdown()
