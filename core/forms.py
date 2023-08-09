from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Profile, Comment, Category, ArticlePost
from tinymce.widgets import TinyMCE



# Signup Form form Usercreationform
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
           'first_name', 'last_name', 'username', 'email', 'password1', 'password2',
        ]
    
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'First Name*',
    }))
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Last Name*',
    }))
    username = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Username*',
    }))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Email*',
    }))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'password*',
    }))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'confirm password*',
    }))

# login form using Authentication Form
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Username',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Password',
    }))

# Model Form for creating post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content_text',  'content_image', 'content_file']

    content_text = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your post content...',
        'rows': 3
    }))
    content_image = forms.ImageField(required=False, label='choose image', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control-file form-control border p-2 bg-light rounded'
    }))
    content_file = forms.FileField(required=False, label='choose file', widget=forms.FileInput(attrs={
        'class': 'custom-file-input form-control border p-2 bg-light rounded'
    }))

# Model form to add profile details
class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'contact', 'city']
    
    profile_pic = forms.ImageField(required=False, label='choose profile', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control p-2 border bg-light rounded'
    }))
    bio = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe Yourself..',
        'rows': 3
    }))
    contact = forms.CharField(required=False, label='Enter Contact No', widget=forms.NumberInput(attrs={
        'class':'form-control'
    }))
    city = forms.CharField(required=False, label='Enter Address', widget=forms.TextInput(attrs={
        'class':'form-control'
    }))

# simple form for adding comment in post
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text',]
    
    comment_text = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Write Your comment Here..',
        'rows': 2
    }))


# Modelform for creating ArticlePost
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('category','title', 'content',)

    
    content = forms.CharField(widget=TinyMCE())
    title = forms.CharField(required=False, label='Title of Article', widget=forms.TextInput(attrs={
        'class':'form-control  p-2 border-dark bg-light rounded '
    }))
    

