from django.urls import path, include
from rest_framework import routers
from .views import PokemonViewSet, TrainerViewSet, GitHubLoginAPIView
from django.conf import settings
from pokedex.auth_view import CustomTokenView
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'pokemons', PokemonViewSet, basename='pokemon')
router.register(r'trainers', TrainerViewSet, basename='trainer')

urlpatterns = [

    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/catalog/', include('catalog.urls')),
    path('api/v1/o/token/', CustomTokenView.as_view(), name='token'),
    path('api/v1/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]