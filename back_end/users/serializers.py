from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class LoginPersonalizadoSerializer(TokenObtainPairSerializer):
    """
    Estende o serializer padrão do JWT para retornar dados do usuário
    junto com os tokens de acesso.
    """
    def validate(self, attrs):
        # 1. Executa a validação padrão (verifica senha e gera tokens)
        data = super().validate(attrs)

        # 2. Adiciona dados personalizados ao dicionário de resposta (JSON)
        # self.user é o usuário autenticado que o método super() encontrou
        data['usuario'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'papel': self.user.papel, # O CAMPO MAIS IMPORTANTE
            'cidade': self.user.cidade,
            'url_foto': self.user.url_foto if self.user.url_foto else None
        }

        # O retorno será: { "access": "...", "refresh": "...", "usuario": { ... } }
        return data
