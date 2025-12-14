from rest_framework import serializers
from .models import Evento
from participacoes.models import Inscricao, StatusInscricao 


class EventoSerializer(serializers.ModelSerializer):
    """
    Serializer para listar, criar e editar eventos.
    """
    # Exibe o nome do organizador (leitura) em vez de apenas o ID
    organizador_username = serializers.ReadOnlyField(source='organizador.username')
    
    # Campo para checagem rápida no Frontend
    e_gratuito = serializers.SerializerMethodField()
    
    # Campo para o Feed: Vagas Restantes
    vagas_restantes = serializers.ReadOnlyField()


    class Meta:
        model = Evento
        fields = (
            'id', 
            'titulo', 
            'descricao_curta', 
            'descricao_completa', 
            'local_endereco', 
            'local_url',
            'data_inicio', 
            'data_fim', 
            'prazo_inscricao', 
            'tipo', 
            'preco', 
            'status',
            'capacidade',
            'exige_aprovacao',
            'banner_url',
            'organizador',
            'organizador_username',
            'e_gratuito',
            'vagas_restantes', # Campo de leitura
        )

        # Campos que não podem ser alterados diretamente via JSON
        read_only_fields = ('organizador', 'status', 'e_gratuito', 'vagas_restantes') 


    def get_e_gratuito(self, obj):
        """Calcula se o evento é gratuito."""
        return obj.tipo == 'gratuito'


    def create(self, validated_data):
        # Define o organizador automaticamente como o usuário logado
        validated_data['organizador'] = self.context['request'].user

        # Define o status inicial como 'rascunho'
        validated_data['status'] = 'rascunho' 
        
        # Se o tipo for gratuito, garante que o preço seja 0
        if validated_data.get('tipo') == 'gratuito':
            validated_data['preco'] = 0.00
            
        return super().create(validated_data)
        