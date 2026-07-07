from rest_framework import viewsets
from .serializer import PokemonSerializer, TrainerSerializer
from pokedex.models import Pokemon, Trainer

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer