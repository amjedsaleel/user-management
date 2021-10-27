# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

# local Django
from .forms import UpdateUser
from .decorators import admin_only
from accounts.forms import CustomUserCreationForm


# Create your views here.


def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-panel:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        try:
            super_user = User.objects.get(username=username)
            if not super_user.is_superuser:
                messages.error(request, 'You are not admin user')
                return redirect('admin-panel:admin-login')
        except ObjectDoesNotExist:
            pass

        if user is not None:
            login(request, user)
            request.session['admin'] = 'admin'
            messages.success(request, 'Successfully Logged In')
            return redirect('admin-panel:dashboard')

        messages.error(request, 'Invalid credentials, Please try again.')
    return render(request, 'admin-panel/admin-login.html')


@login_required(login_url='admin-panel:admin-login')
@admin_only
def dashboard(request):
    users = User.objects.all().order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'admin-panel/dashboard.html', context)


@login_required(login_url='admin-panel:admin-login')
@admin_only
def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'admin-panel/user-profile.html', context)


@login_required(login_url='admin-panel:admin-login')
@admin_only
def update_user(request, username):
    user = User.objects.get(username=username)
    form = UpdateUser(instance=user)

    if request.method == 'POST':
        form = UpdateUser(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated user profile')
            return redirect('admin-panel:dashboard')
    context = {'form': form}
    return render(request, 'admin-panel/update-user.html', context)


@login_required(login_url='admin-panel:admin-login')
@admin_only
def delete_user(request, username):
    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('admin-panel:dashboard')

    User.objects.get(username=username).delete()
    messages.success(request, 'Successfully deleted the user')
    return redirect('admin-panel:dashboard')



@login_required(login_url='admin-panel:admin-login')
@admin_only
def block_user(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    return redirect('admin-panel:dashboard')


@login_required(login_url='admin-panel:admin-login')
@admin_only
def unblock_user(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save()
    return redirect('admin-panel:dashboard')


@login_required(login_url='admin-panel:admin-login')
@admin_only
def search_user(request):
    search_key = request.GET.get('search')
    users = User.objects.filter(username__icontains=search_key) | User.objects.filter(
        first_name__icontains=search_key) | User.objects.filter(email__icontains=search_key)
    context = {
        'users': users
    }
    return render(request, 'admin-panel/search.html', context)


@login_required(login_url='admin-panel:admin-login')
@admin_only
def add_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added an new user.')
            return redirect('admin-panel:dashboard')
    context = {'form': form}
    return render(request, 'admin-panel/add-user.html', context)
