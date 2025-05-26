from rest_framework import serializers
from pokemons.models import Pokemons
# este es mi serialixador de pokemons
class PokemonsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pokemons
        fields= '__all__'