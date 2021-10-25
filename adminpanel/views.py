# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login

# local Django
from .forms import UpdateUser
from .decorators import admin_only
# Create your views here.


def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-panel:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if request.user.is_superuser:
                messages.success(request, 'Successfully Logged In')
                return redirect('admin-panel:dashboard')
            else:
                messages.error(request, 'You are not admin user')
                return redirect('admin-panel:admin-login')

        messages.error(request, 'Invalid credentials, Please try again.')
    return render(request, 'admin-panel/admin-login.html')


@login_required(login_url='admin-panel:admin-login')
@admin_only
def dashboard(request):
    users = User.objects.all()
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
    user = User.objects.get(username=username)

    if request.method == 'POST':
        User.objects.get(username=username).delete()
        messages.success(request, 'Successfully deleted the user')
        return redirect('admin-panel:dashboard')
    context = {'user': user}
    return render(request, 'admin-panel/delete.html', context)
