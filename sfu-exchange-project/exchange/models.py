from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext as _


class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=65)
    description = models.CharField(max_length=256)
    
    def __str__(self) -> str:
        return self.name

# Create your models here.
class User(AbstractUser):
    bio = models.TextField("Biography", max_length=500, blank=True)
    img = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, blank=True)

    # Relationships 
    faculty_id = models.ForeignKey( Faculty, null=True, on_delete=models.SET_NULL, verbose_name="Faculty")
    roles = models.ManyToManyField(Role)


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    read = models.BooleanField(default=False)
    url = models.CharField(max_length=256)
    notification_text = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    deleted = models.BooleanField(default=False)

    # Relationships
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.notification_text

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name 

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    question_text = models.TextField(max_length=2000, null=False)
    votes = models.IntegerField(default=0, null=False)
    anonymous = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=False)
    last_edited = models.DateTimeField(auto_now_add=True, null=False)
    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('title',))

    # Relationships 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title

    # def save(self):
    #     if not self.id:
    #         self.slug = slugify(self.title)

    #     super(Question, self).save

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    answer_text = models.TextField(max_length=2000, null=False)
    votes = models.IntegerField(default=0, null=False)
    anonymous = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=False)
    last_edited = models.DateTimeField(auto_now_add=True, null=False)

    # Relationships 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Q: {self.question_id}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_text = models.TextField(max_length=2000, null=False)
    votes = models.IntegerField(default=0, null=False)
    anonymous = models.BooleanField(default=False, null=False)
    deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=False)
    last_edited = models.DateTimeField(auto_now_add=True, null=False)

     # Relationships 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"A: {self.answer_id}"