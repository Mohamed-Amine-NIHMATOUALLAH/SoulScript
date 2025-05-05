from django.urls import path
from .views import (
    ArticleListView, ArticleDetailView, ArticleCreateView,
    ArticleUpdateView, ArticleDeleteView, like_article,
    filter_by_category, search_articles, add_comment
)
from . import views

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('like/<int:pk>/', views.like_article, name='like-article'),
    path('comment/<int:pk>/', views.add_comment, name='add-comment'),
    path('reply/<int:pk>/', views.add_reply, name='add-reply'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete-comment'),
    path('search/', search_articles, name='search-articles'),  # Ajoutez cette ligne
]