from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


class Faculty(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=65)
    descrption = models.CharField(max_length=256)


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    img = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, blank=True)

    # Relationships 
    faculty_id = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    roles = models.ManyToManyField(Role)


class Notification(models.Model):
    id = models.IntegerField(primary_key=True)
    read = models.BooleanField(default=False)
    url = models.CharField(max_length=256)
    notification_text = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    deleted = models.BooleanField(default=False)

    # Relationships
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    question_text = models.TextField(max_length=2000, null=False)
    votes = models.IntegerField(default=0, null=False)
    anonymous = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=False)
    last_edited = models.DateTimeField(auto_now_add=True, null=False)

    # Relationships 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    answer_text = models.TextField(max_length=2000, null=False)
    votes = models.IntegerField(default=0, null=False)
    anonymous = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=False)
    last_edited = models.DateTimeField(auto_now_add=True, null=False)

    # Relationships 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    comment_text = models.TextField(max_length=2000, null=False)
    votes = models.IntegerField(default=0, null=False)
    anonymous = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=False)
    last_edited = models.DateTimeField(auto_now_add=True, null=False)

     # Relationships 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
