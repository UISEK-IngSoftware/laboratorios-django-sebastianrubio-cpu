from rest_framework import serializer
from pokedex.models import Pokemon

class PokemonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pokemon
		fields = 