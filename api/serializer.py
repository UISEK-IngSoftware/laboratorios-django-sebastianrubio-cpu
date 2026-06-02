from rest_framework import serializers
from pokedex.models import Pokemon # Corrección: el modelo vive en la Pokedex

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'