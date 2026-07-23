from django.urls import path, include
from rest_framework import routers
from pokedex.auth_view import CustomTokenView
from .views import PokemonViewSet, TrainerViewSet
from .views import PokemonViewSet, RegisterView

router = routers.DefaultRouter()
router.register(r'pokemons', PokemonViewSet, basename='pokemon')
router.register(r'trainers', TrainerViewSet, basename='trainer')

urlpatterns = [
    path('oauth/token/', CustomTokenView.as_view(), name='oauth2_token'),
    path('register/', RegisterView.as_view(), name='api-register'),
    path('', include(router.urls)),
]