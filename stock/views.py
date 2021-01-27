from django.http import HttpResponse
from django.shortcuts import render
import yfinance as yf

def home(request):
    data = yf.download("AAPL", period = "1d", interval = "1m")
    return  render(request,"index.html", {"stocks":data.to_dict('index')})