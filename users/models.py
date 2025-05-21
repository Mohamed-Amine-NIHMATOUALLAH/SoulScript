from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from django.conf import settings

# Ajouter ce champ au modèle Profile
class Profile(models.Model):
    # Champs existants
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    
    # Nouveau champ pour les abonnements
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        # Appeler la méthode save du parent
        super().save(*args, **kwargs)
        
        # Vérifier si l'image existe et la redimensionner
        if self.image and os.path.isfile(self.image.path):
            img = Image.open(self.image.path)
            
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Document(models.Model):
    DOCUMENT_TYPES = (
        ('certificat', 'Certificat'),
        ('diplome', 'Diplôme'),
        ('cv', 'CV'),
        ('lettre_motivation', 'Lettre de motivation'),
        ('stage', 'Stage'),
        ('accreditation', 'Accréditation professionnelle'),
        ('autre', 'Autre'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:].upper()
    
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:].upper()

# Ajouter ce modèle pour les notifications
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'J\'aime'),
        ('comment', 'Commentaire'),
        ('follow', 'Abonnement'),
        ('mention', 'Mention'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('articles.Comment', on_delete=models.CASCADE, null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} {self.get_notification_type_display()} - {self.created_at.strftime('%d/%m/%Y')}"