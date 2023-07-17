from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json
from orders.models import Order
class QueueConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.group_name = 'queue_group'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        all_orders = await sync_to_async(self.get_all_order)()
        await self.send_change({'data':all_orders})

        #await self.send_change({'data': orders_list})

    def get_all_order(self):
        order_list = []
        query_set = Order.objects.all()
        for query in query_set:
            order_list.append({'order_code':query.order_code, 'waiting_time':query.waiting_time, 'bread_number':query.bread_number})
        return order_list    
    async def send_change(self, event):
        print(event)
        event_data = event['data']
        for order in event_data:
            await self.send(json.dumps(order))
