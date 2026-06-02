from rest_framework import viewsets
from .serializer import PokemonSerializer
from pokedex.models import Pokemon # Corrección: extraemos el queryset de la aplicación principal

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer