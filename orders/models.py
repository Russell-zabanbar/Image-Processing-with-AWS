from django.db import models
from accounts.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_code = models.IntegerField()
    time = models.IntegerField()
    waiting_time = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    bread_number = models.IntegerField()
    random_code = models.CharField(max_length=6, null=True, blank=True)

class single_order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_code = models.IntegerField()
    time = models.IntegerField()
    waiting_time = models.IntegerField()
    created_at = models.TimeField(auto_now_add=True)
    bread_number = models.IntegerField()
    random_code = models.CharField(max_length=6, null=True, blank=True)




@receiver(post_save, sender=Order)
def send_order_change(sender, instance, created, **kwargs):
    if created:
        data = [{
            'order_code': instance.order_code,
            'waiting_time': instance.waiting_time,
            'bread_number': instance.bread_number
        }]
        async_to_sync(channel_layer.group_send)('queue_group', {'type': 'send_change', 'data': data})
