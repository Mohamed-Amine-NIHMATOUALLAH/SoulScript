import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkedin_clone.settings')
django.setup()

from articles.models import Category

# Créer une catégorie par défaut si elle n'existe pas déjà
if not Category.objects.filter(name='Général').exists():
    Category.objects.create(name='Général', slug='general')
    print("Catégorie 'Général' créée avec succès.")
else:
    print("La catégorie 'Général' existe déjà.")