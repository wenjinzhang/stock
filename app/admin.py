from django.contrib import admin
from .models import Stock, StockInfo,PredictPrice

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockInfo)
admin.site.register(PredictPrice)