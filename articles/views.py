# articles/views.py
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Article, Categorie
from .forms import ArticleForm


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/liste.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(statut='publie').select_related(
            'auteur', 'categorie'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm  # ← Utiliser le form personnalisé
    template_name = 'articles/formulaire.html'

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        messages.success(self.request, "✅ Article créé avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Erreur dans le formulaire.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('articles:detail', kwargs={'slug': self.object.slug})

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm  # ← Utiliser le form personnalisé
    template_name = 'articles/formulaire.html'

    def form_valid(self, form):
        messages.success(self.request, "✅ Article modifié avec succès !")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('articles:detail', kwargs={'slug': self.object.slug})

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/supprimer.html'
    success_url = reverse_lazy('articles:liste')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Article supprimé.")
        return super().delete(request, *args, **kwargs)


# articles/views.py  (ajouter en bas du fichier)
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (ArticleSerializer, ArticleListSerializer,
                          CategorieSerializer)

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'description']
    lookup_field = 'slug'


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('auteur', 'categorie')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]

    # ─── Filtrage par champs ────────────────────────────────────
    filterset_fields = ['statut', 'categorie', 'auteur']

    # ─── Recherche full-text ────────────────────────────────────
    search_fields = ['titre', 'contenu', 'auteur__username']

    # ─── Tri ────────────────────────────────────────────────────
    ordering_fields = ['date_creation', 'titre']
    ordering = ['-date_creation']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Utiliser le serializer allégé pour la liste"""
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def get_queryset(self):
        """Filtrer les articles publiés pour les anonymes"""
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(statut='publie')
        return qs

    # ─── Action personnalisée : mes articles ───────────────────
    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def mes_articles(self, request):
        """GET /api/articles/mes_articles/ → articles de l'utilisateur connecté"""
        articles = Article.objects.filter(auteur=request.user)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
