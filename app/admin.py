from django.contrib import admin
from .models import Stock, StockInfo

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockInfo)