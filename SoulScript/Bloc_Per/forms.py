from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['username', 'nom', 'Catégorie', 'Création_date', 'Description']
        widgets = {
            'Création_date': forms.DateInput(attrs={'type': 'date'}),
            'Description': forms.Textarea(attrs={'maxlength': '500'}),
        }