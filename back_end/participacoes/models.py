from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid 


# Importação de Evento é feita via string para evitar importação circular no futuro.
# from events.models import Evento 


Usuario = get_user_model()


# --- DEFINIÇÕES FIXAS DE PARTICIPAÇÃO ---
class StatusInscricao(models.TextChoices):
    # Status da participação
    PENDENTE = 'pendente', _('Pendente (Aguardando Aprovação/Pagamento)')
    APROVADA = 'aprovada', _('Aprovada/Confirmada')
    RECUSADA = 'recusada', _('Recusada')
    CANCELADA = 'cancelada', _('Cancelada pelo Participante')


# --- MODELO PRINCIPAL DE PARTICIPAÇÃO ---
class Inscricao(models.Model):
    """
    Representa a participação de um usuário em um evento.
    Esta é a tabela de relacionamento Many-to-Many com dados extras.
    """
    participante = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='inscricoes_feitas',
        verbose_name=_("Participante")
    )

    # Referência ao Evento (App 'events') via string
    evento = models.ForeignKey(
        'events.Evento', # Aponta para o modelo no outro App
        on_delete=models.CASCADE, 
        related_name='inscricoes',
        verbose_name=_("Evento Inscrito")
    )

    # Controle da Inscrição
    status = models.CharField(
        max_length=15, 
        choices=StatusInscricao.choices, 
        default=StatusInscricao.PENDENTE,
        verbose_name=_("Status da Inscrição")
    )

    data_inscricao = models.DateTimeField(auto_now_add=True, verbose_name=_("Data da Inscrição"))
    
    # QR Code / Check-in
    codigo_verificacao = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True, 
        verbose_name=_("Código Único de Check-in")
    )

    check_in_realizado = models.BooleanField(default=False, verbose_name=_("Check-in Realizado"))


    class Meta:
        verbose_name = _("Inscrição")
        verbose_name_plural = _("Inscrições")
        unique_together = ('participante', 'evento')
        ordering = ['data_inscricao']


    def __str__(self):
        return f"[{self.get_status_display()}] {self.participante.username} em {self.evento.titulo}"
