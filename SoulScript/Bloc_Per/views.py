from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy  
from datetime import date
from Bloc_Per.models import Utilisateur, Article, Image  
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import ArticleForm
from datetime import date
from django.contrib.auth import authenticate, login as auth_login

app_name = 'Bloc_Per'

class inscription(CreateView):
    model = Utilisateur
    template_name = 'inscription.html'
    fields = ['username', 'prenom', 'nom', 'cne', 'telephone', 'date_naissance', 'email', 'password']
    success_url = reverse_lazy('Bloc_Per:login')

    def form_valid(self, form):
        date_naissance = form.cleaned_data.get('date_naissance')
        if date_naissance:
            age = (date.today() - date_naissance).days // 365
            if age < 18:
                form.add_error('date_naissance', 'Vous devez avoir au moins 18 ans pour vous inscrire.')
                return self.form_invalid(form)

        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        cne = form.cleaned_data.get('cne')
        telephone = form.cleaned_data.get('telephone')
        

        if Utilisateur.objects.filter(email=email).exists():
            form.add_error('email', "Cet email est déjà utilisé.")
            return self.form_invalid(form)
        if Utilisateur.objects.filter(username=username).exists():
            form.add_error('username', "Ce nom d'utilisateur est déjà pris.")
            return self.form_invalid(form)
        if Utilisateur.objects.filter(cne=cne).exists():
            form.add_error('cne', "Ce CNE est déjà enregistré.")
            return self.form_invalid(form)
        if Utilisateur.objects.filter(telephone=telephone).exists():
            form.add_error('telephone', "Ce numéro de téléphone est déjà utilisé.")
            return self.form_invalid(form)
        
        form.instance.password = make_password(form.cleaned_data.get('password') or '')
        return super().form_valid(form)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Utilisateur.objects.get(email=email)

            # Vérifie si le mot de passe est valide
            if user.password and check_password(password, user.password):
                # Authentifie l'utilisateur dans le système de Django
                auth_login(request, user)
                return render(request, 'Home.html', {'username': user.username})
            else:
                return render(request, 'login.html', {'error': 'Mot de passe incorrect'})
        except Utilisateur.DoesNotExist:
            return render(request, 'login.html', {'error': 'Utilisateur non trouvé'})

    return render(request, 'login.html')


def ajout_article(request, username):
    user = Utilisateur.objects.get(username=username)  # Récupérer l'utilisateur
    if request.method == 'POST':
        # Récupérer les données du formulaire personnalisé
        nom = request.POST.get('nom')
        categorie = request.POST.get('Catégorie')
        creation_date = request.POST.get('Création_date')
        description = request.POST.get('Description')
        images = request.FILES.getlist('images')  # Récupérer les fichiers

        # Créer un nouvel article
        article = Article.objects.create(
            username=user,
            nom=nom,
            Catégorie=categorie,
            Création_date=creation_date,
            Description=description,
        )

        # Enregistrer les images associées à l'article
        for image in images:
            Image.objects.create(article=article, image=image)

        # Rediriger après l'ajout
        return redirect('Bloc_Per:articles_personnels', username=username)

    return render(request, 'ajout_article.html', {'user': user})


def articles_personnels(request, username):
    user=Utilisateur.objects.get(username=username)
    articles = Article.objects.filter(username__username=username)  # Correction ici
    images = Image.objects.all()  # Correction pour accéder aux images
    return render(request, 'articles_personnels.html', {'articles': articles, 'images': images , 'user':user})

