from orders.models import Order, single_order
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect
import base64


def CreateOrderUtils(request, bread_number, random_code):
    one_group = Order.objects.all().count()
    two_group = single_order.objects.all().count()
    order_number = one_group + two_group
    if bread_number > 1:
        times = Order.objects.aggregate(Sum('time'))
        waiting_time = times['time__sum']
        time_sec = int(bread_number * 20)
        if waiting_time is None:
            waiting_time = time_sec

        order_number += 1
        Order.objects.create(
            user=request.user,
            order_code=order_number,
            time=time_sec,
            waiting_time=waiting_time,
            bread_number=bread_number,
            random_code=random_code
        )
        messages.success(request, "نوبت شما با موفقیت ثبت شده ", 'success')
        return redirect('detect:order_list')
    else:
        times = single_order.objects.aggregate(Sum('time'))
        waiting_time = times['time__sum']
        time_sec = int(bread_number * 20)
        if waiting_time is None:
            waiting_time = time_sec
        single_order.objects.create(
            user=request.user,
            order_code=order_number + 1,
            time=time_sec,
            waiting_time=waiting_time,
            bread_number=bread_number,
            random_code=random_code
        )
    messages.success(request, "یک عدد نان نوبت شما با موفقیت ثبت شده ", 'success')
    return redirect('detect:order_list')


