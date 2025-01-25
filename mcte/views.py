#from . import fifa

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

    def teste():
        # Criar objetos
        carreira1 = Carreira.objects.get(pk=1)

        time1 = Time.objects.get(pk=1)
        time2 = Time.objects.get(pk=2)

        jogador1 = Jogador.objects.create(nome="Jogador 1")
        jogador2 = Jogador.objects.create(nome="Jogador 2")

        # Vincular Carreira, Time e Jogador
        CarreiraTimeJogador.objects.create(carreira=carreira1, time=time1, jogador=jogador1)
        CarreiraTimeJogador.objects.create(carreira=carreira1, time=time1, jogador=jogador2)
    #teste()
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
    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('meu_perfil')
    return render(request, 'mcte/meu_perfil.html', {'user': user})


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


# Criar nova carreira
@login_required
def criar_carreira(request):
    if request.method == "POST":
        nome:str = request.POST['nome']
        time:int = int(request.POST['time'])
        treinador:int = int(request.POST['treinador'])
        try:
            carreira = Carreira(nome=nome, time_atual_id=time, treinador_id=treinador, usuario=request.user)
            carreira.save()
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
            time = Time(nome=nome, usuario=request.user, criado=True)
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
        
        ativo = 'carreiras'
        context = {'carreira': carreira, 'temporadas': temporadas, 'estatisticas': estatisticas, 'ativo': ativo}
        
        return render(request, 'carreira/carreira.html', context)

@login_required
def jogadores(request, car_id:int):
    carreira = get_object_or_404(Carreira, pk=car_id, usuario=request.user)
    ativo = 'jogadores'
    time = get_object_or_404(Time, pk=carreira.time_atual.id)
    jogadores = Jogador.objects.filter(time=time.nome)
    return render(request, 'carreira/jogadores.html', {'carreira': carreira, 'ativo': ativo, 'jogadores': jogadores})

def demitir_jogador(request, jogador_id:int):
    ...

def contratar_jogador_existente(request):
    print(request.GET)
    ...

def contratar_jogador_novo(request):
    ...

def pesquisar_jogadores(request):
    query = request.GET.get('nome_jogador', '')
    if query:
        jogadores = Jogador.objects.filter(nome__icontains=query)
        resultados = [{'id': jogador.id, 'nome': jogador.nome} for jogador in jogadores]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)


def detalhes_jogador(request, jogador_id:int):
    ...

# Logout
def logout_view(request):
    logout(request)
    return redirect('index')
