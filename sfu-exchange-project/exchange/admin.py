from django.contrib import admin
from .models import Answer, Comment, Notification, Question, Role, Tag, User, Faculty

# Register your models here.
admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Role)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Notification)