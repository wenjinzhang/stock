from django.http import HttpResponse
from django.shortcuts import render
import yfinance as yf

def home(request):
    data = yf.download("AAPL", period = "7d", interval = "1d")
    return  render(request,"index.html", {"stocks":data.to_dict('index')})