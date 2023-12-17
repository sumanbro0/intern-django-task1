
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:post_id>", views.post_detail, name="post_detail"),
    path("add_post", views.add_post, name="add_post"),
]
