from django.db import models
from django.contrib.auth.models import User

# Crie seus modelos aqui

class Campeonato(models.Model):
    nome = models.CharField(max_length=50)
    #logo = Adicionar no futuro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome
    
class Time(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='times/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Treinador(models.Model):
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='treinadores/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Carreira(models.Model):
    nome = models.CharField(max_length=50)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="carreiras")
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE, related_name="carreiras")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carreiras")
    
    class Meta:
        unique_together = ('nome', 'usuario')
    
    def __str__(self):
        return self.nome


class Jogador(models.Model):
    nome = models.CharField(max_length=50)
    data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='jogadores/', blank=True, null=True)
    clube_atual = models.BooleanField(default=True)
    class Meta:
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome
    
class Temporada(models.Model):
    data = models.CharField(max_length=50, default="24/25")
    
    class Meta:
        ordering = ["data"]
    
    def __str__(self):
        return self.data

class Estatistica(models.Model):
    jogos = models.IntegerField('Quantidade de Jogos')
    gol = models.IntegerField('Quantidade de Gols')
    assistencia = models.IntegerField('Quantidade de Assistências')
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name="estatisticas")
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name="estatisticas")
    carreira = models.ForeignKey(Carreira, on_delete=models.CASCADE, related_name="estatisticas")
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="estatisticas")
    
    def total_participacoes(self):
        return self.gol + self.assistencia

    def __str__(self):
        return f"{self.jogador} - {self.campeonato} ({self.temporada})"

    
def criar_dados_padrao():
    cria_temporada(data="24/25")
    cria_temporada(data="25/26")
    cria_temporada(data="26/27")
    cria_temporada(data="27/28")
    cria_temporada(data="28/29")
    cria_temporada(data="29/30")
    cria_temporada(data="30/31")
    cria_temporada(data="31/32")
    cria_temporada(data="32/33")
    cria_temporada(data="33/34")
    #cria_time(nome="Liverpool")

def cria_temporada(data:str):
    if not Temporada.objects.filter(data=data):
        Temporada(data=data).save()

def cria_time(nome:str):
    if not Time.objects.filter(nome=nome):
        Time(nome=nome).save()
    

#criar_dados_padrao()