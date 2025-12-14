from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Evento, StatusEvento
from .serializers import EventoSerializer
from .permissions import EhOrganizadorOuLeitura, EhDonoDoEvento
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventoFilter
from django.utils import timezone


class EventoViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar Eventos (CRUD).
    Inclui o Feed Geral (listagem) e o Feed de Gestão do Organizador.
    """
    serializer_class = EventoSerializer
    
    # Configura o DjangoFilterBackend para processar os parâmetros da URL
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoFilter
    
    # Permissão padrão (GET é público; POST/PUT/DELETE só para organizadores)
    permission_classes = [EhOrganizadorOuLeitura] 
    

    def get_queryset(self):
        """
        Define o conjunto de dados base (QuerySet) para esta View.
        A listagem principal ('list' action) deve mostrar apenas eventos PUBLICADOS e ATIVOS.
        """
        # Para ações detalhadas (retrieve, update, destroy) e ações customizadas (@action)
        # o queryset é deixado amplo para que as permissões e filtros específicos atuem.
        if self.action != 'list':
            return Evento.objects.all()

        # ----------------------------------------------------
        # Lógica do Feed Público (Ação 'list'):
        # 1. Deve ser publicado
        # 2. A data de fim deve ser futura (o evento ainda não pode ter acabado)
        # ----------------------------------------------------
        return Evento.objects.filter(
            status=StatusEvento.PUBLICADO,
            data_fim__gt=timezone.now() # Filtra eventos que ainda não acabaram
        ).order_by('data_inicio') # Ordena os próximos primeiro


    def get_permissions(self):
        """
        Define a permissão específica para as ações de CRUD de um único objeto.
        """
        # Para detalhar, atualizar ou deletar (ações que envolvem um objeto específico)
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Aplica duas permissões: 1. É organizador OU leitura, e 2. É o dono do evento
            return [EhOrganizadorOuLeitura(), EhDonoDoEvento()]
        
        # Para listagem (list) e criação (create), usa a permissão padrão
        return [EhOrganizadorOuLeitura()]


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def meus_eventos(self, request):
        """
        Rota exclusiva para o Feed de Gestão do Organizador.
        Retorna apenas os eventos criados pelo usuário logado.
        URL: GET /api/eventos/meus_eventos/
        
        Nota: O DjangoFilterBackend é aplicado automaticamente aqui também,
        permitindo que o organizador filtre seus próprios eventos.
        """
        if not request.user.is_authenticated:
            return Response({"erro": "Usuário não autenticado"}, status=401)
            
        # Filtra a lista para mostrar apenas eventos criados pelo usuário logado
        eventos = Evento.objects.filter(organizador=request.user).order_by('-data_criacao')
        
        # O filtro de URL (DjangoFilterBackend) é aplicado em 'eventos' antes da paginação.
        
        # Usa o método de paginação padrão do viewset
        page = self.paginate_queryset(eventos)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(eventos, many=True)
        return Response(serializer.data)
