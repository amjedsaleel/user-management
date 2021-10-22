# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# local Django
from . forms import CustomUserCreationForm

# Create your views here.


def login_fun(request):
    if request.user.is_authenticated:
        return redirect('user:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:index')
    return render(request, 'accounts/login.html')


def signup(request):
    form = CustomUserCreationForm(use_required_attribute=False)

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, use_required_attribute=False)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully account is created')
            return redirect('accounts:login')
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('accounts:login')
