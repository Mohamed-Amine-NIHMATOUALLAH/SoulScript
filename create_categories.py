import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkedin_clone.settings')
django.setup()

from articles.models import Category

# Liste des catégories professionnelles
categories = [
    "Certificat",
    "Diplôme",
    "CV",
    "Lettre de motivation",
    "Stage",
    "Accréditation professionnelle",
    "Autre"
]

# Créer les catégories si elles n'existent pas déjà
for category_name in categories:
    slug = slugify(category_name)
    if not Category.objects.filter(slug=slug).exists():
        Category.objects.create(name=category_name, slug=slug)
        print(f"Catégorie '{category_name}' créée avec succès.")
    else:
        print(f"La catégorie '{category_name}' existe déjà.")

print("Toutes les catégories ont été créées.")