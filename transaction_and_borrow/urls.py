from django.urls import path
from . import views
from .views import DepositMoneyView,CommentView, BorrowedBookView, ReturnBookView
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposiMoney'),
    path('borrow_book/<int:id>',  BorrowedBookView.as_view(), name='buy_now'),
    path('return_book/', ReturnBookView.as_view(), name='returnBook'),
    path('comments/<int:pk>//', CommentView.as_view(), name='commentViews'),
    path('deposit/', views.deposit_money, name='deposit_money'),
]
