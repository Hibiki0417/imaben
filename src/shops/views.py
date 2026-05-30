from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BentoShop, ShopStaff
from .forms import BentoShopStatusForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

def shop_list(request):
    shops = BentoShop.objects.all().order_by('-updated_at')

    context = {
        'shops': shops,
    }

    return render(request, 'shops/public/shop_list.html', context)


def shop_detail(request, pk):
    shop = get_object_or_404(BentoShop, pk=pk)

    context = {
        'shop': shop,
    }

    return render(request, 'shops/public/shop_detail.html', context)    

@login_required
def manager_dashboard(request):
    try:
        shop_staff = ShopStaff.objects.get(user=request.user)
    except ShopStaff.DoesNotExist:
        return render(request, 'shops/manager/no_shop_staff.html')

    shop = shop_staff.shop

    if request.method == 'POST':
        form = BentoShopStatusForm(request.POST, instance=shop)
        if form.is_valid():
            shop = form.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'shop_status',
                {
                    'type': 'shop_status_update',
                    'shop_id': shop.id,
                    'business_status': shop.business_status,
                    'business_status_display': shop.get_business_status_display(),
                    'stock_status': shop.stock_status,
                    'stock_status_display': shop.get_stock_status_display(),
                    'today_menu': shop.today_menu,
                    'is_discount_display_active': shop.is_discount_display_active,
                    'discount_text': shop.discount_text,
                    'discount_quantity': shop.discount_quantity,
                    'discount_end_time': shop.discount_end_time.strftime('%H:%M') if shop.discount_end_time else '',
                    'updated_at': timezone.localtime(shop.updated_at).strftime('%Y年%m月%d日%H:%M'),
                }
            )

            return redirect('shops:manager_dashboard')
    else:
        form = BentoShopStatusForm(instance=shop)

    context = {
        'shop': shop,
        'form': form,
    }

    return render(request, 'shops/manager/dashboard.html', context)

@login_required
def update_quick_status(request):
        if request.method != 'POST':
            return redirect('shops:manager_dashboard')

        try:
            shop_staff = ShopStaff.objects.get(user=request.user)
        except ShopStaff.DoesNotExist:
            return render(request, 'shops/manager/no_shop_staff.html')

        shop = shop_staff.shop

        status_type = request.POST.get('status_type')
        status_value = request.POST.get('status_value')

        if status_type == 'business_status':
            valid_values = [choice[0] for choice in BentoShop.BUSINESS_STATUS_CHOICES]
            if status_value in valid_values:
                shop.business_status = status_value
                shop.save()

        elif status_type == 'stock_status':
            valid_values = [choice[0] for choice in BentoShop.STOCK_STATUS_CHOICES]
            if status_value in valid_values:
                shop.stock_status = status_value
                shop.save()
      
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'shop_status',
        {
            'type': 'shop_status_update',
            'shop_id': shop.id,
            'business_status': shop.business_status,
            'business_status_display': shop.get_business_status_display(),
            'stock_status': shop.stock_status,
            'stock_status_display': shop.get_stock_status_display(),
            'updated_at': timezone.localtime(shop.updated_at).strftime('%Y年%m月%d日%H:%M'),
        }
    )

        return redirect('shops:manager_dashboard')

        