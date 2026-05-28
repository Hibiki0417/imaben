from django import forms
from .models import BentoShop


class BentoShopStatusForm(forms.ModelForm):
    class Meta:
        model = BentoShop
        fields = [
            'business_status',
            'stock_status',
            'today_menu',
            'is_discount_active',
            'discount_text',
            'discount_quantity',
            'discount_end_time',
        ]
        labels = {
            'business_status': '営業状況',
            'stock_status': '在庫状況',
            'today_menu': '今日のメニュー',
            'is_discount_active': '値下げ中',
            'discount_text': '値下げ内容',
            'discount_quantity': '残り個数',
            'discount_end_time': '終了予定時刻',
        }
        widgets = {
            'today_menu': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': '例：からあげ弁当、チキン南蛮、沖縄そば弁当'     
            }),
            'discount_text': forms.TextInput(attrs={
                'placeholder': '例：全品100円引き、30%OFF、2個で500円'
            }),
            'discount_end_time': forms.TimeInput(attrs={
                'type': 'time'
            }),
        }