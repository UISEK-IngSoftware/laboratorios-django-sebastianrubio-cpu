from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pokedex.auth_view import CustomTokenView
from api.views import PokemonViewSet, TrainerViewSet

router = DefaultRouter()
router.register(r'pokemons', PokemonViewSet, basename='pokemon')
router.register(r'trainers', TrainerViewSet, basename='trainer')

urlpatterns = [
    path('oauth/token/', CustomTokenView.as_view(), name='oauth2_token'),
    path('', include(router.urls)),
]