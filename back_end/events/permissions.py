from rest_framework import permissions


class EhOrganizadorOuLeitura(permissions.BasePermission):
    """
    Permissão personalizada:
    - Leitura (GET, HEAD, OPTIONS): Permitido para todos (Público).
    - Escrita (POST, PUT, DELETE): Permitido apenas para quem é 'organizador'.
    """


    def has_permission(self, request, view):
        # Se for apenas leitura (safe method), permite (Feed Público)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Se for escrita, usuário deve estar logado E ser organizador
        return (request.user and 
                request.user.is_authenticated and 
                request.user.papel == 'organizador')


class EhDonoDoEvento(permissions.BasePermission):
    """
    Permite edição/exclusão (PUT, DELETE) apenas se o usuário for o dono (organizador) do evento.
    Esta permissão é usada APÓS o EhOrganizadorOuLeitura.
    """
    def has_object_permission(self, request, view, obj):
        # Leitura (safe methods) é permitida a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escrita apenas se o usuário for o organizador do objeto
        return obj.organizador == request.user
