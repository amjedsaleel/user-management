# Django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def dashboard(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'admin-panel/dashboard.html', context)


def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'admin-panel/user-profile.html', context)
