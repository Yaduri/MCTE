from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def render(request, nome_template:str, contexto = {}):
    template = loader.get_template(nome_template)
    return HttpResponse(template.render(contexto, request))

# Create your views here.
def index(request):
    return render(request, 'mcte/index.html')

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

def signup(request):
    if request.method == "GET":
        return render(request, 'auth/signup.html')
    else:
        username = request.POST["username"]
        email = request.POST["username"]
        password = request.POST["password"]
        if not User.objects.filter(username=username):
            if not User.objects.filter(email=email):
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('index')
        messages.add_message(request, messages.INFO, "Nome de usuário ou email já cadastrado")
        return redirect('signup')
                

def logout_view(request):
    logout(request)
    return redirect('index')