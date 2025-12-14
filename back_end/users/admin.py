from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuarioAdmin(UserAdmin):
    """
    Configuração personalizada do painel admin para o modelo Usuario.
    Adiciona os campos extras (papel, cidade, etc.) aos formulários padrão.
    """
    # 1. Colunas que aparecem na lista geral de usuários
    list_display = ('username', 'email', 'papel', 'cidade', 'is_staff')
    
    # 2. Filtros laterais para facilitar a busca
    list_filter = UserAdmin.list_filter + ('papel', 'visibilidade_participacao')

    # 3. Campos que aparecem no formulário de EDIÇÃO de usuário
    # Adicionamos uma nova seção 'Informações Extras' ao final
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras do EventSync', {
            'fields': ('papel', 'cidade', 'url_foto', 'visibilidade_participacao', 'rating_organizador')
        }),
    )

    # 4. Campos que aparecem no formulário de CRIAÇÃO de usuário (botão 'Adicionar usuário')
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Extras', {
            'fields': ('email', 'papel', 'cidade')
        }),
    )
    

# Registra o modelo usando nossa classe personalizada
admin.site.register(Usuario, UsuarioAdmin)