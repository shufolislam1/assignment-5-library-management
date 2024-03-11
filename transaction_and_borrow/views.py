from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView
from django.core.mail import EmailMultiAlternatives
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from .models import  BorrowingHistory
from .forms import DepositForm, CommentForm
from django.views import View
from first_app.models import Book
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class DepositMoneyView(View):
    template_name = 'transactions/deposit_money.html'

    def get(self, request, *args, **kwargs):
        form = DepositForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_account = request.user.account
        
        if request.method == 'POST':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                
                messages.success(
                    request,
                    f'{"{:,.2f}".format(float(amount))}$ is deposited to your account successfully'
                )

                send_transaction_email(request.user, amount, "Deposit Message", "transactions/deposit_email.html")
                return redirect('home')
        else:
            form = DepositForm()

        return render(request, self.template_name, {'form': form})


class BorrowedBookView(View): 

    def post(self, request, id):
        book = get_object_or_404(Book, pk=id)
        user_balance = int(request.user.account.balance)
        borrowing_price = int(book.borrowing_price)

        if user_balance >= borrowing_price:
            BorrowingHistory.objects.create(user=request.user, book=book)
            request.user.account.balance -= borrowing_price
            request.user.account.save()
            messages.success(
                request,
                f'{"{:,.2f}".format(float(borrowing_price))}$ is borrowed book successfully'
                )

            send_transaction_email(request.user, borrowing_price, "Borrowed Book Message", "transactions/borrowed_book_email.html")
        else:
            messages.success(
                request,
                f'{"{:,.2f}".format(float(borrowing_price))}$ Borrowing price is more than your account balance. Please deposit more'
                )

        return redirect('profile')

class ReturnBookView(View):

    def get(self, request, id):
        record = get_object_or_404(BorrowingHistory, pk=id)

        request.user.account.balance += int(record.book.borrowing_price)
        request.user.account.save()

        record.delete()
        messages.success(
            request,
            'Borrowed book is returned successfully'
        )

        # send_transaction_email(request.user, int(record.book.borrowing_price), "Return Book Message", "return_book_email.html")
        return redirect('profile')

class CommentView(DetailView):
    model = Book
    template_name = 'transactions/comment.html'
 
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
        
            new_comment.save()
        return self.get(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        comments = book.comments.all()
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['book'] = book
        return context  