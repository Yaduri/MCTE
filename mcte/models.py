from django.db import models
from django.contrib.auth.models import User

# Crie seus modelos aqui

class Campeonato(models.Model):
    nome = models.CharField(max_length=50)
    #logo = Adicionar no futuro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Time(models.Model):
    nome = models.CharField(max_length=50)
    #logo = Adicionar no futuro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Treinador(models.Model):
    nome = models.CharField(max_length=50)
    #foto = Adicionar no futuro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Carreira(models.Model):
    nome = models.CharField(max_length=50)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Jogador(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField('Data de Nascimento')
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE)

class Estatistica(models.Model):
    jogos = models.IntegerField('Quantidade de Jogos')
    gol = models.IntegerField('Quantidade de Gols')
    assistencia = models.IntegerField('Quantidade de Assistencias')
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE)
    