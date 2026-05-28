from django.db import models
from django.contrib.auth.models import User

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
    is_discount_active = models.BooleanField(
        '値下げ中',
        default=False
    )
    discount_text = models.CharField(
        '値下げ内容',
        max_length=100,
        blank=True
    )
    discount_quantity = models.PositiveIntegerField(
        '残り個数',
        null=True,
        blank=True
    )
    discount_end_time = models.TimeField(
        '終了予定時刻',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def __str__(self):
        return self.name


class ShopStaff(models.Model):
    ROLE_CHOICES = [
        ('owner', 'オーナー'),
        ('staff', 'スタッフ'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='ユーザー'
    )
    shop = models.ForeignKey(
        BentoShop,
        on_delete=models.CASCADE,
        related_name='staff_members',
        verbose_name='店舗'
    )
    role = models.CharField(
        '権限',
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.shop.name}'