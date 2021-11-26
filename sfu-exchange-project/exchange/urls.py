from django.urls import path
from . import views



urlpatterns = [
    path('', views.LoginView, name='Login'),
    path('exchange/', views.HomeView, name='Home'),
    path('exchange/profile/', views.ProfileView, name='Profile'),
    path('exchange/profile/edit/', views.ProfileEditView, name='Profile Edit'),
    path('exchange/questions/', views.QuestionsView, name='Questions'),
    path('exchange/questions/<int:question_id>/<slug:slug>/', views.QuestionsDetailView, name="Questions Detail"),
]
