from django.urls import path
from .views import index, ajax_search_products, shop

urlpatterns = [
    path('', index),
    path('ajax_search_products/', ajax_search_products),
    path('shop/<int:pk>/', shop)
]