from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

def validar_tamanho_imagem(imagem):
    tamanho_maximo_mb = 5
    if imagem.size > tamanho_maximo_mb * 1024 * 1024:
        raise ValidationError(f"A imagem não pode ter mais de {tamanho_maximo_mb} MB.")


# Crie seus modelos aqui

class Campeonato(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='campeonatos/', blank=True, null=True, validators=[validar_tamanho_imagem])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome
    
class Time(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='times/', blank=True, null=True, validators=[validar_tamanho_imagem])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Treinador(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    foto = models.ImageField(upload_to='treinadores/', blank=True, null=True, validators=[validar_tamanho_imagem])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Carreira(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="carreiras")
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE, related_name="carreiras")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carreiras")
    
    class Meta:
        unique_together = ('nome', 'usuario')
    
    def __str__(self):
        return self.nome


class Jogador(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    carreira = models.ManyToManyField(Carreira, related_name="jogadores")
    foto = models.ImageField(upload_to='jogadores/', blank=True, null=True, validators=[validar_tamanho_imagem])
    clube_atual = models.BooleanField(default=True)
    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome
    
class Temporada(models.Model):
    data = models.CharField(max_length=50, default=f"{date.today().year}/{date.today().year + 1}")
    
    class Meta:
        ordering = ["data"]
    
    def __str__(self):
        return self.data



class Estatistica(models.Model):
    jogos = models.IntegerField('Quantidade de Jogos', validators=[MinValueValidator(0)], default=0)
    gol = models.IntegerField('Quantidade de Gols', validators=[MinValueValidator(0)], default=0)
    assistencia = models.IntegerField('Quantidade de Assistências', validators=[MinValueValidator(0)], default=0)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name="estatisticas")
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name="estatisticas")
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name="estatisticas")
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="estatisticas")
    
    def total_participacoes(self):
        return self.gol + self.assistencia
    
    def eficiencia(self):
        if self.jogos > 0:
            return (self.total_participacoes() / self.jogos) * 100
        return 0

    def __str__(self):
        return f"{self.jogador} - {self.campeonato} ({self.temporada})"
