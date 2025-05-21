# SoulScript - Professional Document Sharing Platform

<div align="center">  
  <br>
  <p><strong>A LinkedIn-inspired platform for professionals to share and manage their career documents</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)](https://www.djangoproject.com/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
  [![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
</div>

---

## 🌟 <a name="features"></a>Features

- 📝 **Content Creation** - Write and share professional articles
- 📁 **Document Management** - Organized storage for CVs, certificates, and diplomas
- 👥 **Detailed Profiles** - Showcase professional skills and experiences
- 💬 **Comment System** - User interaction on publications
- ❤️ **Engagement** - Likes and interaction statistics on articles
- 🏷️ **Categorization** - Organization of content by professional domains
- 🔍 **Advanced Search** - Filtering and discovery of relevant content

## 🚀 <a name="installation"></a>Installation Guide

### Prerequisites

- Python 3.8+
- MySQL/MariaDB
- Git

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/Mohamed-Amine-NIHMATOUALLAH/SoulScript.git
cd SoulScript

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment File

Create a `.env` file in the root directory with the following configurations:

```ini
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=soulscript
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

# Email Configuration (development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Media & Static Files
MEDIA_URL=/media/
STATIC_URL=/static/

# Session Configuration
SESSION_COOKIE_AGE=1209600
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True

# Internationalization
LANGUAGE_CODE=fr-fr
TIME_ZONE=Europe/Paris
```

### Database Setup

```bash
# Create database
mysql -u root -p
CREATE DATABASE soulscript CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# Apply migrations
python manage.py makemigrations
python manage.py migrate
```

### Initialize Data

```bash
# Create superuser
python manage.py createsuperuser

# Create default categories
python create_default_category.py
```

### Run Development Server

```bash
python manage.py runserver
```

Access the application at http://127.0.0.1:8000

## 🛠️ <a name="tech-stack"></a>Tech Stack

### Backend

- **Framework**: Django 5.2.1
- **Database**: MySQL/MariaDB
- **Authentication**: Django Authentication System

### Frontend

- **Structure**: HTML5
- **Styles**: CSS3, Bootstrap 5
- **Interactivity**: JavaScript
- **Text Editor**: Summernote
- **Forms**: Crispy Forms with Bootstrap 5

### Tools & Libraries

- **Image Processing**: Pillow
- **Environment Variables**: python-dotenv
- **DB Connector**: PyMySQL

## 📁 <a name="structure"></a>Structure du Projet

```
SoulScript/
├── articles/                   # Application de gestion des articles
│   ├── migrations/             # Migrations de base de données
│   ├── static/                 # Fichiers statiques spécifiques
│   ├── templates/              # Templates HTML
│   ├── admin.py                # Configuration de l'interface admin
│   ├── apps.py                 # Configuration de l'application
│   ├── forms.py                # Formulaires
│   ├── models.py               # Modèles de données
│   ├── urls.py                 # Configuration des URLs
│   └── views.py                # Vues et logique métier
├── users/                      # Application de gestion des utilisateurs
│   ├── migrations/             # Migrations de base de données
│   ├── templates/              # Templates HTML
│   ├── admin.py                # Configuration de l'interface admin
│   ├── apps.py                 # Configuration de l'application
│   ├── forms.py                # Formulaires
│   ├── models.py               # Modèles de données
│   ├── signals.py              # Signaux Django
│   └── views.py                # Vues et logique métier
├── linkedin_clone/             # Configuration du projet principal
│   ├── settings.py             # Paramètres du projet
│   ├── urls.py                 # URLs du projet
│   ├── asgi.py                 # Configuration ASGI
│   └── wsgi.py                 # Configuration WSGI
├── static/                     # Fichiers statiques globaux
│   ├── css/                    # Feuilles de style
│   ├── js/                     # Scripts JavaScript
│   └── images/                 # Images
├── media/                      # Fichiers uploadés par les utilisateurs
│   ├── profile_pics/           # Photos de profil
│   └── article_images/         # Images des articles
├── templates/                  # Templates HTML globaux
│   ├── base.html               # Template de base
│   └── home.html               # Page d'accueil
├── venv/                       # Environnement virtuel Python
├── .env                        # Variables d'environnement
├── .gitignore                  # Fichiers à ignorer par Git
├── LICENSE                     # Licence du projet
├── README.md                   # Documentation du projet
├── requirements.txt            # Dépendances Python
├── manage.py                   # Script de gestion Django
└── create_default_category.py  # Script d'initialisation des catégories
```

## 📊 <a name="schema"></a>Database Schema

### Users App

**Profile**

- User (OneToOne) - Relation with Django User
- Image - Profile picture
- Bio - Personal description
- Skills - Professional skills
- Professional Title - Job title

### Articles App

**Category**

- Name - Category name
- Slug - URL-friendly identifier
- Created At - Creation date
- Updated At - Last update date

**Article**

- Title - Article title
- Content - Formatted content
- Author (FK → User) - Article author
- Category (FK → Category) - Article category
- Created At - Creation date
- Updated At - Update date
- Likes - Number of likes
- Status - Publication status

**Comment**

- Article (FK → Article) - Commented article
- Author (FK → User) - Comment author
- Content - Comment content
- Created At - Creation date

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test articles
python manage.py test users
```

## 📦 <a name="deployment"></a>Deployment

### Production Environment Configuration

For a production environment, you'll need to modify your settings. Here's a basic checklist:

1. **Security Settings**

   - Set `DEBUG=False`
   - Update `ALLOWED_HOSTS` with your domain
   - Configure HTTPS with SSL certificates
   - Set `SESSION_COOKIE_SECURE=True` and `CSRF_COOKIE_SECURE=True`

2. **Static Files**

   ```bash
   python manage.py collectstatic
   ```

3. **Production Server Setup**

   - Use a production-ready server (Gunicorn, uWSGI)
   - Set up a reverse proxy (Nginx, Apache)
   - Configure process management (Supervisor, systemd)

4. **Database**

   - Use a production database with proper credentials
   - Implement regular backups

5. **Logging**
   - Set up centralized logging
   - Configure error notification

Refer to Django's [deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/) for more details.

## 🔐 Security Measures

- CSRF Protection enabled
- XSS Prevention
- SQL Injection Protection
- Secure Password Hashing
- Session Security
- File Upload Validation

## 🎯 <a name="roadmap"></a>Future Enhancements

- [ ] Real-time notifications
- [ ] Document version control
- [ ] Advanced search filters
- [ ] RESTful API
- [ ] Social authentication (Google, LinkedIn)
- [ ] Document collaboration
- [ ] Analytics dashboard
- [ ] Complete internationalization
- [ ] Companion mobile app
- [ ] Personalized recommendation system

## 💡 Contributing Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow coding standards:
   - PEP 8 for Python
   - Use meaningful variable names
   - Add comments for complex logic
   - Write tests for new features
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📫 <a name="contact"></a>Contact

- GitHub: [@Mohamed-Amine-NIHMATOUALLAH](https://github.com/Mohamed-Amine-NIHMATOUALLAH)
- LinkedIn: [Mohamed Amine NIHMATOUALLAH](https://linkedin.com/in/mohamed-amine-nihmatouallah)
- Project Link: [https://github.com/Mohamed-Amine-NIHMATOUALLAH/SoulScript](https://github.com/Mohamed-Amine-NIHMATOUALLAH/SoulScript)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
