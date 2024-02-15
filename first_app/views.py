from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Brand, Car
from django.views.generic import DetailView

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,'registered successful')
            return redirect('register')

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

def home(request, brand_slug = None):
    cars = Car.objects.all()
    if brand_slug is not None:
        brands = Brand.objects.get(slug = brand_slug)
        cars = Car.objects.filter(brand = brands)
    brands = Brand.objects.all()
    
    return render(request, 'home.html', {'brands': brands, 'cars': cars})

def all_cars(request):
    cars = Car.objects.all()
    brands = Brand.objects.all()

    return render(request, 'home.html', {'brands': brands, 'cars': cars})

class carDetails(DetailView):
    model = Car
    template_name = 'car_details.html'
    
    def post(self, request, *args, **kwargs):
        car = self.get_object()
        if self.request.method == 'POST':
            comment_form = forms.commentForm(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.car = car
                new_comment.save()
            return self.get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object 
        comments = car.comment.all()
        comment_form = forms.commentForm()
        
        context['comments'] = comments
        context['comments_form'] = comment_form
        return context