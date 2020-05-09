from django.urls import path
from . import views


app_name = 'ecapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.detail, name='detail'),
    path('product/', views.detail_from_article, name='detail_from_article'),
    path('toggele_fav_product_status/', views.toggle_fav_product_status,
         name='toggele_fav_product_status'),
    path('fav_products/', views.fav_products, name='fav_products'),
    path('my_products/', views.my_products, name='my_products'),
    path('cart/', views.cart, name='cart'),
    path('change_item_amount/', views.change_item_amount,
         name='change_item_amount'),
    path('order_history/', views.order_history, name='order_history'),
    path('sell/', views.sell, name='sell'),
    path('delete/<int:product_id>', views.delete, name='delete'),
]
