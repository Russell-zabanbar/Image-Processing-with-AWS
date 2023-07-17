







# # # signals.py
# # from django.db.models.signals import post_save, post_delete
# # from django.dispatch import receiver
# # from asgiref.sync import async_to_sync
# # from channels.layers import get_channel_layer
# # import json
# from orders.models import Order, single_order  
# # from orders.consumers import QueueConsumer  

# @receiver(post_save, sender=Order)
# def send_all_order()


# # @receiver(post_save, sender=single_order)
# # def model_save_handler(sender, instance, **kwargs):
# #     data = {}
# #     data['model1_data'] = fetch_model1_data()  
# #     data['model2_data'] = fetch_model2_data()  
# #     send_change_to_clients(data)

# # @receiver(post_delete, sender=Order)
# # @receiver(post_delete, sender=single_order)
# # def model_delete_handler(sender, instance, **kwargs):
# #     data = {}
# #     data['model1_data'] = fetch_model1_data()  
# #     data['model2_data'] = fetch_model2_data()  
# #     send_change_to_clients(data)

# # def fetch_model1_data():
# #     queryset = Order.objects.all()  # جایگزین کنید
# #     data = [item.to_dict() for item in queryset]  # تبدیل به لیست دیکشنری
# #     return data

# # def fetch_model2_data():
# #     queryset = single_order.objects.all()  # جایگزین کنید
# #     data = [item.to_dict() for item in queryset]  # تبدیل به لیست دیکشنری
# #     return data

# # def send_change_to_clients(data):
# #     channel_layer = get_channel_layer()
# #     async_to_sync(channel_layer.group_send)('queue_group', {'type': 'send_change', 'data': data})
