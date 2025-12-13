from rest_framework import serializers
from django.contrib.auth import get_user_model


Usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    # Campo 'senha' é apenas para escrita e não será retornado na resposta
    senha = serializers.CharField(write_only=True)


    class Meta:
        model = Usuario
        # Campos necessários para o cadastro do MVP
        fields = ('id', 'username', 'email', 'senha', 'cidade', 'papel')
        # Mapeia 'senha' para 'password' do modelo Django internamente
        extra_kwargs = {
            'senha': {'write_only': True},
            'email': {'required': True}, # Garante que o email seja sempre fornecido
        }


    def create(self, dados_validados):
        # Renomeia 'senha' para 'password' para o método interno do Django
        senha = dados_validados.pop('senha')
        
        usuario = Usuario.objects.create_user(
            username=dados_validados['username'],
            email=dados_validados.get('email'),
            password=senha,
            cidade=dados_validados.get('cidade', ''),
            papel=dados_validados.get('papel', 'participante')
        )
        return usuario
