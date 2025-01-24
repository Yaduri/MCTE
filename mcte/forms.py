from django import forms
from .models import Time, Campeonato, Treinador, Jogador, Carreira

class CampeonatoForm(forms.ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nome', 'logo']

class TreinadorForm(forms.ModelForm):
    class Meta:
        model = Treinador
        fields = ['nome', 'foto']

class JogadorForm(forms.ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'data_nascimento', 'carreira', 'foto', 'clube_atual']

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['nome', 'logo']

class CarreiraForm(forms.ModelForm):
    class Meta:
        model = Carreira
        fields = ['nome', 'time', 'treinador']