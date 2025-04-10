from django.shortcuts import redirect, render
from django.urls import reverse_lazy  
from datetime import date
from Bloc_Per.models import Utilisateur, Article, Image  
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import CreateView
from .forms import ArticleForm
from datetime import date
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

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Utilisateur.objects.get(email=email)

            # Vérifie si le mot de passe est bien haché et valide
            if user.password and check_password(password, user.password):
                # Tu peux stocker l'ID dans la session par exemple
                request.session['user_id'] = user.id
                return render(request, 'Home.html', {'username': user.username})
            else:
                return render(request, 'login.html', {'error': 'Mot de passe incorrect'})
        except Utilisateur.DoesNotExist:
            return render(request, 'login.html', {'error': 'Utilisateur non trouvé'})

    return render(request, 'login.html')


def ajout_article(request,username):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_articles')  # à adapter selon ton URL
    else:
        form = ArticleForm()
    return render(request, 'ajout_article.html', {'form': form})


def articles_personnels(request,username):
    Article=Article.objects.filter(username=username)
    images=Image.image_set.all()
    return render(request,'articles_personnels.html', {'articles': Article, 'images': images})


def profil(request, username):
    
    user = Utilisateur.objects.get(username=username)
    error = None
    success = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            # Mettre à jour les informations personnelles
            cne = request.POST.get('cne', user.cne)  # Utiliser la valeur actuelle si non fournie
            nom = request.POST.get('nom', user.nom)
            prenom = request.POST.get('prenom', user.prenom)
            new_username = request.POST.get('username', user.username)
            email = request.POST.get('email', user.email)
            telephone = request.POST.get('telephone', user.telephone)

            # Vérifier les conflits avec d'autres utilisateurs
            if email != user.email and (Utilisateur.objects.filter(email=email).exists() or Fournisseur.objects.filter(email=email).exists()):
                error = "L'email existe déjà."
            elif telephone != user.telephone and (Utilisateur.objects.filter(phone_number=phone_number).exists() or Fournisseur.objects.filter(phone_number=phone_number).exists()):
                error = "Le numéro de téléphone existe déjà."
            elif new_username != user.username and (Utilisateur.objects.filter(username=new_username).exists() or Fournisseur.objects.filter(username=new_username).exists()):
                error = "Le nom d'utilisateur existe déjà."
            else:
                # Mettre à jour les informations personnelles
                user.cne = cne
                user.nom = nom
                user.prenom = prenom
                user.username = new_username
                user.email = email
                user.telephone =telephone
                user.save()
                success = "Informations mises à jour avec succès."

        

    return render(request, 'profil.html', {'user': user, 'error': error, 'success': success})
