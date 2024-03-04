from django.urls import path
from .views import DepositMoneyView,CommentView, BorrowedBookView, ReturnBookView
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposiMoney'),
    path('borrow_book/',  BorrowedBookView.as_view(), name='borrowBook'),
    path('return_book/', ReturnBookView.as_view(), name='returnBook'),
    path('comments/<int:pk>//', CommentView.as_view(), name='commentViews')
]
