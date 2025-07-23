from django.urls import path
from .views import index, about, contacts, services, blog, facebook, instagram, twitter, linkedin, youtube, track, returns, shipping, faqs

urlpatterns = [
    path('', index),
    path('about', about),
    path('contacts', contacts),
    path('services', services),
    path('blog', blog),
    path('facebook', facebook),
    path('instagram', instagram),
    path('twitter', twitter),
    path('linkedin', linkedin),
    path('youtube', youtube),
    path('track', track),
    path('returns', returns),
    path('shipping', shipping),
    path('faqs', faqs),
]