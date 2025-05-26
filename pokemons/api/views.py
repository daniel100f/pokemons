from rest_framework import viewsets
from pokemons.api.serializer import PokemonsSerializer
from pokemons.models import Pokemons
# segundo paso crear viewset
class PokemonsViewSet(viewsets.ModelViewSet):

    queryset=Pokemons.objects.all()
    serializer_class=PokemonsSerializer