# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# local Django
from .forms import UpdateUser
# Create your views here.


@login_required
def dashboard(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'admin-panel/dashboard.html', context)


@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'admin-panel/user-profile.html', context)


@login_required
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
