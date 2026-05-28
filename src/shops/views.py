from django.shortcuts import render
from .models import BentoShop


def shop_list(request):
    shops = BentoShop.objects.all().order_by('-updated_at')

    context = {
        'shops': shops,
    }

    return render(request, 'shops/shop_list.html', context)