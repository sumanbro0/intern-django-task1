from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_product/", views.add_product, name="add_product"),
    path("product_detail/<int:id>/", views.product_detail, name="product_detail"),
    path("add_comment/<int:id>/", views.add_comment, name="add_comment"),
    path("delete_comment/<int:id>/", views.delete_comment, name="delete_comment"),
    path("update_comment/<int:id>/", views.update_comment, name="update_comment"),
]