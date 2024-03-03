from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.core.mail import EmailMultiAlternatives
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from .models import Transaction, BorrowingHistory
from .forms import DepositForm, BorrowBookForm, ReviewForm, ReturnBookForm

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transactions_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'book': self.request.book
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'balance': self.request.balance,
        })
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        # Assuming each user has multiple books
        book = self.request.user.book_set.first()
        kwargs.update({
            'book': book,
        })
        return kwargs
    

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user = self.request.user

        # Update the user's book balance
        user.book.balance += amount
        user.book.save()

        # Create a new transaction record
        form.instance.user = user
        form.instance.balance = user.book.balance - amount
        form.instance.balance_after_transaction = user.book.balance
        form.instance.save()

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        # Send transaction email
        send_transaction_email(user, amount, "Deposit Message", "transactions/deposit_email.html")

        return super().form_valid(form)

class BorrowBookView(TransactionCreateMixin):
    form_class = BorrowBookForm
    title = 'Borrow Book'

    def form_valid(self, form):
        book_cost = form.cleaned_data.get('book').price

        if self.request.balance >= book_cost:
            # Sufficient balance to borrow the book
            self.request.balance -= book_cost
            self.request.save(update_fields=['balance'])

            # Track borrowing history
            BorrowingHistory.objects.create(user=self.request, book=form.cleaned_data.get('book'))

            messages.success(
                self.request,
                f'You have borrowed {form.cleaned_data.get("book")} successfully.'
            )

            # Send email to the user about the successful borrowing
            send_transaction_email(
                self.request,
                book_cost,
                "Book Borrowed",
                "transactions/borrow_book_email.html"
            )

        else:
            messages.error(self.request, "Insufficient balance to borrow the book.")

        return super().form_valid(form)

class ReturnBookView(TransactionCreateMixin, SuccessMessageMixin):
    form_class = ReturnBookForm
    title = 'Return Book'
    success_message = 'Book returned successfully'

    def form_valid(self, form):
        book_cost = form.cleaned_data.get('book').cost
        amount = book_cost  # Positive value for returning
        self.request.balance += amount
        self.request.save(update_fields=['balance'])

        # Update borrowing history with return date
        borrowing_history = get_object_or_404(
            BorrowingHistory,
            user=self.request,
            book=form.cleaned_data.get('book'),
            return_date=None
        )
        borrowing_history.return_date = timezone.now()
        borrowing_history.save()

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(book_cost))}$ was added to your account for returning the book'
        )
        send_transaction_email(self.request, amount, "Return Book Message", "transactions/return_book_email.html")
        return super().form_valid(form)

class ReviewBookView(LoginRequiredMixin, CreateView):
    template_name = 'transactions/review_form.html'
    form_class = ReviewForm
    model = Transaction
    success_url = reverse_lazy('book_list')  # Update with your book list URL
    title = 'Review Book'

    def form_valid(self, form):
        form.instance = self.request
        return super().form_valid(form)

class BorrowingHistoryView(LoginRequiredMixin, ListView):
    model = BorrowingHistory
    template_name = 'transactions/borrowing_history.html'
    context_object_name = 'borrowing_history'

    def get_queryset(self):
        return BorrowingHistory.objects.filter(user=self.request)
