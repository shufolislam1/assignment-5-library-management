from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
# Create your views here.

TRANSACTION_TYPE = (
    ('DEPOSIT', 'Deposite'),
    
)

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
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
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "transactions/deposite_email.html")
        return super().form_valid(form)
    
class BorrowBookView(TransactionCreateMixin):
    form_class = BorrowBookForm  # You need to create this form for book borrowing
    title = 'Borrow Book'

    def get_initial(self):
        initial = {'transaction_type': BORROW}  # Assuming you have a constant BORROW
        return initial

    def form_valid(self, form):
        book_cost = form.cleaned_data.get('book').cost
        account = self.request.user.account

        if account.balance >= book_cost:
            # Sufficient balance to borrow the book
            account.balance -= book_cost
            account.save(update_fields=['balance'])

            # Track borrowing history
            BorrowHistory.objects.create(user=self.request.user, book=form.cleaned_data.get('book'))

            messages.success(
                self.request,
                f'You have borrowed {form.cleaned_data.get("book")} successfully.'
            )

            # Send email to the user about the successful borrowing
            send_transaction_email(
                self.request.user,
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

    def get_initial(self):
        return {'transaction_type': RETURN}

    def form_valid(self, form):
        book_cost = form.cleaned_data.get('book').cost
        amount = book_cost  # Positive value for returning
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=['balance']
        )

        # Update borrowing history with return date
        borrowing_history = get_object_or_404(
            BorrowingHistory,
            user=self.request.user,
            book=form.cleaned_data.get('book'),
            return_date=None
        )
        borrowing_history.return_date = timezone.now()
        borrowing_history.save()

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(book_cost))}$ was added to your account for returning the book'
        )
        send_transaction_email(self.request.user, amount, "Return Book Message", "transactions/return_book_email.html")
        return super().form_valid(form)


class ReviewBookView(LoginRequiredMixin, CreateView):
    template_name = 'transactions/review_form.html'
    form_class = ReviewForm
    model = Transaction
    success_url = reverse_lazy('book_list')  # Update with your book list URL
    title = 'Review Book'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BorrowingHistoryView(LoginRequiredMixin, ListView):
    model = BorrowHistory
    template_name = 'transactions/borrowing_history.html'
    context_object_name = 'borrowing_history'

    def get_queryset(self):
        return BorrowHistory.objects.filter(user=self.request.user)
