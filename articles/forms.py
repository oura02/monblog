# articles/forms.py
from django import forms
from django.utils.text import slugify
from .models import Article, Categorie


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'categorie', 'statut', 'slug']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre de l'article (min. 10 caractères)"  # ← guillemets doubles
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': "Contenu de l'article..."  # ← guillemets doubles
            }),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'slug-auto-genere (laisser vide)'
            }),
        }
        labels = {
            'titre': 'Titre',
            'contenu': 'Contenu',
            'categorie': 'Catégorie',
            'statut': 'Statut',
            'slug': 'Slug (URL)',
        }

    def clean_titre(self):
        titre = self.cleaned_data.get('titre', '')
        if len(titre) < 10:
            raise forms.ValidationError(
                "Le titre doit contenir au moins 10 caractères."
            )
        return titre

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        titre = self.cleaned_data.get('titre', '')

        if not slug:
            slug = slugify(titre)

        qs = Article.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "Ce slug est déjà utilisé. Choisissez-en un autre."
            )
        return slug