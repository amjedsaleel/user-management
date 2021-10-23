# Django
from django.urls import path

# local Django
from .import views

app_name = 'admin-panel'

urlpatterns = [
    path('dashbaord/', views.dashboard, name='dashboard'),
    path('<str:username>/', views.user_profile, name='user-profile')
]