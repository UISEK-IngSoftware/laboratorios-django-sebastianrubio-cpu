from django.urls import path, include
from rest_framework import routers
from pokedex.auth_view import CustomTokenView
from .views import PokemonViewSet, TrainerViewSet

router = routers.DefaultRouter()
router.register(r'pokemons', PokemonViewSet, basename='pokemon')
router.register(r'trainers', TrainerViewSet, basename='trainer')

urlpatterns = [
    path('oauth/token/', CustomTokenView.as_view(), name='oauth2_token'),
    path('', include(router.urls)),
]