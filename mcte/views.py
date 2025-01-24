from . import fifa

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404

from .models import Campeonato, Treinador, Jogador, Carreira, Estatistica, Temporada, Time
from .forms import *

def render(request, nome_template: str, contexto={}):
    template = loader.get_template(nome_template)
    return HttpResponse(template.render(contexto, request))


# Página inicial
def index(request):
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
    carreiras = Carreira.objects.filter(usuario=request.user)
    for carreira in carreiras:
        print(carreira.time.logo.url)
        print(carreira.time.logo.name)
    return render(request, 'carreira/selecionar_carreira.html', {'carreiras': carreiras})

@login_required
def minha_carreira(request, id=0):
    if id != 0:
        carreira = get_object_or_404(Carreira, pk=id)
        context = {'carreira': carreira}
        return render(request, 'carreira/carreira.html', context)

# Criar nova carreira
@login_required
def criar_carreira(request):
    if request.method == "POST":
        form = CarreiraForm(request.POST)
        if form.is_valid():
            nova_carreira = form.save(commit=False)
            nova_carreira.usuario = request.user
            nova_carreira.save()
            messages.success(request, "Carreira criada com sucesso!")
            return redirect('selecionar_carreira')
        else:
            messages.error(request, "Ocorreu um erro ao criar a carreira. Verifique os dados e tente novamente.")
    times = Time.objects.filter(criado=False)
    times2 = Time.objects.filter(usuario=request.user)
    treinadores = Treinador.objects.filter(usuario=request.user)
    return render(request, 'carreira/criar_carreira.html', {'times': times, 'times2': times2, 'treinadores': treinadores})


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


# Logout
def logout_view(request):
    logout(request)
    return redirect('index')
