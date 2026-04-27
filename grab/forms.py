from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Profile,Post
from django import forms

class signupform(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'social-input','placeholder':'Enter your username'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'social-input','placeholder':'Enter your E-mail'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'social-input','placeholder':'Enter your password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'social-input','placeholder':'Re-Enter your password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'social-input'}),
            'bio': forms.Textarea(attrs={'class': 'social-input social-textarea', 'rows': 4, 'placeholder': 'Tell people what you create, think, or share.'}),
        }

class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'content','post_image']  
        widgets = {
            'topic': forms.Select(attrs={'class': 'social-input'}),
            'content': forms.Textarea(attrs={'class': 'social-input social-textarea', 'rows': 5, 'placeholder': 'What story are you sharing today?'}),
            'post_image': forms.ClearableFileInput(attrs={'class': 'social-input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'comment-input', 'placeholder': 'Write a comment...'}),
        }

    
