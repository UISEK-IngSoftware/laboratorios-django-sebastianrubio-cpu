from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'pokedex'
urlpatterns = [
    path('pokemon/<int:id>/', views.pokemon, name='pokemon'),
    path('', views.index, name='index'),
    path('trainer/<int:id>/', views.trainer, name='trainer'),
    path('pokemon/edit/<int:id>/', views.edit_pokemon, name='edit_pokemon'),
    path('pokemon/delete/<int:id>/', views.delete_pokemon, name='delete_pokemon'),
    path('trainer/edit/<int:id>/', views.edit_trainer, name='edit_trainer'),
    path('trainer/delete/<int:id>/', views.delete_trainer, name='delete_trainer'),
    path('login/', views.CustomLogInView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pokedex:index'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('pokemon/add/', views.add_pokemon, name='add_pokemon'),
    path('pokemon/<int:id>/', views.pokemon, name='pokemon'),
    path('', views.index, name='index'),
]