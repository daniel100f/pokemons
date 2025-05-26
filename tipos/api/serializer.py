from rest_framework import serializers
from tipos.models import Tipos
#primero creamos el serializador, uego vamos a viewset
class TiposSerializers(serializers.ModelSerializer):
    class Meta:
        model=Tipos
        fields='__all__'
