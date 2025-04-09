from . import views
from django.urls import path
urlpatterns=[
    path('inscription/', views.inscription.as_view(), name='inscription'),
    path('login/', views.login, name='login'),
    path('ajout_article/', views.ajout_article, name='ajout_article'),
    path('articles_personnels/', views.articles_personnels, name='articles_personnels'),
    path('profil/', views.profil, name='profil'),
]
