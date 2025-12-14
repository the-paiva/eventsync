from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import serializers
from .models import Inscricao
from .serializers import InscricaoSerializer


class InscricaoViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar as Inscrições dos participantes em Eventos.
    
    A rota principal (POST /api/inscricoes/) é para o usuário se inscrever.
    GET /api/inscricoes/minhas_inscricoes/ lista os ingressos do usuário logado.
    """
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    
    # Permissões: Apenas usuários autenticados podem interagir (criar, listar suas inscrições)
    permission_classes = [permissions.IsAuthenticated]


    # Removemos o try/except do create para usar o perform_create
    def create(self, request, *args, **kwargs):
        """
        Customiza a criação de inscrição para injetar o usuário logado e verificar regras.
        """
        # Injeta o request no contexto para que o Serializer possa acessar o user logado
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # O perform_create é quem chama serializer.save(). 
        # Captura de erros de negócio delegada ao perform_create para DRY (Don't Repeat Yourself)
        return super().create(request, *args, **kwargs)


    # Implementa a captura de erros de negócio gerados pelo Serializer
    def perform_create(self, serializer):
        try:
            serializer.save()
        except serializers.ValidationError as e:
            # Captura o erro de validação (ex: "Vagas esgotadas" ou "Já inscrito")
            # e re-levanta (raise) para ser tratado pelo exception handler do DRF, 
            # garantindo que a resposta 400 seja formatada corretamente.
            raise serializers.ValidationError(e.detail)


    @action(detail=False, methods=['get'])
    def minhas_inscricoes(self, request):
        """
        Rota personalizada para o Feed do Participante: lista todos os ingressos
        do usuário logado, incluindo o código de verificação para o QR Code.
        URL: GET /api/inscricoes/minhas_inscricoes/
        """
        # Filtra as inscrições apenas pelo participante logado
        inscricoes = Inscricao.objects.filter(participante=request.user).order_by('-data_inscricao')
        
        # Paginação (se estiver configurada)
        page = self.paginate_queryset(inscricoes)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(inscricoes, many=True)
        return Response(serializer.data)

    
    def list(self, request, *args, **kwargs):
        """Bloqueia a listagem geral de todas as inscrições por questões de privacidade."""
        # Apenas superusuários ou organizadores podem listar TUDO
        if not request.user.is_superuser and request.user.papel != 'organizador':
            return Response({"erro": "Acesso negado. Use /minhas_inscricoes/."}, status=status.HTTP_403_FORBIDDEN)
        
        # Se for admin/organizador, permite o list
        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Permite visualizar a inscrição se for o participante OU o organizador do evento
        if instance.participante == request.user or instance.evento.organizador == request.user:
            return super().retrieve(request, *args, **kwargs)
        
        # O código só chega aqui se a condição acima for falsa
        return Response({"erro": "Você não tem permissão para visualizar esta inscrição."}, status=status.HTTP_403_FORBIDDEN)
