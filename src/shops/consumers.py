import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ShopStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'shop_status'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def shop_status_update(self, event):
        await self.send(text_data=json.dumps({
            'shop_id': event['shop_id'],
            'business_status': event['business_status'],
            'business_status_display': event['business_status_display'],
            'stock_status': event['stock_status'],
            'stock_status_display': event['stock_status_display'],
            'updated_at': event['updated_at'],
        }))