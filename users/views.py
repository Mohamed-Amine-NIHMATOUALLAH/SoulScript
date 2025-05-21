from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DocumentForm
from .models import Profile, Document
from articles.models import Article

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Votre compte a été créé avec succès!')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Votre profil a été mis à jour!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Récupérer tous les articles de l'utilisateur (brouillons inclus)
    user_articles = Article.objects.filter(author=request.user).order_by('-date_posted')
    
    # Statistiques
    total_views = sum(article.views_count for article in user_articles)
    total_likes = sum(article.total_likes() for article in user_articles)
    total_comments = sum(article.total_comments() for article in user_articles)
    
    # Documents
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'articles': user_articles,
        'stats': {
            'views': total_views,
            'likes': total_likes,
            'comments': total_comments,
            'articles': user_articles.count()
        },
        'documents': documents,
        'document_types': Document.DOCUMENT_TYPES
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, f'Votre document a été téléchargé avec succès!')
            return redirect('profile')
    else:
        form = DocumentForm()
    
    return render(request, 'users/upload_document.html', {'form': form})

@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, f'Le document a été supprimé avec succès!')
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # Articles publics de l'utilisateur (exclure les brouillons)
    articles = Article.objects.filter(author=user, is_draft=False).order_by('-date_posted')
    
    # Statistiques
    total_views = sum(article.views_count for article in articles)
    total_likes = sum(article.total_likes() for article in articles)
    total_comments = sum(article.total_comments() for article in articles)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'articles': articles,
        'stats': {
            'views': total_views,
            'likes': total_likes,
            'comments': total_comments,
            'articles': articles.count()
        }
    }
    
    return render(request, 'users/user_profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès!')
    return redirect('home')