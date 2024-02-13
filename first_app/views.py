from django.shortcuts import render, redirect
from . import forms

# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('register')

    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form':register_form})