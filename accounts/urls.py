# Django
from django.urls import path

# local Django
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_fun, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_sign_out, name='logout'),
    path('admin-logout/', views.admin_sign_out, name='admin-logout')
]
