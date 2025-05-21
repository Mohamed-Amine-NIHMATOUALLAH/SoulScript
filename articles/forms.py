from django import forms
from .models import Article, Comment, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'categories', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'article'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'categories': forms.CheckboxSelectMultiple(),
            'is_draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == "<p><br></p>":
            return "<p>Contenu par défaut</p>"  # Valeur par défaut pour éviter l'erreur
        return content

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].help_text = "Sélectionnez les catégories professionnelles pertinentes pour votre article."

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Écrivez votre commentaire...', 'class': 'form-control'}),
        }