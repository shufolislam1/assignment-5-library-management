from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Comment
from django.contrib.auth.forms import UserChangeForm
from .models import Catagory, Book

class BrandForm(forms.ModelForm):
    class Meta:
        moodel = Catagory
        fields = '__all__'
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
        
# class commentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['name', 'email', 'body']
        
 
 
# class ChangeUserForm(UserChangeForm):
#     password = None
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']