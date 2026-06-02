from django.urls import path
from . import views
from rest_framework import routers 



router = routers.DefualtRouter()
router.register(r'pokemons', PokemonViewSet)



urlpatterns = [
	path('', include (router.urls))
]