from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),

    path('', views.shop_list, name='shop_list'),
    path('<int:pk>/', views.shop_detail, name='shop_detail'),
]