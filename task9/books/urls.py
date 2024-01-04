
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
    path("wishlist/",views.wishlist,name="wishlist"),
    path("add_to_wishlist/<int:id>",views.add_to_wishlist,name="add_to_wishlist"),
    path("remove_from_wishlist/<int:id>",views.remove_from_wishlist,name="remove_from_wishlist"),
    path("add_review/<int:id>",views.add_review,name="add_review"),
    path("remove_review/<int:id>",views.remove_review,name="remove_review"),
    path("notifications/",views.notifications,name="notifications"),
    path("delete_notification/<int:id>",views.delete_notification,name="delete_notification"),
    path("my_books",views.my_books,name="my_books"),
    path('read-book/<int:book_id>/', views.read_book, name='read_book'),
]
