# articles/admin.py
from django.contrib import admin
from .models import Article, Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ['nom']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'statut', 'date_creation']
    list_filter = ['statut', 'categorie', 'auteur']
    search_fields = ['titre', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
    list_editable = ['statut']
    date_hierarchy = 'date_creation'
    ordering = ['-date_creation']
