from django.shortcuts import render
from .models import BentoShop


def shop_list(request):
    shops = BentoShop.objects.all().order_by('-updated_at')

    context = {
        'shops': shops,
    }

    return render(request, 'shops/shop_list.html', context)

from django.shortcuts import render, get_object_or_404
from .models import BentoShop


def shop_list(request):
    shops = BentoShop.objects.all().order_by('-updated_at')

    context = {
        'shops': shops,
    }

    return render(request, 'shops/shop_list.html', context)


def shop_detail(request, pk):
    shop = get_object_or_404(BentoShop, pk=pk)

    context = {
        'shop': shop,
    }

    return render(request, 'shops/shop_detail.html', context)    