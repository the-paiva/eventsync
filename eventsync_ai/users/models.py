from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="E-mail")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    url_foto = models.URLField(blank=True, null=True, verbose_name="URL da Foto de Perfil")
    visibilidade_participacao = models.BooleanField(default=True, verbose_name="Visível em Listas de Participantes")
    rating_organizador = models.FloatField(default=0.0, verbose_name="Rating do Organizador")

    OPCOES_PAPEL = (
        ('participante', 'Participante'),
        ('organizador', 'Organizador'),
    )
    
    papel = models.CharField(max_length=20, choices=OPCOES_PAPEL, default='participante', verbose_name="Papel")
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        