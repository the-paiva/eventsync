from rest_framework import serializers
from .models import Inscricao, StatusInscricao
from events.models import Evento
from django.contrib.auth import get_user_model


Usuario = get_user_model()


"""
Serializer para o Participante se inscrever em um evento e para o Organizador
gerenciar essas inscrições.
"""
class InscricaoSerializer(serializers.ModelSerializer):
    # Campos de leitura apenas, para serem exibidos no Front-end
    participante_username = serializers.ReadOnlyField(source='participante.username')
    evento_titulo = serializers.ReadOnlyField(source='evento.titulo')
    
    # Campo para checar se o usuário logado está inscrito (Usado no Feed)
    e_o_usuario_logado = serializers.SerializerMethodField()


    class Meta:
        model = Inscricao

        fields = [
            'id', 
            'evento', 
            'participante', 
            'participante_username',
            'evento_titulo',
            'status', 
            'data_inscricao', 
            'codigo_verificacao',
            'check_in_realizado',
            'e_o_usuario_logado',
        ]

        # Campos que só podem ser lidos (ID, quem criou, status, código)
        read_only_fields = (
            'participante', 
            'status', 
            'codigo_verificacao', 
            'check_in_realizado', 
            'data_inscricao',
            'e_o_usuario_logado',
        )


    def get_e_o_usuario_logado(self, obj):
        """ Retorna True se o participante for o usuário que fez a requisição. """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.participante == request.user
        return False


    def create(self, validated_data):
        # 1. Define o participante automaticamente como o usuário logado
        user = self.context['request'].user
        validated_data['participante'] = user
        
        # 2. Verifica se o usuário já está inscrito no evento
        evento_id = validated_data['evento'].id
        if Inscricao.objects.filter(participante=user, evento_id=evento_id).exists():
            raise serializers.ValidationError({"erro": "Você já está inscrito neste evento."})

        # 3. Verifica se o evento exige aprovação, definindo o status inicial
        evento = validated_data['evento']
        if evento.exige_aprovacao:
            validated_data['status'] = StatusInscricao.PENDENTE
        else:
            validated_data['status'] = StatusInscricao.APROVADA
            
        # 4. Verifica a capacidade máxima
        if evento.vagas_restantes <= 0:
            raise serializers.ValidationError({"erro": "As vagas para este evento estão esgotadas."})

        return super().create(validated_data)
