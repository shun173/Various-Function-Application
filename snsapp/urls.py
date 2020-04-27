from django.urls import path
from . import views

app_name = 'snsapp'
urlpatterns = [
    path('', views.index, name='index'),
]
