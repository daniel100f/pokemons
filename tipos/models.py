from django.db import models

# Create your model types here.

class Tipos(models.Model):
    
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50, unique=True)
    
