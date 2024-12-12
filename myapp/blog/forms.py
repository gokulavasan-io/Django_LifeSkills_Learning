from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Category, Post

class ContactForm(forms.Form):
    name=forms.CharField(label="Name",max_length=100,required=True)
    email=forms.EmailField(label="Email",required=True)
    message=forms.CharField(label="Message",required=True)
    
class RegisterForm(forms.ModelForm):
    username=forms.CharField(label="Username",max_length=100,required=True)
    email=forms.CharField(label="Email",max_length=100,required=True)
    password=forms.CharField(label="Password",max_length=100,required=True)
    class Meta:
        model= User
        fields=["username","email","password"]
    


class LoginForm(forms.Form):
    username=forms.CharField(label="Username",max_length=100,required=True)
    password=forms.CharField(label="Password",max_length=100,required=True)
    
    def clean(self):
        cleaned_data=super().clean()
        username=cleaned_data.get("username")
        password=cleaned_data.get("password")
        if username and password:
            user=authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("Invalid username and password")
            

class PostForm(forms.ModelForm):
    title=forms.CharField(label="Title",max_length=200,required=True)
    content=forms.CharField(label="Content",required=True)
    category=forms.ModelChoiceField(label="Category",required=True,queryset=Category.objects.all())
    
    class Meta:
        model=Post
        fields=["title","content","category"]
        
    def clean(self):
        cleaned_data= super().clean()
        title=cleaned_data.get("title")
        content=cleaned_data.get("content")
        
        if title and len(title)<5:
            raise forms.ValidationError("Title must be atleast 5 characters")
        if content and len(content)<10:
            raise forms.ValidationError("Content must be atleast 10 characters")
            
    def save(self, commit = ...):
        post= super().save(commit)
        
        if commit:
            post.save()
        return post
        