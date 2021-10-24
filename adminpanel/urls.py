# Django
from django.urls import path

# local Django
from .import views

app_name = 'admin-panel'

urlpatterns = [
    path('', views.admin_login, name='admin-login'),
    path('dashbaord/', views.dashboard, name='dashboard'),
    path('<str:username>/', views.user_profile, name='user-profile'),
    path('update/<str:username>/', views.update_user, name='update-user'),
]
