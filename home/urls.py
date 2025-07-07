from django.urls import path
from .views import index, about, contacts, services, blog

urlpatterns = [
    path('', index),
    path('about', about),
    path('contacts', contacts),
    path('services', services),
    path('blog', blog),
]