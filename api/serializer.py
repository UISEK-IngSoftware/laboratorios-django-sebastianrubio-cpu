from rest_framework import serializers
from api.models import Pokemon # Asumiendo que el modelo está en api, de lo contrario pokedex.models es correcto si lo compartes

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__' # Debes definir los campos