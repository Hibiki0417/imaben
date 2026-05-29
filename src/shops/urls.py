from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/update-quick-status/', views.update_quick_status, name='update_quick_status'),

    path('', views.shop_list, name='shop_list'),
    path('<int:pk>/', views.shop_detail, name='shop_detail'),
]