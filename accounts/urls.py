# Django
from django.urls import path

# local Django
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_fun, name='login'),
    path('signup/', views.signup, name='signup')
]
