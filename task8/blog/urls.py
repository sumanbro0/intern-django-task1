from django.urls import path
from .views import CommentDeleteView, CommentView, IndexView, RegisterView, LoginView, LogoutView, VerifyOTPView,PostCreateView,PostUpdateView,PostDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>', IndexView.as_view(), name='index_with_pk'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
     path('comments/<int:pk>/', CommentView.as_view(), name='add_comment'),
    path('comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),

]