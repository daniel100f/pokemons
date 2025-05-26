from rest_framework import viewsets
from tipos.models import Tipos
from tipos.api.serializer import TiposSerializers

class TiposViewSet(viewsets.ModelViewSet):
    queryset=Tipos.objects.all()
    serializer_class=TiposSerializers