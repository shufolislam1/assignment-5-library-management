from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import DepositMoneyView,CommentView, BorrowedBookView, ReturnBookView
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposiMoney'),
    path('borrow_book/<int:id>',  BorrowedBookView.as_view(), name='buy_now'),
    path('return_book/<int:id>', ReturnBookView.as_view(), name='returnBook'),
    path('comments/<int:pk>/', CommentView.as_view(), name='commentViews'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)