#from . import fifa
from django.db.models import Q
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404

from .models import Campeonato, Treinador, Jogador, Carreira, Estatistica, Temporada, Time, CarreiraTimeJogador
#from .forms import *

def render(request, nome_template: str, contexto={}):
    template = loader.get_template(nome_template)
    return HttpResponse(template.render(contexto, request))


# Página inicial
def index(request):
    if request.user.is_authenticated:
        carreiras_usuario = Carreira.objects.filter(usuario=request.user)
        ativo = 'carreiras'
        return render(request, 'carreira/selecionar_carreira.html', {'carreiras': carreiras_usuario, 'ativo': ativo})
    return render(request, 'mcte/index.html')




# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, "Nome de usuário/email ou senha incorretos")
        return redirect('login')
    return render(request, 'auth/login.html')


# Cadastro de conta
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('index')
        messages.error(request, "Nome de usuário ou email já cadastrado")
        return redirect('signup')
    return render(request, 'auth/signup.html')


# Perfil do usuário
@login_required
def meu_perfil(request):
    user = request.user
    ativo = 'meu perfil'
    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('meu_perfil')
    return render(request, 'mcte/meu_perfil.html', {'user': user, 'ativo': ativo})


# Visualizar carreiras
@login_required
def selecionar_carreira(request):
    carreiras_usuario = Carreira.objects.filter(usuario=request.user)
    ativo = 'carreiras'
    return render(request, 'carreira/selecionar_carreira.html', {'carreiras': carreiras_usuario, 'ativo': ativo})

@login_required
def adicionar_temporada(request, id):
    carreira = get_object_or_404(Carreira, id=id, usuario=request.user)
    if request.method == 'POST':
        nome_temporada = request.POST.get('novaTemporada')
        if nome_temporada:
            Temporada.objects.create(carreira=carreira, data=nome_temporada)
            messages.success(request, 'Temporada adicionada com sucesso!')
        else:
            messages.error(request, 'O nome da temporada é obrigatório.')
    return redirect('minha_carreira', id=carreira.id)

@login_required
def adicionar_campeonato(request, carreira_id):
    if request.method == "POST":
        nome = request.POST.get('nome')
        logo = request.FILES.get('logo')
        campeonato = Campeonato.objects.create(nome=nome, logo=logo, usuario=request.user)
        return redirect('estatisticas', carreira_id)
    return render(request, 'adicionar_campeonato.html')

# Criar nova carreira
@login_required
def criar_carreira(request):
    if request.method == "POST":
        nome:str = request.POST['nome']
        time:int = int(request.POST['time_id'])
        treinador:int = int(request.POST['treinador_id'])
        try:
            carreira = Carreira(nome=nome, time_atual_id=time, treinador_id=treinador, usuario=request.user)
            carreira.save()
            time = Time.objects.get(pk=time)
            jogadores = Jogador.objects.filter(time=time.nome)
            for jogador in jogadores:
                CarreiraTimeJogador.objects.create(carreira=carreira, time=time, jogador=jogador)
            Temporada.objects.create(carreira=carreira, data='24/25')
            messages.success(request, "Carreira criada com sucesso!")
            return redirect('selecionar_carreira')
        except:
            messages.error(request, "Ocorreu um erro ao criar a carreira. Verifique os dados e tente novamente.")
    times = Time.objects.filter(usuario=request.user)
    times2 = Time.objects.filter(criado=False)
    treinadores = Treinador.objects.filter(usuario=request.user)
    treinadores2 = Treinador.objects.filter(criado=False)
    ativo = 'carreiras'
    return render(request, 'carreira/criar_carreira.html', {'times': times, 'times2': times2, 'treinadores': treinadores, 'treinadores2': treinadores2, 'ativo': ativo})


# Criar time
@login_required
def criar_time(request):
    if request.method == "POST":
        nome = request.POST['nome']
        try:
            time = Time(nome=nome, usuario=request.user, criado=True, logo=request.FILES['logo'])
            #time = Time(nome=nome, usuario=request.user, criado=True)
            time.save()
            messages.success(request, "Time criado com sucesso!")
            return redirect('criar_carreira')
        except:
            messages.error(request, "Ocorreu um erro ao criar o time. Verifique os dados e tente novamente.")



# Criar treinador
@login_required
def criar_treinador(request):
    if request.method == "POST":
        nome = request.POST['nome']
        try:
            treinador = Treinador(nome=nome, usuario=request.user, criado=True)
            treinador.save()
            messages.success(request, "Treinador criado com sucesso!")
            return redirect('criar_carreira')
        except:
            messages.error(request, "Ocorreu um erro ao criar o treinador. Verifique os dados e tente novamente.")
    

@login_required
def minha_carreira(request, id=0):
    if id != 0:
        carreira = get_object_or_404(Carreira, pk=id, usuario=request.user)
        temporadas = Temporada.objects.filter(carreira=carreira)
        jogadores = Jogador.objects.filter(usuario=request.user)
        estatisticas = Estatistica.objects.filter(carreira=carreira, jogador__in=jogadores)
        
        ativo = 'minha carreira'
        context = {'carreira': carreira, 'temporadas': temporadas, 'estatisticas': estatisticas, 'ativo': ativo}
        return render(request, 'carreira/carreira.html', context)

@login_required
def jogadores(request, carreira_id:int):
    carreiraTimeJogador = CarreiraTimeJogador.objects.filter(carreira_id=carreira_id, time_atual=True)
    carreira = get_object_or_404(Carreira, pk=carreira_id)
        
    ativo = 'jogadores'
    return render(request, 'carreira/jogadores.html', {'ativo': ativo, 'carr': carreiraTimeJogador, 'carreira': carreira})

@login_required
def demitir_jogador(request, jogador_id:int, carreira_id:int):
    try:
        carreiraTimeJogador = CarreiraTimeJogador.objects.get(carreira_id=carreira_id, jogador_id=jogador_id)
        carreiraTimeJogador.time_atual = False
        carreiraTimeJogador.save()
        messages.success(request, f"{carreiraTimeJogador.jogador.nome} demitido com sucesso!")
        return redirect('jogadores', carreira_id)
    except Exception as err:
        messages.error(request, f"Erro ao demitir {carreiraTimeJogador.jogador.nome}!")
        return redirect('jogadores', carreira_id)

@login_required
def contratar_jogador_existente(request):
    jogador_id = int(request.GET['jogador_id'])
    carreira_id = int(request.GET['carreira_id'])
    carreira = Carreira.objects.get(pk=carreira_id)
    time = carreira.time_atual
    jogador = Jogador.objects.get(pk=jogador_id)
    try:
        carreiraTimeJogador = CarreiraTimeJogador.objects.filter(carreira=carreira, jogador=jogador)
        if not carreiraTimeJogador:
            carreiraTimeJogador = CarreiraTimeJogador.objects.create(carreira=carreira, time=time, jogador=jogador)
        else:
            carreiraTimeJogador = CarreiraTimeJogador.objects.get(carreira=carreira, jogador=jogador)
            carreiraTimeJogador.time_atual = True
        carreiraTimeJogador.save()
        messages.success(request, f"{jogador.nome} contratado!")
        return redirect('jogadores', carreira_id)
    except Exception as err:
                messages.error(request, f"Erro ao contratar!")
                return redirect('jogadores', carreira_id)
    
@login_required
def contratar_jogador_novo(request):
    ...

@login_required
def estatisticas(request, carreira_id: int):
    carreira = get_object_or_404(Carreira, pk=carreira_id, usuario=request.user)
    temporadas = Temporada.objects.filter(carreira=carreira).prefetch_related('estatisticas__jogador')
    campeonatos = Campeonato.objects.filter(usuario=None)
    campeonatos2 = Campeonato.objects.filter(usuario=request.user)
    campeonatos_combinados = chain(campeonatos, campeonatos2)

    campeonatos_combinados = Campeonato.objects.filter(
        Q(usuario=None) | Q(usuario_id=1)
    )

    context = {
        'carreira': carreira,
        'temporadas': temporadas,
        'campeonatos': campeonatos_combinados,
        'ativo': 'estatisticas'
    }
    return render(request, 'carreira/estatisticas.html', context)

@login_required
def adicionar_estatistica(request, carreira_id):
    if request.method == "POST":
        carreira = get_object_or_404(Carreira, pk=carreira_id, usuario=request.user)
        jogador_id = request.POST.get("jogador_id")
        campeonato_id = request.POST.get("campeonato_id")
        temporada_id = request.POST.get("temporada_id")
        jogos = request.POST.get("jogos")
        gols = request.POST.get("gols")
        assistencias = request.POST.get("assistencias")

        try:
            jogador = Jogador.objects.get(pk=jogador_id)
            campeonato = Campeonato.objects.get(pk=campeonato_id)
            temporada = Temporada.objects.get(pk=temporada_id)
            Estatistica.objects.create(
                carreira=carreira,
                jogador=jogador,
                campeonato=campeonato,
                temporada=temporada,
                jogos=jogos,
                gols=gols,
                assistencias=assistencias,
            )
            messages.success(request, "Estatística adicionada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao adicionar estatística: {e}")

    return redirect("estatisticas", carreira_id=carreira_id)

@login_required
def excluir_estatistica(request, estatistica_id):
    estatistica = get_object_or_404(Estatistica, id=estatistica_id)
    estatistica.delete()
    return redirect('estatisticas', carreira_id=estatistica.carreira.id)

@login_required
def editar_estatistica(request, estatistica_id):
    estatistica = get_object_or_404(Estatistica, id=estatistica_id)
    if request.method == 'POST':
        jogos = request.POST['jogos']
        gols = request.POST['gols']
        assistencias = request.POST['assistencias']
        estatistica.jogos = jogos
        estatistica.gols = gols
        estatistica.assistencias = assistencias
        estatistica.save()
    return redirect('estatisticas', carreira_id=estatistica.carreira.id)

@login_required
def estatisticas_temporada(request, carreira_id):
    temporada = request.GET.get('temporada')
    estatisticas = Estatistica.objects.filter(carreira_id=carreira_id, temporada__data=temporada)
    
    # Criando um dicionário para armazenar as estatísticas por jogador
    jogadores_estatisticas = {}

    for estatistica in estatisticas:
        jogador = estatistica.jogador
        if jogador not in jogadores_estatisticas:
            jogadores_estatisticas[jogador] = {
                'jogos': 0,
                'gols': 0,
                'assistencias': 0,
                'foto': jogador.foto.url if jogador.foto else None,
                'competicoes': []
            }
        
        jogadores_estatisticas[jogador]['jogos'] += estatistica.jogos
        jogadores_estatisticas[jogador]['gols'] += estatistica.gols
        jogadores_estatisticas[jogador]['assistencias'] += estatistica.assistencias

        
        if not estatistica.campeonato.logo:
            logo_url = ''
        else:
            logo_url = estatistica.campeonato.logo.url

        # Adicionar as competições
        competicao = {
            'nome': estatistica.campeonato.nome,
            'jogos': estatistica.jogos,
            'gols': estatistica.gols,
            'assistencias': estatistica.assistencias,
            'logo': logo_url,
        }
        jogadores_estatisticas[jogador]['competicoes'].append(competicao)

    # Preparando os dados para enviar
    estatisticas_data = [
        {
            'jogador': jogador.nome,
            'foto': dados['foto'],
            'jogos': dados['jogos'],
            'gols': dados['gols'],
            'assistencias': dados['assistencias'],
            'competicoes': dados['competicoes']
        }
        for jogador, dados in jogadores_estatisticas.items()
    ]
    
    return JsonResponse({'estatisticas': estatisticas_data})

@login_required
def pesquisar_jogadores(request):
    query = request.GET.get('nome_jogador', '')
    if query:
        jogadores = Jogador.objects.filter(nome__icontains=query)
        resultados = [{'id': jogador.id, 'nome': jogador.nome} for jogador in jogadores]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)

@login_required
def pesquisar_times(request):
    query = request.GET.get('nome_time', '')
    if query:
        times = Time.objects.filter(nome__icontains=query)
        resultados = [{'id': time.id, 'nome': time.nome, 'logo': time.logo.url} for time in times]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)

@login_required
def pesquisar_treinadores(request):
    query = request.GET.get('nome_time', '')
    if query:
        treinador = Treinador.objects.filter(nome__icontains=query)
        resultados = [{'id': treinador.id, 'nome': treinador.nome} for treinador in treinador]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)

@login_required
def detalhes_jogador(request, jogador_id:int):
    return redirect('jogadores', 1)
    ...

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
