from django.db import models

# Create your model types here.

class Tipos(models.Model):
    
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50, unique=True)
    

    class Meta: # <--- Esta es la Meta del MODELO
        # Atributos específicos del MODELO
        ordering = ['id'] # Cómo se ordenan las consultas por defecto
        verbose_name = "Tipo" # Nombre singular en el admin
        verbose_name_plural = "Tipos" # Nombre plural en el admin
        db_table = 'pokemon_type' # Nombre de la tabla en la DB (opcional)
