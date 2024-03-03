from django.urls import path
from .views import DepositMoneyView, BorrowBookView, BorrowingHistoryView, ReturnBookView, ReviewBookView
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposiMoney'),
    path('borrow_book/',  BorrowBookView.as_view(), name='borrowBook'),
    path('borrow_history', BorrowingHistoryView.as_view(), name='borrowHistory'),
    path('return_book/', ReturnBookView.as_view(), name='returnBook'),
    path('review_book/', ReviewBookView.as_view(), name='reviewBook')
]
