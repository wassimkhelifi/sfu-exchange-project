from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include, path

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='exchange/login.html', redirect_authenticated_user=True), name='Login'),
    path('exchange/', views.QuestionsView, name='Home'),
    path('exchange/register/', views.RegisterView, name='Register'),
    path('exchange/profile/', views.ProfileView, name='Profile'),
    path('exchange/profile/edit/', views.ProfileEditView, name='Profile Edit'),
    path('exchange/users/', views.UsersView, name="Users"),
    path('exchange/users/<int:user_id>/<str:user_username>', views.UsersDetailView, name="Users_Detail"),
    path('exchange/tags/', views.TagsView, name='Tags'),
    path('exchange/notifications', views.NotificationsView, name='Notifications'),
    path('exchange/questions/ask/', views.QuestionSubmitView, name='Submit_Question'),
    path('exchange/questions/ask/<int:id>/', views.QuestionSubmitView, name='Edit_Question'),
    path('exchange/questions/<int:question_id>/<slug:slug>/', views.QuestionsDetailView, name='Questions_Detail'),
    path('exchange/questions/<int:question_id>/<slug:slug>/upvote', views.QuestionUpvote, name='Question_Upvote'),
    path('exchange/questions/<int:question_id>/<slug:slug>/downvote', views.QuestionDownvote, name='Question_Downvote'),
    path('exchange/questions/<int:question_id>/<slug:slug>/<int:notification_id>', views.QuestionsDetailView, name="Questions_Detail_Notification"),
    path('exchange/answers/upvote/<int:answer_id>', views.AnswerUpvote, name='Answer_Upvote'),
    path('exchange/answers/downvote/<int:answer_id>', views.AnswerDownvote, name='Answer_Downvote'),
]
