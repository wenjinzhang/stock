from django.db import models

# Create your models here.
class Stock(models.Model):
    id = models.AutoField(primary_key = True)
    # Date = models.TimeField(_(""), auto_now=False, auto_now_add=False)
    symbol = models.CharField("Symbol", max_length=50,default="")
    company = models.CharField("Company", max_length=50, default="Other company")

    def __str__(self):
        return self.company


class StockInfo(models.Model):
    id = models.CharField("timestamp_symbol", max_length=50, primary_key = True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="info_set")
    open_price = models.DecimalField("Open", max_digits=11, decimal_places=2, default=None)
    high_price = models.DecimalField("High", max_digits=11, decimal_places=2, default=None)
    low_price = models.DecimalField("Low", max_digits=11, decimal_places=2, default=None)
    close_price = models.DecimalField("Close", max_digits=11, decimal_places=2, default=None)
    adj_close_price = models.DecimalField("Adj Close", max_digits=11, decimal_places=2, default=None)
    volume = models.DecimalField("Volume", max_digits=11, decimal_places=2, default=None)
    date = models.DateTimeField("Date", auto_now=False, auto_now_add=False, default=None)

    def __str__(self):
        return "date:{};stock:{};close price:{}".format(self.date, self.stock, self.close_price)
    
class PredictPrice(models.Model):
    id = models.CharField("timestamp_symbol", max_length=50, primary_key = True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="price_set")
    price = models.DecimalField("Price", max_digits=11, decimal_places=2, default=None)
    date = models.DateTimeField("Date", auto_now=False, auto_now_add=False, default=None)
    model_type = models.CharField("model_type", max_length=20, default=None)
    
    def __str__(self):
        return "date:{};stock:{};prediction price:{}".format(self.date, self.stock, self.price)
