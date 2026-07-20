from django.urls import path, include
from rest_framework import routers
from .views import PokemonViewSet, TrainerViewSet, GitHubLoginAPIView

router = routers.DefaultRouter()
router.register(r'pokemons', PokemonViewSet, basename='pokemon')
router.register(r'trainers', TrainerViewSet, basename='trainer')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/github/', GitHubLoginAPIView.as_view(), name='github_auth'),
]