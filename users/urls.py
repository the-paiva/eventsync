from django.urls import path
from .views import RegistroView, LoginPersonalizadoView
from rest_framework_simplejwt.views import TokenRefreshView


# Definimos os caminhos de URL para o app 'users'
urlpatterns = [
    # POST /autenticacao/registrar/ (Cria um novo usuário)
    path('registrar/', RegistroView.as_view(), name='auth_registrar'),
    
    # POST /autenticacao/login/ (Gera o Access/Refresh Token E os dados do usuário/papel)
    path('login/', LoginPersonalizadoView.as_view(), name='auth_login'),
    
    # POST /autenticacao/token/refresh/ (Usa o Refresh Token para obter um novo Access Token)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]