from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import Catagory, Book
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Order
from transaction_and_borrow.models import  BorrowingHistory

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,'registered successful')
            return redirect('userLogin')

    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form':register_form, 'type':'register'})

def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user_authenticate = authenticate(username=user_name, password = user_pass)
            if user_authenticate is not None:
                messages.success(request,'login successful')
                login(request, user_authenticate)
                return redirect('home')
            else:
                messages.warning(request, 'login info incorrect')
                return redirect('register')
            
    else:
        form = AuthenticationForm()
    return render(request,'register.html', {'form': form, 'type':'login'})
    
def userLogout(request):
    logout(request)
    messages.success(request,'logout successful')
    return redirect('userLogin')

def home(request, Catagory_slug = None):
    print("Category Slug:", Catagory_slug)
    Books = Book.objects.all()
    if Catagory_slug is not None:
        category = get_object_or_404(Catagory, slug=Catagory_slug)
        print("Selected Category:", category.id)
        Books = Book.objects.filter(Catagory = category)
        print("Generated Query:", Books.query)
    Catagorys = Catagory.objects.all()
    
    return render(request, 'home.html', {'Catagorys': Catagorys, 'Books': Books})

def all_Books(request):
    Books = Book.objects.all()
    Catagorys = Catagory.objects.all()

    return render(request, 'home.html', {'Catagorys': Catagorys, 'Books': Books})

class bookDetails(DetailView):
    model = Book
    template_name = 'book_details.html'

   
# @login_required
# def buy_now(request, book_id):
#     book = get_object_or_404(Book, id=book_id)

#     if request.method == 'POST':
#         if book.quantity > 0:
#             book.user = request.user
#             book.quantity -= 1
#             book.save()
#             messages.success(request, 'Book purchased successfully!')
#         else:
#             messages.warning(request, 'Book is out of stock.')

#     return redirect('bookDetails', pk=book.id)


@login_required
def profile(request):
    user_data = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    orders = Order.objects.filter(user=request.user)
    print(orders)
    data = BorrowingHistory.objects.filter(user=request.user)
    
    return render(request, 'profile.html', {'orders': orders, 'user_data': user_data, 'data':data})


    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'update_profile.html', {'form' : profile_form})



