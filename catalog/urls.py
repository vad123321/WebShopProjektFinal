from django.urls import path
from .views import index, ajax_search_products

urlpatterns = [
    path('', index),
    path('ajax_search_products/', ajax_search_products, name='ajax_search_products'),
]