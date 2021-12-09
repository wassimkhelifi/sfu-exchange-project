from django import forms
from .models import User, Tag
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404

class RegistrationForm(UserCreationForm):
    bio = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=150)
    # TODO: Max length of stackoverflow body is 30k characters, need to change model limit. : https://meta.stackexchange.com/questions/176445/knowing-your-limits-what-is-the-maximum-length-of-a-question-title-post-image
    question_text = forms.CharField(max_length=3000)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    user_id = 1
    
    # TODO: Potentially provide validation if needed, otherwise we can remove these functions
    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean_questions_text(self):
        data = self.cleaned_data['question_text']
        return data