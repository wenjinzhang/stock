from apscheduler.scheduler import Scheduler
from django.core.cache import cache


sched = Scheduler()    

@sched.interval_schedule()
def sched_test():
    """
    :return:
    """
    import time
    print("schedule work is runing, Now is", str(time.time()))



