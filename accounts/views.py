# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache

# local Django
from .forms import CustomUserCreationForm
from adminpanel.decorators import admin_only
from user.decorators import user_only

# Create your views here.


@never_cache
def login_fun(request):
    """
    User login
    """
    # if request.user.is_authenticated:
    #     return redirect('user:index')
    if request.session.has_key('user'):
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

        if user is not None and not user.is_superuser:
            request.session['user'] = user.username
            messages.success(request, 'Successfully Logged In')
            return redirect('user:index')

        messages.error(request, 'Invalid credentials, Please try again.')

    return render(request, 'accounts/login.html')


@never_cache
def signup(request):
    if request.session.has_key('user'):
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


@never_cache
@user_only
def user_sign_out(request):
    if request.method == "POST":
        try:
            del request.session['user']
        except KeyError:
            pass

        messages.success(request, 'Successfully logged out')
        return redirect('accounts:login')

    return render(request, 'accounts/login.html')


@never_cache
@admin_only
def admin_sign_out(request):
    if request.method == "POST":
        try:
            del request.session['admin']
        except KeyError:
            pass

        messages.success(request, 'Successfully logged out')
        return redirect('admin-panel:admin-login')
