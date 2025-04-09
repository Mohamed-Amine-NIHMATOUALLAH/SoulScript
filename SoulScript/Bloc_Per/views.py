from django.shortcuts import redirect, render
from django.urls import reverse_lazy  
from Bloc_Per.models import Utilisateur  
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import CreateView
app_name = 'Bloc_Per'
class inscription (CreateView):
    model = Utilisateur
    template_name = 'inscription.html'
    fields = ['prenom','nom','cne','telephone','date_naissance','email','password']

    def form_invalid(self, form):
        if Utilisateur.objects.filter(email=form.instance.email).exists():
            return render(self.request, 'inscription.html', {'error': 'Cet email est déjà utilisé.'})
        return super().form_invalid(form)
    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)  # Hash the password before saving
        return super().form_valid(form)
    success_url = reverse_lazy('Bloc_Per:login')  # Redirect to the login page after successful registration


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user= Utilisateur.objects.get(email=email)
            if check_password(password, user.password):
                return redirect('articles_personnels')
            else:
                return render(request,'login.html',{'error':'Mot de passe incorrect'})
        except Utilisateur.DoesNotExist:
            return render(request,'login.html',{'error':'Utilisateur non trouvé'})
    return render(request,'login.html')

def ajout_article(requeste):
    return render(requeste,'ajout_article.html')
def articles_personnels(request):
    return render(request,'articles_personnels.html')
def profil(request):
    return render(request,'profil.html')
