from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class Utilisateur(AbstractBaseUser):
    username = models.CharField(validators=[MaxLengthValidator(50)], unique=True, max_length=50)
    prenom = models.CharField(validators=[MaxLengthValidator(50)], max_length=50)
    nom = models.CharField(validators=[MaxLengthValidator(50)], max_length=50)
    cne = models.CharField(validators=[MinLengthValidator(8), MaxLengthValidator(8)], unique=True, max_length=8)
    telephone = models.CharField(validators=[MaxLengthValidator(10), MinLengthValidator(10)], unique=True, max_length=10)
    date_naissance = models.DateField()
    email = models.EmailField(unique=True, validators=[MaxLengthValidator(50)])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['username']  # Fields required when creating a superuser

    def __str__(self):
        return self.email

class Article(models.Model):
    username = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    Catégorie = models.CharField(max_length=255)
    Création_date = models.DateField()
    Description = models.TextField()

class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images_article/')
