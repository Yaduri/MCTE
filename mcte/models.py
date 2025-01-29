from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

def validar_tamanho_imagem(imagem):
    #tamanho_maximo_mb = 500
    #if imagem.size > tamanho_maximo_mb * 1024 * 1024:
    #    raise ValidationError(f"A imagem não pode ter mais de {tamanho_maximo_mb} MB.")
    ...


# Crie seus modelos aqui
class Time(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    apelido = models.CharField(max_length=50, default="")
    logo = models.ImageField(upload_to='times/', blank=True, null=True, validators=[validar_tamanho_imagem])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    criado = models.BooleanField('Time foi criado manualmente?', default=False)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Jogador(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    posicao = models.CharField(max_length=30)
    time = models.CharField(max_length=50)
    criado = models.BooleanField('Jogador foi criado manualmente?', default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    clube_atual = models.BooleanField(default=False)
    
    #data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    #carreira = models.ManyToManyField(Carreira, related_name="jogadores")
    foto = models.ImageField(upload_to='jogadores/', blank=True, null=True, validators=[validar_tamanho_imagem])
    
    
    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome

class Treinador(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    foto = models.ImageField(upload_to='treinadores/', blank=True, null=True, validators=[validar_tamanho_imagem])
    #time = models.ManyToManyField(Time, related_name="treinadores")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    criado = models.BooleanField('Treinador foi criado manualmente?', default=False)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome



class Carreira(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    time_atual = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="carreiras")
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE, related_name="carreiras")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carreiras")
    
    class Meta:
        unique_together = ('nome', 'usuario')
    
    def __str__(self):
        return self.nome

class CarreiraTimeJogador(models.Model):
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name="carreira_times_jogadores")
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="carreira_times_jogadores")
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name="carreira_times_jogadores")
    time_atual = models.BooleanField(default=True)
    titular = models.BooleanField(default=False)

    class Meta:
        unique_together = ("carreira", "time", "jogador")
        verbose_name = "Carreira-Time-Jogador"
        verbose_name_plural = "Carreira-Times-Jogadores"

    def __str__(self):
        return f"{self.carreira.nome} - {self.time.nome} - {self.jogador.nome}"


class Campeonato(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='campeonatos/', blank=True, null=True, validators=[validar_tamanho_imagem])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class CarreiraCampeonato(models.Model):
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name="carreira_campeonatos")
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name="carreira_campeonatos")
    ativo = models.BooleanField(default=True)
    
    
class Temporada(models.Model):
    data = models.CharField(max_length=50, default=f"{date.today().year}/{date.today().year + 1}")
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name="temporadas")
    class Meta:
        ordering = ["data"]
    
    def __str__(self):
        return self.data

class Estatistica(models.Model):
    jogos = models.IntegerField('Quantidade de Jogos', validators=[MinValueValidator(0)], default=0)
    gols = models.IntegerField('Quantidade de Gols', validators=[MinValueValidator(0)], default=0)
    assistencias = models.IntegerField('Quantidade de Assistências', validators=[MinValueValidator(0)], default=0)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name="estatisticas")
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="estatisticas")
    carreira_time_jogador = models.ForeignKey(CarreiraTimeJogador, on_delete=models.CASCADE, related_name="estatisticas", default=0)
    #jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name="estatisticas")
    #carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name="estatisticas")
    
    
    def total_participacoes(self):
        return self.gol + self.assistencia
    
    def eficiencia(self):
        if self.jogos > 0:
            return (self.total_participacoes() / self.jogos) * 100
        return 0

    def __str__(self):
        return f"{self.jogador} - {self.campeonato} ({self.temporada})"
