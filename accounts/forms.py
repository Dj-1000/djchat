from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms   
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput, TextInput

#register a user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email','password1','password2']
        
        
# authenticate the user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
