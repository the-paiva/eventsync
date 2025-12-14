from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    # Rota da Raiz (Health Check)
    path('', TemplateView.as_view(template_name='api_root.html'), name='api_root'),
    
    # Painel Administrativo
    path('admin/', admin.site.urls),
    
    # Autenticação (Users)
    path('autenticacao/', include('users.urls')), 
    
    # API de Eventos (CRUD e Feed Geral)
    path('api/', include('events.urls')), 
    
    # API de Inscrições/Participações (Gestão de Vagas, Check-in, Meus Ingressos)
    path('api/', include('participacoes.urls')),
]