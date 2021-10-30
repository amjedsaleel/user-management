# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# local Django
from .decorators import user_only

# Create your views here.


@login_required
# @user_only
def index(request):
    return render(request, 'user/index.html')
