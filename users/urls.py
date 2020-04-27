from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_page/', views.my_page, name='my_page'),
    path('user_detail/<int:user_id>', views.user_detail, name='user_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
