from celery import shared_task
from .models import Order, single_order
from accounts.models import OtpCode
from datetime import datetime, timedelta

import pytz


@shared_task
def delete_order_expired_time():
    time_sec = Order.objects.values_list('waiting_time', flat=True)
    print(time_sec)
    for time in time_sec:
        print(time)
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(seconds=time)
        single_order.objects.filter(created_at__lt=expired_time).delete()

    # time_sec = single_order.objects.values_list('waiting_time', flat=True)
    # for time in time_sec:
    #     expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(seconds=time)
    #     single_order.objects.filter(created_at__lt=expired_time).delete()
    #
    # expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    # OtpCode.objects.filter(created__lt=expired_time).delete()
