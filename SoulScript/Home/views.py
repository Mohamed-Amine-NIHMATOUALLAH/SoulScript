from django.shortcuts import render
from Bloc_Per.models import Utilisateur

def Home_all(request):
        return render(request,'Home.html')

def Home(request, username):
        user=Utilisateur.objects.get(username = username)
        return render(request,'Home.html', {'user': user})
