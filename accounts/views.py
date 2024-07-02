from django.shortcuts import render
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm
import random
from django.urls import reverse
from django.contrib import messages

import requests

User = get_user_model()

def register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect(reverse('login'))
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    
    return render(request,'register.html', {'form': form})

def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            # Payload for authentication
            payload = {
                "username" : username,
                "password" : password
            }
            # user = authenticate(request, username=username, password=password)

            #  The jwt token endpoint
            url = 'localhost:8000/accounts/token/'
            
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    token = data['access']
                    if token is not None:
                        print(f'Access token: {token}')
                    return redirect('dashboard')
                else:
                    print('Login failed:', data['message'])
            else:
                print('Failed to call the API:', response.status_code)
                        

    return render(request, "login.html", context={"form": form})

def logout(request):
    auth.logout(request)
    return redirect("login")


def dashboard(request):
    users = User.objects.all()
    return render(request,'dashboard.html',{'users':users})