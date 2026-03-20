# articles/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategorieViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategorieViewSet, basename='categorie')

urlpatterns = [
    path('', include(router.urls)),
]


