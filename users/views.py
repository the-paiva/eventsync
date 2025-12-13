from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegistroSerializer, LoginPersonalizadoSerializer
from django.contrib.auth import get_user_model


Usuario = get_user_model()


class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = (AllowAny,) # Qualquer um pode se registrar
    serializer_class = RegistroSerializer


class LoginPersonalizadoView(TokenObtainPairView):
    """
    View de Login customizada que usa o nosso Serializer
    para retornar dados do usuário junto com o token.
    """
    serializer_class = LoginPersonalizadoSerializer
    