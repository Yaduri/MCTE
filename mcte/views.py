from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from .models import Campeonato, Treinador, Jogador, Carreira, Estatistica, Temporada, Time

def render(request, nome_template:str, contexto = {}):
    template = loader.get_template(nome_template)
    return HttpResponse(template.render(contexto, request))

# Create your views here.
def index(request):
    return render(request, 'mcte/index.html')

# Login
def login_view(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.INFO, "Nome de usuário/email ou senha incorretos")
            return redirect('login')

# Cadastro Conta
def signup(request):
    if request.method == "GET":
        return render(request, 'auth/signup.html')
    else:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if not User.objects.filter(username=username):
            if not User.objects.filter(email=email):
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('index')
        messages.add_message(request, messages.INFO, "Nome de usuário ou email já cadastrado")
        return redirect('signup')

@login_required
def meu_perfil(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "GET":
        return render(request, 'mcte/meu_perfil.html')
    user.username = request.POST["username"]
    user.email = request.POST["email"]
    user.first_name = request.POST["first_name"]
    user.last_name = request.POST["last_name"]
    user.save()
    return redirect('meu_perfil')

                
@login_required
def carreira(request, id = 0):
    print(id)
    carreiras = Carreira.objects.filter(usuario=request.user)
    context = {
        'carreiras': carreiras
    }
    return render(request, 'carreira/carreira.html', context)


def criar_carreira(request):
    """
    Nome
    Time
    Treinador
    Usuario
    """
    if request.method == "GET":
        times = Time.objects.filter(usuario=request.user)
        treinadores = Treinador.objects.filter(usuario=request.user)
        context = {
            'times': times,
            'treinadores': treinadores
        }
        return render(request, 'carreira/criar_carreira.html', context)
    nome = request.POST["nome"]
    time = Time.objects.get(pk=int(request.POST["time"]))
    treinador = Treinador.objects.get(pk=int(request.POST["treinador"]))
    nova_carreira = Carreira(nome=nome, time=time, treinador=treinador, usuario=request.user)
    nova_carreira.save()
    return redirect('carreira')
    
    

def criar_time(request):
    #NOME
    #USUARIO
    if request.method == "GET":
        return render(request, 'carreira/criar_time.html')
    nome = request.POST["nome"]
    time = Time(nome=nome, usuario=request.user)
    time.save()
    return redirect('criar_carreira')

def criar_treinador(request):
    #NOME
    #USUARIO
    if request.method == "GET":
        return render(request, 'carreira/criar_treinador.html')
    nome = request.POST["nome"]
    treinador = Treinador(nome=nome, usuario=request.user)
    treinador.save()
    return redirect('criar_carreira')
    
    

def logout_view(request):
    logout(request)
    return redirect('index')