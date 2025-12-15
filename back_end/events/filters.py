import django_filters
from .models import Evento, StatusEvento, TipoEvento, CategoriaEvento


class EventoFilter(django_filters.FilterSet):
    """
    Define os filtros customizados para a listagem (Feed) de Eventos.
    Permite filtrar por data, categoria, tipo (pago/gratuito) e destaque.
    """
    
    # Filtro por TIPO (pago ou gratuito)
    tipo = django_filters.ChoiceFilter(
        choices=TipoEvento.choices,
        lookup_expr='exact',
        label="Tipo (gratuito/pago)"
    )

    # Filtro por CATEGORIA (tecnologia, esportes, etc.)
    categoria = django_filters.ChoiceFilter(
        choices=CategoriaEvento.choices,
        lookup_expr='exact',
        label="Categoria"
    )

    # Filtro para eventos com data de início APÓS a data fornecida (Ex: filtrar por mês)
    data_inicio_gt = django_filters.DateTimeFilter(
        field_name='data_inicio', 
        lookup_expr='gte', 
        label="Data de Início (Maior ou igual a)"
    )
    
    # Filtro para eventos com prazo de inscrição ANTES da data fornecida
    prazo_inscricao_lt = django_filters.DateTimeFilter(
        field_name='prazo_inscricao', 
        lookup_expr='lte', 
        label="Prazo de Inscrição (Menor ou igual a)"
    )
    
    # Filtro por Preço Máximo (para o Front-end mostrar eventos abaixo de um certo valor)
    preco_max = django_filters.NumberFilter(
        field_name='preco', 
        lookup_expr='lte', 
        label="Preço Máximo (Menor ou igual a)"
    )


    class Meta:
        model = Evento
        fields = ['tipo', 'categoria', 'data_inicio_gt', 'preco_max', 'status']