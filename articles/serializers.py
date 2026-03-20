# articles/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Categorie


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorieSerializer(serializers.ModelSerializer):
    nombre_articles = serializers.SerializerMethodField()

    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'slug', 'description', 'nombre_articles']
        read_only_fields = ['slug']

    def get_nombre_articles(self, obj):
        return obj.articles.filter(statut='publie').count()


class ArticleSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True)
    categorie_detail = CategorieSerializer(source='categorie', read_only=True)
    categorie = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(), write_only=True, allow_null=True
    )

    class Meta:
        model = Article
        fields = [
            'id', 'titre', 'slug', 'contenu',
            'auteur', 'categorie', 'categorie_detail',
            'statut', 'date_creation', 'date_modification'
        ]
        read_only_fields = ['slug', 'date_creation', 'date_modification', 'auteur']

    def validate_titre(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Le titre doit contenir au moins 10 caractères."
            )
        return value

    def create(self, validated_data):
        validated_data['auteur'] = self.context['request'].user
        return super().create(validated_data)


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer allégé pour la liste (performances)"""
    auteur_nom = serializers.CharField(source='auteur.username', read_only=True)
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'titre', 'slug', 'auteur_nom',
                  'categorie_nom', 'statut', 'date_creation']
