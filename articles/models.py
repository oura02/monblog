# articles/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']


class Article(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='articles')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='articles')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES,
                              default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_publication = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_creation']
