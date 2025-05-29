from rest_framework import viewsets
from pokemons.api.serializer import PokemonsSerializer
from pokemons.models import Pokemons

# segundo paso crear viewset
class PokemonsViewSet(viewsets.ModelViewSet):
        #aqui se hace un llamado a la base de datos o al modelo en especifico para  obtener los pokemons
 
        queryset=Pokemons.objects.all()
        serializer_class=PokemonsSerializer
        





