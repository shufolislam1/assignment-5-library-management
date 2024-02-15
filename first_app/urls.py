from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.userLogin, name='userLogin'),
    path('logout/', views.userLogout, name='userLogout'),
    path('', views.home, name='home'),
    path('brand/<slug:brand_slug>/', views.home, name='brand'),
    path('all_cars/', views.all_cars, name='all_cars'),
    path('details/<int:pk>/', views.carDetails.as_view(), name='carDetails'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/pass_change/', views.pass_change, name='pass_change'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)