import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Article, Comment, Like, Category
from .forms import ArticleForm, CommentForm

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/home.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_template_names(self):
        # Vérifier si l'utilisateur est authentifié
        if self.request.user.is_authenticated:
            return [self.template_name]
        else:
            return ['articles/welcome.html']
    
    def get_queryset(self):
        queryset = Article.objects.filter(is_draft=False)
        
        # Filtrer par catégorie
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filtrer par date
        date_filter = self.request.GET.get('date')
        if date_filter:
            today = datetime.now().date()
            if date_filter == 'today':
                queryset = queryset.filter(date_posted__date=today)
            elif date_filter == 'week':
                week_ago = today - timedelta(days=7)
                queryset = queryset.filter(date_posted__date__gte=week_ago)
            elif date_filter == 'month':
                month_ago = today - timedelta(days=30)
                queryset = queryset.filter(date_posted__date__gte=month_ago)
            elif date_filter == 'year':
                year_ago = today - timedelta(days=365)
                queryset = queryset.filter(date_posted__date__gte=year_ago)
        
        # Trier par date de publication (du plus récent au plus ancien)
        return queryset.order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        # Ajouter les filtres actifs au contexte
        category_slug = self.request.GET.get('category', '')
        context['active_category'] = category_slug
        context['active_date'] = self.request.GET.get('date', '')
        
        # Ajouter l'objet catégorie active si disponible
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        # Ajouter les filtres actifs au contexte
        context['active_category'] = self.request.GET.get('category', '')
        context['active_date'] = self.request.GET.get('date', '')
        
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Incrémenter le compteur de vues
        article.views_count += 1
        article.save()
        
        # Vérifier si l'utilisateur a aimé l'article
        if self.request.user.is_authenticated:
            context['liked'] = Like.objects.filter(article=article, user=self.request.user).exists()
        
        context['comments'] = article.comments.all().order_by('-date_posted')
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        article = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'Votre commentaire a été ajouté!')
        
        return redirect('article-detail', pk=article.pk)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Votre article a été créé avec succès!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create_article.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Votre article a été mis à jour avec succès!')
        return super().form_valid(form)
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Votre article a été supprimé avec succès!')
        return super().delete(request, *args, **kwargs)



def filter_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    articles = Article.objects.filter(categories=category, is_draft=False).order_by('-date_posted')
    
    # Filtrer par date si nécessaire
    date_filter = request.GET.get('date')
    if date_filter:
        today = datetime.now().date()
        if date_filter == 'today':
            articles = articles.filter(date_posted__date=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            articles = articles.filter(date_posted__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            articles = articles.filter(date_posted__date__gte=month_ago)
        elif date_filter == 'year':
            year_ago = today - timedelta(days=365)
            articles = articles.filter(date_posted__date__gte=year_ago)
    
    return render(request, 'articles/home.html', {
        'articles': articles,
        'categories': Category.objects.all(),
        'active_category': category.slug,
        'active_date': request.GET.get('date', ''),
        'current_category': category  # Passer l'objet catégorie complet
    })

def search_articles(request):
    query = request.GET.get('q', '')
    
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct().order_by('-date_posted')
    else:
        articles = Article.objects.none()
    
    return render(request, 'articles/search_results.html', {
        'articles': articles,
        'query': query,
        'categories': Category.objects.all()
    })

@login_required
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    like, created = Like.objects.get_or_create(article=article, user=request.user)
    
    if not created:
        # L'utilisateur a déjà aimé l'article, donc on supprime le like
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': article.total_likes()
    })

@login_required
def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if content:
            comment = Comment.objects.create(
                article=article,
                author=request.user,
                content=content
            )
            
            return JsonResponse({
                'success': True,
                'author': comment.author.get_full_name() or comment.author.username,
                'author_image': comment.author.profile.image.url,
                'content': comment.content,
                'date_posted': comment.date_posted.strftime('%d/%m/%Y %H:%M'),
                'total_comments': article.comments.count()
            })
    
    return JsonResponse({'success': False}, status=400)

@login_required
def add_reply(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = get_object_or_404(Comment, id=pk)
        
        # Créer la réponse
        reply = Comment(
            article=comment.article,
            author=request.user,
            content=data['content'],
            parent=comment
        )
        reply.save()
        
        return JsonResponse({
            'success': True,
            'author': request.user.get_full_name() or request.user.username,
            'author_username': request.user.username,
            'author_image': request.user.profile.image.url,
            'content': data['content'],
            'reply_id': reply.id
        })
    
    return JsonResponse({'success': False})

@login_required
def delete_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        
        # Vérifier que l'utilisateur est l'auteur du commentaire
        if comment.author != request.user:
            return JsonResponse({'success': False, 'error': 'Vous n\'êtes pas autorisé à supprimer ce commentaire'}, status=403)
        
        # Supprimer le commentaire
        article = comment.article
        comment.delete()
        
        # Mettre à jour le nombre total de commentaires
        total_comments = article.comments.count()
        
        return JsonResponse({
            'success': True,
            'total_comments': total_comments
        })
    
    return JsonResponse({'success': False})

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment

@login_required
def add_reply(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = get_object_or_404(Comment, id=pk)
        
        # Créer la réponse
        reply = Comment(
            article=comment.article,
            author=request.user,
            content=data['content'],
            parent=comment
        )
        reply.save()
        
        return JsonResponse({
            'success': True,
            'author': request.user.get_full_name() or request.user.username,
            'author_username': request.user.username,
            'author_image': request.user.profile.image.url,
            'content': data['content'],
            'reply_id': reply.id
        })
    
    return JsonResponse({'success': False})

@login_required
def delete_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        
        # Vérifier que l'utilisateur est l'auteur du commentaire
        if comment.author != request.user:
            return JsonResponse({'success': False, 'error': 'Vous n\'êtes pas autorisé à supprimer ce commentaire'}, status=403)
        
        # Supprimer le commentaire
        article = comment.article
        comment.delete()
        
        # Mettre à jour le nombre total de commentaires
        total_comments = article.comments.count()
        
        return JsonResponse({
            'success': True,
            'total_comments': total_comments
        })
    
    return JsonResponse({'success': False})