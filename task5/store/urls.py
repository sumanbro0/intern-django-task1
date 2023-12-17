
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("add_product/",views.add_product,name="add_product"),
    path("product_detail/<int:id>/",views.product_detail,name="product_detail"),
]
