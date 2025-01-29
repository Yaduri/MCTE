import django.shortcuts
from django.template import loader
from django.http import HttpResponse

def render(request, nome_template: str, contexto={}):
    template = loader.get_template(nome_template)
    return HttpResponse(template.render(contexto, request))

def erro_404(request, exception):
    return django.shortcuts.render(request, "auth/erro_404.html", {'status': 404})