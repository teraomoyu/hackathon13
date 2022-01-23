from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Comment


class SignUpForm(UserCreationForm):

    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_content", "time_start", "time_end"]


    
class NewVideoForm(forms.Form):
    
    content = forms.CharField(label='Content', max_length=300)
    file = forms.FileField()

