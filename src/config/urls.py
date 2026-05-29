from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'manager/login/',
        auth_views.LoginView.as_view(
            template_name='manager/login.html'
        ),
        name='manager_login'
    ),

    path(
        'manager/logout/',
        auth_views.LogoutView.as_view(),
        name='manager_logout'
    ),

    path('shops/', include('shops.urls')),
]