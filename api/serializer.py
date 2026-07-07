from rest_framework import serializers
from pokedex.models import Pokemon, Trainer # Aseguramos importar ambos modelos

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'