from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='exchange/login.html'), name='Login'),
    path('exchange/', views.QuestionsView, name='Home'),
    path('exchange/register/', views.RegisterView, name='Register'),
    path('exchange/profile/', views.ProfileView, name='Profile'),
    path('exchange/profile/edit/', views.ProfileEditView, name='Profile Edit'),
    path('exchange/users/', views.UsersView, name="Users"),
    path('exchange/user/<str:username>', views.UsersView, name="User"),
    path('exchange/search/', views.SearchView, name='Search'),
    path('exchange/tags/', views.TagsView, name='Tags'),
    path('exchange/questions/ask', views.QuestionSubmitView, name='Submit_Question'),
    path('exchange/questions/<int:question_id>/<slug:slug>/', views.QuestionsDetailView, name='Questions_Detail'),
    path('exchange/questions/<int:question_id>/<slug:slug>/upvote', views.QuestionUpvote, name='Question_Upvote'),
    path('exchange/questions/<int:question_id>/<slug:slug>/downvote', views.QuestionDownvote, name='Question_Downvote'),
    path('exchange/answers/upvote/<int:answer_id>', views.AnswerUpvote, name='Answer_Upvote'),
    path('exchange/answers/downvote/<int:answer_id>', views.AnswerDownvote, name='Answer_Downvote'),
]
