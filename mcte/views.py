from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    return render(request, 'mcte\index.html')

def login(request):
    return render(request, 'auth\login.html')
    
    #template = loader.get_template('auth/login.html')
    #return HttpResponse(template.render(context, request))

