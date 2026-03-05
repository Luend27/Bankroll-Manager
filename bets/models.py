from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Banca(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, help_text="Ex: Bet365, Pinnacle, Banca Principal")
    capital_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.usuario.username}"

class Aposta(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('GANHA', 'Ganha'),
        ('PERDIDA', 'Perdida'),
        ('DEVOLVIDA', 'Devolvida (Void)'),
        ('CASHOUT', 'Cashout (Encerrada)'),
    ]

    ESPORTE_CHOICES = [
        ('FUTEBOL', 'Futebol'),
        ('BASQUETE', 'Basquete'),
        ('TENIS', 'Tênis'),
        ('E-SPORTS', 'E-Sports'),
        ('MMA', 'MMA'),
        ('VOLEI', 'Vôlei'),
    ]

    banca = models.ForeignKey(Banca, on_delete=models.CASCADE, related_name='apostas')
    
    esporte = models.CharField(max_length=20, choices=ESPORTE_CHOICES, default='FUTEBOL')
    competicao = models.CharField(max_length=100, blank=True, null=True, verbose_name="Competição")
    mercado = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Over 2.5, ML")
    
    data = models.DateTimeField(default=timezone.now)
    
    odd = models.DecimalField(max_digits=5, decimal_places=2)
    stake = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Apostado")
    
    resultado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    valor_cashout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Cashout")
    anotacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.esporte} - {self.competicao} ({self.stake} @ {self.odd})"

    @property
    def lucro_prejuizo(self):
        if self.resultado == 'PENDENTE':
            return 0
        elif self.resultado == 'PERDIDA':
            return -self.stake
        elif self.resultado == 'DEVOLVIDA':
            return 0
        elif self.resultado == 'GANHA':
            return (self.stake * self.odd) - self.stake
        elif self.resultado == 'CASHOUT':
            if self.valor_cashout is not None:
                return self.valor_cashout - self.stake
            return 0
        return 0