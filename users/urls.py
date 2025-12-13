from django.urls import path
from .views import RegistroView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # View de Login JWT (recebe username/password, retorna access/refresh)
    TokenRefreshView,    # View para renovar o token
)

# Definimos os caminhos de URL para o app 'users'
urlpatterns = [
    # POST /autenticacao/registrar/ (Cria um novo usuário)
    path('registrar/', RegistroView.as_view(), name='auth_registrar'),
    
    # POST /autenticacao/login/ (Gera o Access e Refresh Token)
    path('login/', TokenObtainPairView.as_view(), name='auth_login'),
    
    # POST /autenticacao/token/refresh/ (Usa o Refresh Token para obter um novo Access Token)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]