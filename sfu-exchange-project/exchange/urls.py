from django.urls import path
from . import views



urlpatterns = [
    path('', views.LoginView, name='Login'),
    path('exchange/', views.HomeView, name='Home'),
    path('exchange/register/', views.RegisterView, name='Register'),
    path('exchange/profile/', views.ProfileView, name='Profile'),
    path('exchange/profile/edit/', views.ProfileEditView, name='Profile Edit'),
    path('exchange/users/', views.UsersView, name="Users"),
    path('exchange/tags/', views.TagsView, name="Tags"),
    path('exchange/questions/', views.QuestionsView, name='Questions'),
    path('exchange/questions/add', views.QuestionSubmitView, name='Submit Question'),
    # path('exchange/questions/<int:question_id>/<slug:slug>/', views.QuestionsDetailView, name="Questions Detail"),
    path('exchange/questions/<int:question_id>/', views.QuestionsDetailView, name="Questions_Detail"),
]
