# Django
from django.shortcuts import render, redirect
from django.contrib import messages

# local Django
from .decorators import user_only

# Create your views here.


def index(request):
    if not request.session.has_key('user'):
        return redirect('accounts:login')
    return render(request, 'user/index.html')
