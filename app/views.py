from django.shortcuts import render
import yfinance as yf
from .models import Stock, StockInfo, PredictPrice
from django.utils.timezone import make_aware
from pandas import Timestamp
import json
#

# Create your views here.
def test(request):
    stocks = Stock.objects.all()
    print(stocks)
    for stock in stocks:
        print(stock.symbol)
        data = yf.download(stock.symbol, period = "3y", interval = "1d")
        for pdtimestamp, price_dict in data.to_dict('index').items():
            timestamp = Timestamp(pdtimestamp, tz = 'UTC')
            stockInfo = StockInfo(
                        id = "{}_{}".format(timestamp, stock.symbol),
                        open_price = price_dict['Open'],
                        high_price = price_dict['High'],
                        low_price = price_dict['Low'],
                        close_price = price_dict['Close'],
                        adj_close_price = price_dict['Adj Close'],
                        volume = price_dict['Volume'],
                        date = timestamp
                        )
            stockInfo.stock = stock
            stockInfo.save()

    data = yf.download("ES=F", period = "5d", interval = "1d")
    return  render(request,"index.html", {"stocks":data.to_dict('index')})


def dashboard(request):
    stocks = Stock.objects.order_by('company')[0:3]
    top_stock_dict = {}
    for stock in stocks:
        # get the last 30 days price info
        top_stock_dict[stock] = stock.info_set.order_by("-date")[0:30]
        print(top_stock_dict[stock])
    return render(request, "app/dashboard.html", {"top_stocks_dict": top_stock_dict})



def predict(request):
    stocks = Stock.objects.order_by('company')[0:3]
    top_stock_dict = {}
    model_types = ["LSTM", "RNN"]
    for stock in stocks:
        top_stock_dict[stock] = {}
        for model_type in model_types:
            top_stock_dict[stock][model_type] = stock.price_set.filter(model_type = model_type).order_by("-date")[:5]
    print(top_stock_dict)

    return render(request, "app/predict.html", {"top_stocks_dict": top_stock_dict})
        
    