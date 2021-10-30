# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

# local Django
from .forms import UpdateUser
from .decorators import admin_only
from accounts.forms import CustomUserCreationForm


# Create your views here.


@never_cache
def admin_login(request):
    # if request.user.is_authenticated:
    #     if request.user.is_superuser:
    #         return redirect('admin-panel:dashboard')
    if request.session.has_key('admin'):
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
            request.session['admin'] = 'admin'
            messages.success(request, 'Successfully Logged In')
            return redirect('admin-panel:dashboard')

        messages.error(request, 'Invalid credentials, Please try again.')
    return render(request, 'admin-panel/admin-login.html')


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
def dashboard(request):
    users = User.objects.all().order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'admin-panel/dashboard.html', context)


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'admin-panel/user-profile.html', context)


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
def update_user(request, username):
    user = User.objects.get(username=username)
    form = UpdateUser(instance=user)

    if request.is_ajax():
        form = UpdateUser(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated user profile')
            return JsonResponse({'msg': 'Success'})
        else:
            return JsonResponse({'er': form.errors})
    context = {
            'form': form,
            'username': user.username
    }
    return render(request, 'admin-panel/update-user.html', context)


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
def delete_user(request, username):
    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('admin-panel:dashboard')

    User.objects.get(username=username).delete()
    messages.success(request, 'Successfully deleted the user')
    return redirect('admin-panel:dashboard')


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
def block_user(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()

    return redirect('admin-panel:dashboard')


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
def unblock_user(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save()
    return redirect('admin-panel:dashboard')


@never_cache
@admin_only
# @login_required(login_url='admin-panel:admin-login')
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
