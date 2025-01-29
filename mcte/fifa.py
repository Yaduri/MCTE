from .models import *
import requests
from django.shortcuts import get_object_or_404
from time import sleep
from django.core.files.base import ContentFile
from bs4 import BeautifulSoup


import unicodedata

def remover_acentos(texto):
    # Normalizar a string para decompor os acentos
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    # Filtrar apenas os caracteres não acentuados
    texto_sem_acento = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
    return texto_sem_acento

def buscar_imagens(nome_jogador, idade_api = 0):
    njo = nome_jogador
    if nome_jogador == 'Hwang': nome_jogador = 'Hwang'
    if 'Mudryk' in nome_jogador: nome_jogador = 'Mudryk'
    njo = nome_jogador
    nome_jogador = nome_jogador.replace(' ', '+')
    url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={nome_jogador}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    imagens = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img', {'class': 'bilderrahmen-fixed'}):
        jgd = img.get('title')
        a = True
        elementos = img.next_elements
        #for elemento in elementos:
            #...
        idade = 0
        while idade == 0:
            elementos = img.next_elements
            num = 0
            for elemento in elementos:
                try:
                    a = elemento.get('class')
                    if a[0] == 'zentriert':
                        num += 1
                        if num == 3:
                            try:
                                idade:int = int(elemento.contents[0])
                                break 
                            except:
                                idade = 1
                                break
                    elif a == 'tiny_wappen':
                        time = elemento.get('title')
                        ...

                except:
                    ...
            #idade = 1
            break
        njo = remover_acentos(njo)
        jgd = remover_acentos(jgd)
        if 'Mudryk' in njo or 'Hwang' in njo:
            print('')
        if idade == idade_api:
            #imagens.append({'nome': img.get('title'), 'url': img.get('src')})
            #break
            if ((jgd == njo) or (njo in jgd) or (jgd in njo)) and jgd != 'Martinelli':
                imagens.append({'nome': img.get('title'), 'url': img.get('src')})
                break
            elif 'Hwang' in njo:
                imagens.append({'nome': img.get('title'), 'url': img.get('src')})
                break
            elif njo == 'Ezri Konsa' or njo == 'Cristian Romero' or njo == 'Jeremy Doku' or njo == 'Victor Nilsson-Lindelof':
                imagens.append({'nome': img.get('title'), 'url': img.get('src')})
    
    if len(imagens) == 0:
        imagens.append({'nome': njo, 'url': 'https://img.a.transfermarkt.technology/portrait/header/default.jpg?lm=1'})
        

    return imagens

def buscar_imagem_treinador(nome_treinador:str):
    njo = nome_treinador
    nome_treinador = nome_treinador.replace(' ', '+')
    url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={nome_treinador}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    imagens = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for img in soup.find_all('img', {'class': 'bilderrahmen-fixed'}):
        trei = img.get('title')
        a = True
        elementos = img.next_elements
        manager = False
        while True:
            num = 0
            for elemento in elementos:
                try:
                    a = elemento.get('class')
                    if a[0] == 'rechts' and elemento.contents[0] == 'Manager':
                        manager = True
                        break
                    if a[0] == 'bilderrahmen-fixed':
                        break
                except:
                    ...
            break
        if manager:
            imagens.append({'nome': img.get('title'), 'url': img.get('src')})
            break
            
    
    if len(imagens) == 0:
        imagens.append({'nome': njo, 'url': 'https://img.a.transfermarkt.technology/portrait/header/default.jpg?lm=1'})
        

    return imagens
    
def salvar_imagem_time(url_img, instancia_model, nome_time):
    try:
        # Faz o download da imagem
        resposta = requests.get(url_img, stream=True)
        resposta.raise_for_status()  # Garante que não houve erro no download

        # Extrai o nome do arquivo da URL
        #nome_arquivo = nome_time + ' - ' + url_img.split("/")[-1]
        nome_arquivo = nome_time + '.png'

        # Salva o arquivo na instância do modelo
        instancia_model.logo.save(nome_arquivo, ContentFile(resposta.content), save=True)
    except requests.RequestException as e:
        print(f"Erro ao fazer o download da imagem: {e}")
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")

def salvar_imagem_local_time(objeto, caminho_imagem):
    if not os.path.exists(caminho_imagem):
        return False
    try:
        with open(caminho_imagem, 'rb') as arquivo_imagem:
            objeto.logo.save(os.path.basename(caminho_imagem), File(arquivo_imagem), save=True)
            return True
    except Exception as err:
        print(err)
    return False

import os
from django.core.files import File
from .models import Jogador
from django.conf import settings

def salvar_imagem_local_jogador(jogador, caminho_imagem):
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_imagem):
        #print(f"Erro: O arquivo {caminho_imagem} não existe.")
        return False
    try:
        # Abrir o arquivo de imagem
        with open(caminho_imagem, 'rb') as arquivo_imagem:
            # Salvar a imagem no campo `foto`
            jogador.foto.save(os.path.basename(caminho_imagem), File(arquivo_imagem), save=True)
            return True
    except Exception as err:
        print(err)
    return False

def salvar_imagem_jogador(instancia_model:Jogador, nome_jogador, idade_api):
    try:
        imagens = buscar_imagens(nome_jogador, idade_api)
        for img in imagens:    
            url:str = img['url']
            url = url.replace('/small/', '/header/')
            url = url.replace('?lm=1', '')
            resposta = requests.get(url, stream=True)
            
            resposta.raise_for_status()  # Garante que não houve erro no download

            nome_arquivo = nome_jogador + '.jpg'#+ ' - ' + img['url'].split("/")[-1]

            instancia_model.foto.save(nome_arquivo, ContentFile(resposta.content), save=True)
    except requests.RequestException as e:
        print(f"Erro ao fazer o download da imagem: {e}")
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")


API_KEY = '82cc7a11406643bba1f2fff9d50c9197'
BASE_URL = 'https://api.football-data.org/v4/'

def obter_compet(nome_comept:str):
    url = f"{BASE_URL}competitions/{nome_comept}"  # Exemplo para Premier League
    #url = f"{BASE_URL}/teams"  # Exemplo para Premier League
    headers = {'X-Auth-Token': API_KEY}
    params = {
        'limit': 9999,
    }
    response = requests.get(url, headers=headers, params=params)
    sleep(1) #era 2
    if response.status_code == 200:
        return response.json()
    else:
        return None

def obter_times_compet(compet:str):
    url = f"{BASE_URL}competitions/{compet}/teams"  # Exemplo para Premier League
    #url = f"{BASE_URL}/teams"  # Exemplo para Premier League
    headers = {'X-Auth-Token': API_KEY}
    params = {
        'limit': 9999,
    }
    response = requests.get(url, headers=headers, params=params)
    sleep(1) #era 2
    if response.status_code == 200:
        return response.json()
    else:
        return None

def verifica_time(nome:str, logo:str):
    teste = Time.objects.filter(nome=nome)
    if not teste:
        #aa = Time(nome=nome, logo=logo, usuario=None)
        aa = Time(nome=nome, usuario=None)
        aa.save()
        caminho = 'C:\Yago\Python\Django\MCTE\imagens_times/'+nome+'.png'
        if not salvar_imagem_local_time(aa, caminho):
            salvar_imagem_time(logo, aa, nome)

def salvar_imagem_treinador(nome, instancia_model):
    
    try:
        imagens = buscar_imagem_treinador(nome)
        for img in imagens:    
            url:str = img['url']
            url = url.replace('/small/', '/header/')
            url = url.replace('?lm=1', '')
            resposta = requests.get(url, stream=True)
            
            resposta.raise_for_status()  # Garante que não houve erro no download

            nome_arquivo = nome + '.jpg'#+ ' - ' + img['url'].split("/")[-1]

            instancia_model.foto.save(nome_arquivo, ContentFile(resposta.content), save=True)
    except requests.RequestException as e:
        print(f"Erro ao fazer o download da imagem: {e}")
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")

def verifica_treinador(nome:str):
    treinador:Treinador = Treinador.objects.filter(nome=nome)
    if not treinador:
        treinador = Treinador(nome=nome, usuario=None)
        treinador.save()
        caminho = 'C:\Yago\Python\Django\MCTE\imagens_treinadores/'+nome+'.jpg'
        if not salvar_imagem_local_jogador(treinador, caminho):
            salvar_imagem_treinador(nome, treinador)
    else:
        if not treinador[0].foto:
            caminho = 'C:\Yago\Python\Django\MCTE\imagens_treinadores/'+nome+'.jpg'
            if not salvar_imagem_local_jogador(treinador[0], caminho):
                salvar_imagem_treinador(nome, treinador[0])
        

def verifica_jogador(time:str, jogador:str, posicao:str, idade_api):
    teste = Jogador.objects.filter(nome=jogador)
    posicoes = {
        'Defensive Midfield': 'VOL',
        'Goalkeeper': 'GL',
        'Defence': 'ZAG',
        'Centre-Back': 'ZAG',
        'Right-Back': 'LD',
        'Left-Back': 'LE',
        'Centre-Forward': 'ATA',
        'Central Midfield': 'MC',
        'Left Winger': 'PE',
        'Midfield': 'MC',
        'Attacking Midfield': 'MEI',
        'Right Winger': 'PD',
        'Offence': 'SA',
        'Right Midfield': 'MD',
        'Left Midfield': 'ME',
        'Midfield': 'MC',
    }
    try:
        if not teste:
            posicao = posicoes.get(posicao, posicao)
            if len(posicao) > 3:
                print(posicao)
            jogadors = Jogador(nome=jogador, posicao=posicao, time=time)
            jogadors.save()
            nome_jogador = jogador.replace(' ', '_')
            caminho = 'C:\Yago\Python\Django\MCTE\imagens_jogadores/'+nome_jogador+'.jpg'
            if not salvar_imagem_local_jogador(jogadors, caminho):
                salvar_imagem_jogador(jogadors, jogador, idade_api)
    except:
        ...

from datetime import datetime

def carregar_times(competicao:str):
    times = obter_times_compet(competicao)
    if times:
            
        for time in times['teams']:
            verifica_time(time['name'], time['crest'])
            verifica_treinador(time['coach']['name'])
            for jogador in time['squad']:
                data_nascimento = jogador['dateOfBirth']
                idade_api = 0
                if data_nascimento:
                    dateOfBirth = datetime.strptime(data_nascimento, '%Y-%m-%d')
                    hoje = datetime.today()
                    idade_api = hoje.year - dateOfBirth.year
                    if (hoje.month, hoje.day) < (dateOfBirth.month, dateOfBirth.day):
                        idade_api -= 1
                verifica_jogador(time['name'], jogador['name'], jogador['position'], idade_api)
        else:
            print(f"{competicao}")


def buscar_areas():
    url = f"{BASE_URL}areas"
    headers = {'X-Auth-Token': API_KEY}
    params = {
        'limit': 9999,
    }
    response = requests.get(url, headers=headers, params=params)
    sleep(1) #era 2
    if response.status_code != 200:
        return False
    else:
        return response.json()

def buscar_compets(areas:list):
    url = f"{BASE_URL}competitions/"
    headers = {'X-Auth-Token': API_KEY}
    params = {
        'limit': 9999,
        'areas': ','.join(areas)
    }
    response = requests.get(url, headers=headers, params=params)
    sleep(1)
    if response.status_code != 200:
        return
    else:
        return response.json()

def cria_competicoes(cod_compet:str):
    response = obter_times_compet(cod_compet)
    if response:
        competicao = response['competition']
        emblema_url = competicao['emblem']
        nome_competicao = competicao['name']
        compet = Campeonato.objects.filter(nome=nome_competicao)
        if not compet:
            compet = Campeonato(nome=nome_competicao, usuario=None)
            compet.save()
            caminho = 'C:\Yago\Python\Django\MCTE\imagens_campeonatos/'+nome_competicao+'.png'
            if not salvar_imagem_local_time(compet, caminho):
                salvar_imagem_time(emblema_url, compet, nome_competicao)
        for time in response['teams']:
            verifica_time(time['name'], time['crest'])
            verifica_treinador(time['coach']['name'])
            for jogador in time['squad']:
                data_nascimento = jogador['dateOfBirth']
                idade_api = 0
                if data_nascimento:
                    dateOfBirth = datetime.strptime(data_nascimento, '%Y-%m-%d')
                    hoje = datetime.today()
                    idade_api = hoje.year - dateOfBirth.year
                    if (hoje.month, hoje.day) < (dateOfBirth.month, dateOfBirth.day):
                        idade_api -= 1
                verifica_jogador(time['name'], jogador['name'], jogador['position'], idade_api)
        
            

def cria_tudo():
    areas = buscar_areas()
    lista_areas = ['England', 'Spain', 'France', 'Germany', 'Portugal', 'Italy', 'Netherlands', 'United States', 'Belgium'] # 'Brazil'
    codigos = []
    for area in areas['areas']:
        if area['name'] in lista_areas:
            codigos.append(str(area['id']))
    
    competicoes = buscar_compets(codigos)
    for competicao in competicoes['competitions']:
        cria_competicoes(competicao['id'])
    outras = ['CL', 'EL', 'UCL']
    for time in outras:
        carregar_times(time)
                
    
def apagatudo(apaga, cria_times, cria_compet):
    if apaga:
        #Carreira.objects.all().delete()
        #Time.objects.all().delete()
        #Treinador.objects.all().delete()
        Jogador.objects.all().delete()
        ...
    
    #TIMES
    
    #('PL') #Premier
    #('PD') #LA liga
    #('BL1') #Bundesliga
    #('FL1') #Ligue 1
    #('PPL') #Liga Portugal
    #('SA') #ITALIA
    #('SSL') #Holanda
    if cria_times:
        times = ['PL', 'PD', 'BL1', 'FL1', 'PPL', 'SA', 'SSL']
        #times = ['PL']
        for time in times:
            carregar_times(time)

#apagatudo(False, True, True)
def apagar_fotos_treinadores():
    treinadores = Treinador.objects.all()
    for treinador in treinadores:
        if treinador.foto:  # Verifica se há uma foto associada
            treinador.foto.delete(save=True)  # Remove a foto e salva a mudança
    print("Fotos de todos os treinadores foram apagadas.")

#apagar_fotos_treinadores()
#cria_tudo()

print('acabou')
