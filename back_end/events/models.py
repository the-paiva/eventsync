from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from participacoes.models import StatusInscricao 


Usuario = get_user_model()


# --- DEFINIÇÕES FIXAS (TextChoices) ---
class TipoEvento(models.TextChoices):
    # Valores de tipos de evento, usado para filtros e lógica de preço
    GRATUITO = 'gratuito', _('Gratuito')
    PAGO = 'pago', _('Pago')


class StatusEvento(models.TextChoices):
    # Fluxo de vida do evento: Rascunho, Publicado, Cancelado, etc.
    RASCUNHO = 'rascunho', _('Rascunho')
    PUBLICADO = 'publicado', _('Publicado')
    FINALIZADO = 'finalizado', _('Finalizado')
    CANCELADO = 'cancelado', _('Cancelado')


class CategoriaEvento(models.TextChoices):
    # Categorias fixas para o Feed (filtro)
    TECNOLOGIA = 'tecnologia', _('Tecnologia e TI')
    NEGOCIOS = 'negocios', _('Negócios e Empreendedorismo')
    SAUDE = 'saude', _('Saúde e Bem-estar')
    ENTRETENIMENTO = 'entretenimento', _('Entretenimento e Lazer')
    ESPORTES = 'esportes', _('Esportes e Fitness')
    OUTROS = 'outros', _('Outros')


# --- MODELOS ---
class Evento(models.Model):
    """
    Representa um evento criado por um organizador.
    """
    # Relacionamento (ForeignKey - Muitos Eventos para Um Organizador)
    organizador = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='eventos_organizados',
        verbose_name=_("Organizador")
    )

    # Informações Básicas
    titulo = models.CharField(max_length=255, verbose_name=_("Título do Evento"))
    descricao_curta = models.CharField(max_length=500, verbose_name=_("Descrição Curta"))
    descricao_completa = models.TextField(verbose_name=_("Descrição Completa"))

    banner_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name=_("URL do Banner/Capa do Evento")
    )
    
    # Detalhes de Data e Local
    local_endereco = models.CharField(max_length=255, verbose_name=_("Endereço Físico"))

    local_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name=_("URL do Mapa/Local (Ex: Google Maps)")
    )

    data_inicio = models.DateTimeField(verbose_name=_("Data e Hora de Início"))
    data_fim = models.DateTimeField(verbose_name=_("Data e Hora de Fim"))
    prazo_inscricao = models.DateTimeField(verbose_name=_("Prazo Final de Inscrição"))

    # Controle e Financeiro
    tipo = models.CharField(
        max_length=10, 
        choices=TipoEvento.choices, 
        default=TipoEvento.GRATUITO,
        verbose_name=_("Tipo (Pago/Gratuito)")
    )

    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_("Preço (R$)")
    )

    capacidade = models.PositiveIntegerField(
        default=0, 
        verbose_name=_("Capacidade Máxima de Participantes")
    )

    exige_aprovacao = models.BooleanField(
        default=False, 
        verbose_name=_("Exige aprovação manual do organizador?")
    )

    status = models.CharField(
        max_length=15, 
        choices=StatusEvento.choices, 
        default=StatusEvento.RASCUNHO,
        verbose_name=_("Status do Evento")
    )

    categoria = models.CharField(
        max_length=30,
        choices=CategoriaEvento.choices,
        default=CategoriaEvento.OUTROS,
        verbose_name=_("Categoria")
    )

    # Visibilidade (para o Feed)
    mostrar_participantes = models.BooleanField(
        default=True, 
        verbose_name=_("Mostrar lista parcial de participantes no Feed?")
    )
    

    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")
        ordering = ['data_inicio']


    def __str__(self):
        return self.titulo
    

    @property
    def vagas_restantes(self):
        """Calcula o número de vagas restantes, importando o status do novo app."""
        # usa a related_name='inscricoes' da ForeignKey definida em Inscricao
        aprovadas = self.inscricoes.filter(status=StatusInscricao.APROVADA).count()
        return self.capacidade - aprovadas
