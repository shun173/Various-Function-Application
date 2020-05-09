from django.urls import path
from . import views

app_name = 'snsapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('good_articles/', views.good_articles, name='good_articles'),
    path('my_articles/', views.my_articles, name='my_articles'),
    path('post_article/', views.post_article, name='post_article'),
    path('delete/<int:article_id>', views.delete, name='delete'),
    path('good/<int:pk>', views.good, name='good'),
]
