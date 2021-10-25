# Django
from django.urls import path

# local Django
from .import views

app_name = 'admin-panel'

urlpatterns = [
    path('', views.admin_login, name='admin-login'),
    path('dashbaord/', views.dashboard, name='dashboard'),
    path('search/', views.search_user, name='search-user'),
    path('<str:username>/', views.user_profile, name='user-profile'),
    path('update/<str:username>/', views.update_user, name='update-user'),
    path('delete/<str:username>/', views.delete_user, name='delete-user'),
    path('block-user/<int:pk>/', views.block_user, name='block-user'),
    path('unblock_user/<int:pk>/', views.unblock_user, name='unblock-user')
]
