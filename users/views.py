from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegistroSerializer
from django.contrib.auth import get_user_model


Usuario = get_user_model()


class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (AllowAny,) # Qualquer um pode se registrar
    serializer_class = RegistroSerializer
    