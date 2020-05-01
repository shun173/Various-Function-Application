from django.urls import path
from . import views

app_name = 'snsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_articles/', views.my_articles, name='my_articles'),
    path('post_article/', views.post_article, name='post_article'),
]
