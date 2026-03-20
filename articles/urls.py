# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'  # ← Namespace requis

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='liste'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='detail'),
    path('nouveau/article/', views.ArticleCreateView.as_view(), name='creer'),
    path('<slug:slug>/modifier/', views.ArticleUpdateView.as_view(), name='modifier'),
    path('<slug:slug>/supprimer/', views.ArticleDeleteView.as_view(), name='supprimer'),
]
