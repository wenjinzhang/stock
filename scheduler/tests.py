from django.test import TestCase

from app.models import Stock

# Create your tests here.

class ScheduleTest(TestCase):

    def test_something(self):
        s = Stock.objects.all()
        print(s)
