# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# local Django
from . forms import CustomUserCreationForm

# Create your views here.


def login_fun(request):
    if request.user.is_authenticated:
        return redirect('user:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            if not user.is_active:
                messages.error(request, 'This user is blocked')
                return redirect('accounts:login')
        except ObjectDoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)

        if user.is_superuser:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')

        if user is not None:
            login(request, user)
            request.session['user'] = 'user'
            messages.success(request, 'Successfully Logged In')
            return redirect('user:index')

        messages.error(request, 'Invalid credentials, Please try again.')
    return render(request, 'accounts/login.html')


def signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-panel:dashboard')
        else:
            return redirect('user:index')

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
        admin = False
        messages.success(request, 'Successfully logged out')

        if request.user.is_superuser:
            admin = True

        if admin:
            del request.session['admin']
            logout(request)
            return redirect('admin-panel:admin-login')

        del request.session['user']
        logout(request)
        return redirect('accounts:login')
