"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from genesis.views import *

urlpatterns = [
    path('', lambda request: redirect('home', permanent=False)),
    path('admin/', admin.site.urls),
    path('signup/', signup,name="signup" ),
    path('login/', login ,name="login" ),
    path('home/', home ,name="home" ),
    path('logout/', logout_view, name='logout'),
    path('clear_cc/', clear_cc, name='clear_cc'),
    path('shop/', shop ,name="shop" ),
    path('about/', about ,name="about" ),
    path('product/', product_view, name='product'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('admin_check/', admin_check, name='admin_check'),
    path('admin-view/', admin_view, name='admin_view')



]
