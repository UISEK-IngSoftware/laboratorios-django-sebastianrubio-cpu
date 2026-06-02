from rest_framework import viewsets
from .serializer import PokemonSerializer
from .models import Pokemon

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer