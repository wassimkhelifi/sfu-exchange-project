from django.contrib import admin
from .models import Answer, Comment, Notification, Question, Role, Tag, User, Faculty
from django_summernote.admin import SummernoteModelAdmin


class QuestionAdmin(SummernoteModelAdmin):
    summernote_fields = ('question_text',)

class AnswerAdmin(SummernoteModelAdmin):
    summernote_fields = ('answer_text',)

# Register your models here.
admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Role)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Comment)
admin.site.register(Notification)