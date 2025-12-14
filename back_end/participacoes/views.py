from rest_framework import viewsets
from .models import Inscricao
from .serializers import InscricaoSerializer


# Placeholder inicial
class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    