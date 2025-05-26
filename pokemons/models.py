from django.db import models

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
        altura=models.DecimalField(max_digits=5, decimal_places=2, null=True)
        peso=models.DecimalField(max_digits=5, decimal_places=2, null=True)










