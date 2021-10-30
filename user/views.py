# Django
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    if not request.session.has_key('user'):
        return redirect('accounts:login')

    username = request.session['user']
    user = User.objects.get(username=username)
    print('Username: ', username)

    if not user.is_active:
        del request.session['user']
        return redirect('accounts:login')

    return render(request, 'user/index.html', {'user': user.username})
