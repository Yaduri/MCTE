from django.contrib import admin

# Register your models here.

from .models import Time, Treinador, Jogador, Carreira


admin.site.register(Time)
admin.site.register(Treinador)
admin.site.register(Jogador)
admin.site.register(Carreira)