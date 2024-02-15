from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.userLogin, name='userLogin'),
    path('logout/', views.userLogout, name='userLogout'),
    path('', views.home, name='home'),
    path('brand/<slug:brand_slug>/', views.home, name='brand'),
    path('all_cars/', views.all_cars, name='all_cars'),
]
