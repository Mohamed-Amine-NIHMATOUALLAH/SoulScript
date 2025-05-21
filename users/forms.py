from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Document

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'location', 'birth_date', 'education', 'experience', 'skills']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Parlez de vous en quelques lignes...', 'class': 'form-control'}),
            'education': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Décrivez votre parcours académique...', 
                'class': 'form-control'
            }),
            'experience': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Décrivez vos expériences professionnelles...', 
                'class': 'form-control'
            }),
            'skills': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Listez vos compétences (ex: Python, Django, JavaScript...)', 
                'class': 'form-control'
            }),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }