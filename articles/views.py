import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Article, Comment, Like, Category, CommentLike
from .forms import ArticleForm, CommentForm
from django.db.models import Count 
from django.contrib.auth.models import User 
from django.template.loader import render_to_string 
from django.http import JsonResponse 

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/home.html' # Ou votre template principal
    context_object_name = 'articles'
    paginate_by = 10 # Définissez le nombre d'articles par "page" pour le chargement infini

    def get_queryset(self):
        return Article.objects.filter(is_draft=False).order_by('-date_posted')

    def get(self, request, *args, **kwargs):
        # Si c'est une requête AJAX pour charger plus d'articles
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            # Rendre uniquement les articles sous forme de fragment HTML
            # Supposons que vous avez un template partiel _article_item.html
            # ou que vous itérez sur page_obj.object_list dans le template principal
            # et que le JS peut extraire les nouveaux items.
            
            # Option 1: Renvoyer un fragment HTML (plus simple si le JS peut l'insérer)
            # Vous devrez peut-être ajuster cela pour rendre une liste d'items.
            # Pour cet exemple, nous allons supposer que le template home.html peut gérer cela
            # via une inclusion conditionnelle ou que le JS est assez intelligent.
            # Une approche plus propre serait de rendre un template spécifique pour les items AJAX.
            
            page_num = request.GET.get('page')
            paginator = context['paginator']
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                return HttpResponse('') # Plus de pages
            
            # Créez un template dédié pour les items chargés via AJAX pour plus de propreté
            # Par exemple: 'articles/_ajax_article_items.html'
            # html = render_to_string('articles/_ajax_article_items.html', {'articles': page_obj.object_list, 'user': request.user})
            # return HttpResponse(html)
            
            # Pour cet exemple, nous allons juste renvoyer une indication si plus de pages existent
            # Le JS devra être plus intelligent pour extraire les articles de la page complète
            # ou vous devez créer un endpoint qui renvoie juste les articles.
            # Pour simplifier, nous allons supposer que le JS demande la page suivante et extrait les articles.
            # Si la page demandée n'a pas d'articles, le JS saura s'arrêter.
            # Une meilleure approche est un endpoint dédié qui renvoie du JSON ou un fragment HTML.
            
            # Pour une implémentation plus robuste, envisagez un endpoint séparé pour AJAX.
            # Ici, nous allons juste laisser le template principal gérer la pagination et le JS extraire.
            pass # Laisser la vue normale gérer la pagination, le JS fera une requête GET normale pour la page suivante

        return super().get(request, *args, **kwargs)
    
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return [self.template_name]
        else:
            return ['articles/welcome.html']
    
    def get_queryset(self):
        queryset = Article.objects.filter(is_draft=False)
        
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
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
        
        return queryset.order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.request.GET.get('category', '')
        context['active_date'] = self.request.GET.get('date', '')
        
        if context['active_category']:
            context['current_category'] = get_object_or_404(Category, slug=context['active_category'])
        
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        article.views_count += 1
        article.save()
    
        context['liked'] = self.request.user.is_authenticated and Like.objects.filter(article=article, user=self.request.user).exists()
        # Optimisation ici
        context['comments'] = article.comments.filter(parent__isnull=True).select_related('author', 'author__profile').prefetch_related('replies__author__profile', 'replies__comment_likes__user', 'comment_likes__user').order_by('-date_posted')
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.all()
        context['related_articles'] = Article.objects.filter(categories__in=article.categories.all(), is_draft=False).exclude(id=article.id).distinct()[:5]
        
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
        print("Formulaire valide, sauvegarde en cours")
        print("Données du formulaire:", form.cleaned_data)
        form.instance.author = self.request.user
        messages.success(self.request, 'Votre article a été créé avec succès!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Formulaire invalide:", form.errors)
        print("Données reçues:", self.request.POST)
        messages.error(self.request, 'Erreur dans le formulaire. Vérifiez les champs.')
        return super().form_invalid(form)
    
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
        'current_category': category
    })

def search_articles(request):
    query = request.GET.get('q', '')
    author_username = request.GET.get('author', '')
    date_filter = request.GET.get('date_filter', '') 
    sort_by = request.GET.get('sort_by', '-date_posted') # Valeurs possibles: 'likes', 'comments', '-date_posted'

    articles = Article.objects.filter(is_draft=False) # Commencer avec tous les articles non brouillons

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()

    if author_username:
        articles = articles.filter(author__username__iexact=author_username)

    if date_filter:
        today = datetime.now().date()
        if date_filter == 'today':
            articles = articles.filter(date_posted__date=today)
        elif date_filter == 'week':
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            articles = articles.filter(date_posted__date)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            articles = articles.filter(date_posted__date__gte=month_ago)
        elif date_filter == 'year':
            year_ago = today - timedelta(days=365)
            articles = articles.filter(date_posted__date__gte=year_ago)
    
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
        like.delete()
    
    # 'liked' peut être déterminé par 'created' directement
    return JsonResponse({
        'success': True,
        'liked': created, # True si créé (liké), False si existait (et donc supprimé/unliké)
        'total_likes': article.total_likes() # Assurez-vous que total_likes est recalculé après la suppression
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
                'comment_id': comment.id,
                'author': comment.author.get_full_name() or comment.author.username,
                'author_username': comment.author.username,
                'author_image': comment.author.profile.image.url,
                'content': comment.content,
                'date_posted': comment.date_posted.strftime('%d/%m/%Y %H:%M'),
                'total_comments': article.comments.count()
            })
    
    return JsonResponse({'success': False, 'error': 'Contenu vide ou méthode non autorisée'}, status=400)

@login_required
def add_reply(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = get_object_or_404(Comment, id=pk)
        
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({'success': False, 'error': 'Contenu vide'}, status=400)
        
        reply = Comment.objects.create(
            article=comment.article,
            author=request.user,
            content=content,
            parent=comment
        )
        
        return JsonResponse({
            'success': True,
            'reply_id': reply.id,
            'author': request.user.get_full_name() or request.user.username,
            'author_username': request.user.username,
            'author_image': request.user.profile.image.url,
            'content': content,
            'can_delete': True
        })
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=400)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'success': True,
        'liked': liked,
        'total_likes': comment.comment_likes.count()
    })

@login_required
def delete_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        
        if comment.author != request.user:
            return JsonResponse({'success': False, 'error': 'Vous n\'êtes pas autorisé à supprimer ce commentaire'}, status=403)
        
        article = comment.article
        comment.delete()
        
        return JsonResponse({
            'success': True,
            'total_comments': article.comments.count()
        })
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=400)
