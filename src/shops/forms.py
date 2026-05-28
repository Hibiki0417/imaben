from django import forms
from .models import BentoShop


class BentoShopStatusForm(forms.ModelForm):
    class Meta:
        model = BentoShop
        fields = [
            'business_status',
            'stock_status',
            'today_menu',
        ]
        labels = {
            'business_status': '営業状況',
            'stock_status': '在庫状況',
            'today_menu': '今日のメニュー',
        }
        widgets = {
            'today_menu': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': '例：からあげ弁当、チキン南蛮、沖縄そば弁当'
            }),
        }