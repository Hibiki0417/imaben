from django.db import models


class BentoShop(models.Model):
    BUSINESS_STATUS_CHOICES = [
        ('open', '営業中'),
        ('closed', '本日休み'),
        ('preparing', '準備中'),
    ]

    STOCK_STATUS_CHOICES = [
        ('enough', '十分あり'),
        ('low', '残り少ない'),
        ('sold_out', '売り切れ'),
    ]

    name = models.CharField('店名', max_length=100)
    address = models.CharField('住所', max_length=255)
    description = models.TextField('店舗説明', blank=True)
    business_status = models.CharField(
        '営業状況',
        max_length=20,
        choices=BUSINESS_STATUS_CHOICES,
        default='closed'
    )
    stock_status = models.CharField(
        '在庫状況',
        max_length=20,
        choices=STOCK_STATUS_CHOICES,
        default='enough'
    )
    today_menu = models.TextField('今日のメニュー', blank=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def __str__(self):
        return self.name