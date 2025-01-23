from django.contrib import admin

# Register your models here.

from .models import Time, Treinador, Jogador, Carreira, Estatistica, Campeonato, Temporada


admin.site.register(Time)
admin.site.register(Treinador)
admin.site.register(Jogador)
admin.site.register(Carreira)
admin.site.register(Estatistica)
admin.site.register(Campeonato)
admin.site.register(Temporada)