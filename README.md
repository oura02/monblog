# MonBlog — Application de Gestion de Blog

Application web complète développée avec **Django** et **Django REST Framework**.

## Technologies utilisées
- Python 3.12 / Django 6.0
- Django REST Framework (API REST)
- SQLite
- Bootstrap 5

## Fonctionnalités
- CRUD complet des articles et catégories
- Authentification (connexion / déconnexion)
- Validation personnalisée des formulaires
- API REST avec filtrage et recherche
- Interface d'administration Django
- Pagination (10 articles par page)

## Installation
git clone https://github.com/TON_USERNAME/monblog.git
cd monblog
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Accès
- Blog : http://127.0.0.1:8000/
- Admin : http://127.0.0.1:8000/admin/
- API : http://127.0.0.1:8000/api/

## Auteur
KONAN ROMEO OURA — BTS Développeur d'Applications
