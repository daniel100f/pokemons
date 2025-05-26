from rest_framework import routers
from pokemons.api.views import PokemonsViewSet
router=routers.DefaultRouter()
router.register('pokemons',PokemonsViewSet,basename='pokemons')

urlpatterns=router.urls

