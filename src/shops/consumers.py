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
            'today_menu': event.get('today_menu', ''),
            'is_discount_display_active': event.get('is_discount_display_active', False),
            'discount_text': event.get('discount_text', ''),
            'discount_quantity': event.get('discount_quantity', ''),
            'discount_end_time': event.get('discount_end_time', ''),
            'updated_at': event['updated_at'],
        }))