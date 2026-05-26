from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pokemon/<int:id>/', views.pokemon, name='pokemon'),
    path('trainer/<int:id>/', views.trainer, name='trainer'),
    path('pokemon/edit/<int:id>/', views.edit_pokemon, name='edit_pokemon'),
    path('pokemon/delete/<int:id>/', views.delete_pokemon, name='delete_pokemon'),
    path('trainer/edit/<int:id>/', views.edit_trainer, name='edit_trainer'),
    path('trainer/delete/<int:id>/', views.delete_trainer, name='delete_trainer'),
]