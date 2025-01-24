from . import fifa

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
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
    carreiras = []
    #for carreira in carreiras_usuario:
        #ctj = CarreiraTimeJogador.objects.filter(carreira=carreira)
        #print(ctj.carreira)
        #print(ctj.time)
        #print(ctj.jogador)
    for carreira in carreiras_usuario:
        print(carreira.time_atual.logo.url)
        print(carreira.time_atual.logo.name)
    return render(request, 'carreira/selecionar_carreira.html', {'carreiras': carreiras_usuario})

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
    return render(request, 'carreira/criar_carreira.html', {'times': times, 'times2': times2, 'treinadores': treinadores, 'treinadores2': treinadores2})


# Criar time
@login_required
def criar_time(request):
    if request.method == "POST":
        if request.FILES:
            request.FILES['logo'].name = request.user.username + ' - ' + request.FILES['logo'].name
        form = TimeForm(request.POST, request.FILES)
        if form.is_valid():
            time = form.save(commit=False)
            time.usuario = request.user
            time.save()
            messages.success(request, "Time criado com sucesso!")
            return redirect('criar_carreira')
        else:
            messages.error(request, "Ocorreu um erro ao criar o time. Verifique os dados e tente novamente.")
    else:
        form = TimeForm()
        return render(request, 'carreira/criar_time.html', {'form': form})


# Criar treinador
@login_required
def criar_treinador(request):
    if request.method == "POST":
        if request.FILES:
            request.FILES['foto'].name = request.user.username + ' - ' + request.FILES['foto'].name
        form = TreinadorForm(request.POST, request.FILES)
        if form.is_valid():
            treinador = form.save(commit=False)
            treinador.usuario = request.user
            treinador.save()
            messages.success(request, "Treinador criado com sucesso!")
            return redirect('criar_carreira')
        else:
            messages.error(request, "Ocorreu um erro ao criar o treinador. Verifique os dados e tente novamente.")
        #nome = request.POST["nome"]
        #Treinador.objects.create(nome=nome, usuario=request.user)
        #messages.success(request, "Treinador criado com sucesso!")
        #return redirect('criar_carreira')
    return render(request, 'carreira/criar_treinador.html')

@login_required
def minha_carreira(request, id=0):
    if id != 0:
        carreira = get_object_or_404(Carreira, pk=id, usuario=request.user)
        temporadas = Temporada.objects.filter(carreira=carreira)
        context = {'carreira': carreira, 'temporadas': temporadas}
        return render(request, 'carreira/carreira.html', context)

# Logout
def logout_view(request):
    logout(request)
    return redirect('index')
