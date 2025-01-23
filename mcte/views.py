from django.http import HttpResponse
from django.template import loader

def render(request, nome_template:str, contexto = {}):
    template = loader.get_template(nome_template)
    return HttpResponse(template.render(contexto, request))

# Create your views here.
def index(request):
    return render(request, 'mcte/index.html')

def login(request):
    template = loader.get_template('auth/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

