
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('book/<int:id>',views.book,name='book_detail'),
    path('login/',views.log_in,name='login'),
    path('signup/',views.sign_up,name='signup'),
    path('logout/',views.log_out,name='logout'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('reset_password/<int:id>',views.change_password,name='reset_password'),
    path('remove_from_cart/<int:id>',views.remove_from_cart,name='remove_from_cart'),
    path("cart/",views.cart,name="cart"),
    path("add_to_cart/<int:id>",views.add_to_cart,name="add_to_cart"),
    path("orders/",views.place_order,name="orders"),
    path("address/",views.address,name="address"),
    path("placed_orders/",views.orders,name="placed_orders"),
    path("search/",views.search,name="search"),

]
