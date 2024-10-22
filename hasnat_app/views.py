from django.shortcuts import render, redirect 
from .models import User
from .forms import  UserForm , UserTypeForm
from django.contrib.auth import login ,  authenticate
from django.urls import reverse_lazy 


def signup(request):
    user_type = request.GET.get('user_type') 
    if not user_type:
        return redirect('join_us')  
    if request.method == 'POST':
        form = UserForm(request.POST, user_type=user_type)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = UserForm(user_type=user_type)  
    return render(request, 'hasnat_app/signup.html', {'form': form, 'user_type': user_type})


def user_login(request):
    error_message = None  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('project_list')  
        else:
            error_message = 'Invalid username or password'  
    return render(request, 'hasnat_app/login.html', {'error': error_message})  

def join_us(request):
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            return redirect('signup') + f'?user_type={user_type}'
    else:
        form = UserTypeForm()
    return render(request, 'hasnat_app/join.html', {'form': form})

