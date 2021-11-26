from django.urls import path
from . import views



urlpatterns = [
    path('', views.LoginView, name='Login'),
    path('exchange/', views.HomeView, name='Home'),
    path('exchange/profile/', views.ProfileView, name='Profile'),
    path('exchange/profile/edit/', views.ProfileEditView, name='Profile Edit'),
    path('exchange/question/', views.QuestionView, name='Question'),
]
