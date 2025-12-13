from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # Importa a view genérica

urlpatterns = [
    # Rota da Raiz (Health Check/Boas Vindas)
    # Apenas retorna um status 200 OK e indica que o servidor está funcionando.
    path('', TemplateView.as_view(template_name='api_root.html'), name='api_root'),
    
    # Rota do painel administrativo
    path('admin/', admin.site.urls),
    
    # Conecta as rotas do app 'users' (Registro/Login) sob o prefixo 'autenticacao/'
    # Isso direciona requisições para /autenticacao/ para o users/urls.py
    path('autenticacao/', include('users.urls')), 
]
