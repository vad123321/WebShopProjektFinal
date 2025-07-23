from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('signin', views.signin),
    path('signout', views.signout),
    path('profile', views.profile),
    path('ajaxreg', views.ajaxreg),
    path('favorites', views.favorites),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('favorites/delete/', views.remove_favorite, name='remove_favorite'),
    path('change_password', views.change_password, name='change_password'),
]
