from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BentoShop, ShopStaff
from .forms import BentoShopStatusForm

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
            form.save()
            return redirect('shops:manager_dashboard')
    else:
        form = BentoShopStatusForm(instance=shop)

    context = {
        'shop': shop,
        'form': form,
    }

    return render(request, 'shops/manager/dashboard.html', context)