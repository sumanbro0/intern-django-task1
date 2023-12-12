
from django.urls import  path
from .views import detail, index
urlpatterns = [
    path('home/',index,name="index"),
    path('home/<int:id>',detail,name="product_detail"),
]
