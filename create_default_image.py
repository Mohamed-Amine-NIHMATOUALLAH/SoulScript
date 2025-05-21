import os
from PIL import Image, ImageDraw, ImageFont
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkedin_clone.settings')
django.setup()

from django.conf import settings

def create_default_profile_image():
    # Créer le dossier media s'il n'existe pas
    media_dir = os.path.join(settings.BASE_DIR, 'media')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    
    # Chemin de l'image par défaut
    default_img_path = os.path.join(media_dir, 'default.jpg')
    
    # Vérifier si l'image existe déjà
    if not os.path.exists(default_img_path):
        # Créer une image simple
        img = Image.new('RGB', (300, 300), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        
        # Dessiner un cercle blanc
        d.ellipse((50, 50, 250, 250), fill=(255, 255, 255))
        
        # Ajouter le texte "User" au centre
        try:
            # Essayer de charger une police
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            # Si la police n'est pas disponible, utiliser la police par défaut
            font = ImageFont.load_default()
        
        d.text((120, 150), "User", fill=(0, 0, 0), font=font)
        
        # Sauvegarder l'image
        img.save(default_img_path)
        print(f"Image par défaut créée à {default_img_path}")
    else:
        print(f"L'image par défaut existe déjà à {default_img_path}")

if __name__ == "__main__":
    create_default_profile_image()