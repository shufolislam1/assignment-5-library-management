from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.userLogin, name='userLogin'),
    path('logout/', views.userLogout, name='userLogout'),
    path('', views.home, name='home'),
    path('Catagory/<slug:Catagory_slug>/', views.home, name='catagory'),
    path('all_Books/', views.all_Books, name='all_Books'),
    path('details/<int:pk>/', views.bookDetails.as_view(), name='bookDetails'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    # path('buy_now/<int:book_id>/', views.buy_now, name='buy_now'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)