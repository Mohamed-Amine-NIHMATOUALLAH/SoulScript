from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator,MaxLengthValidator,MinLengthValidator

class Utilisateur (models.Model):
    username = models.CharField(validators=[MaxLengthValidator(50)], unique=True, max_length=50)
    prenom = models.CharField(validators=[MaxLengthValidator(50)], max_length=50)
    nom = models.CharField(validators=[MaxLengthValidator(50)], max_length=50)
    cne = models.CharField(validators=[MinLengthValidator(8),MaxLengthValidator(8)], unique=True, max_length=8)
    telephone = models.CharField(validators=[MaxLengthValidator(10),MinLengthValidator(10)], unique=True, max_length=10)
    date_naissance = models.DateField()
    email = models.EmailField(unique=True, validators=[MaxLengthValidator(50)])
    password = models.CharField(validators=[MinLengthValidator(8),MaxLengthValidator(20)], max_length=20)

class Article (models.Model):
    username=models.ForeignKey(Utilisateur , on_delete=models.CASCADE)
    nom=models.CharField(max_length=255)
    Catégorie=models.CharField(max_length=255)
    Création_date=models.DateField()
    Description=models.TextField()
class Image(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images_article/')
