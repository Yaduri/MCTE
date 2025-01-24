from .models import *
import requests
from django.shortcuts import get_object_or_404
from time import sleep

API_KEY = '82cc7a11406643bba1f2fff9d50c9197'
BASE_URL = 'https://api.football-data.org/v4/'

def obter_times_compet(compet:str):
    url = f"{BASE_URL}competitions/{compet}/teams"  # Exemplo para Premier League
    #url = f"{BASE_URL}/teams"  # Exemplo para Premier League
    headers = {'X-Auth-Token': API_KEY}
    params = {
        'limit': 9999,
    }
    response = requests.get(url, headers=headers, params=params)
    sleep(2)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def test(nome:str, logo:str):
    teste = Time.objects.filter(nome=nome)
    if not teste:
        aa = Time(nome=nome, logo=logo, usuario=None)
        aa.save()

def testT(nome:str):
    teste = Treinador.objects.filter(nome=nome)
    if not teste:
        aa = Treinador(nome=nome, usuario=None)
        aa.save()

def testP(time:str, jogador:str):
    time = Time.objects.get(nome=time)
    jogador = Jogador(nome=jogador)

def carregar_times(competicao:str):
    times = obter_times_compet(competicao)
    if times:
        for time in times['teams']:
            test(time['name'], time['crest'])
            testT(time['coach']['name'])
            #for jogador in time['squad']:
                #testP(time['name'], jogador['name'])
        else:
            print("Erro ao obter dados.")
            
def apagatudo():
    Carreira.objects.all().delete()
    Time.objects.all().delete()
    Treinador.objects.all().delete()
    
    #TIMES
    
    #('PL') #Premier
    #('PD') #LA liga
    #('BL1') #Bundesliga
    #('FL1') #Ligue 1
    #('PPL') #Liga Portugal
    #('SA') #ITALIA
    #('SSL') #Holanda
    
    #times = ['PL', 'PD', 'BL1', 'FL1', 'PPL', 'SA', 'SSL']
    times = ['PL']
    for time in times:
        carregar_times(time)    
    
    #TREINADORES
    
#apagatudo()



#Time(nome=nome, logo=logo)


