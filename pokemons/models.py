from django.db import models
from tipos.models import Tipos

# Create your model pokemons here.

class Pokemons(models.Model):
        
        id=models.IntegerField(primary_key=True)
        name=models.CharField(max_length=50)
        #image=models.URLField()
        image=models.CharField(max_length=100)
        vida=models.IntegerField()
        ataque=models.IntegerField()
        defensa=models.IntegerField()
        velocidad=models.IntegerField(null=True)
        altura=models.IntegerField(null=True)
        peso=models.IntegerField(null=True)
        #relacion de modelos
        types = models.ManyToManyField(Tipos, related_name='pokemons')










