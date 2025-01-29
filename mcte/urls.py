from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/signup/", views.signup, name="signup"),
    path('auth/', include('django.contrib.auth.urls')),
    
    path('carreira/selecionar', views.selecionar_carreira, name='selecionar_carreira'),
    path('carreira/<int:id>', views.minha_carreira, name='minha_carreira'),
    path('carreira/<int:id>/adicionar_temporada/', views.adicionar_temporada, name='adicionar_temporada'),
    path("carreira/<int:carreira_id>/estatisticas/", views.estatisticas, name="estatisticas"),
    path("carreira/<int:carreira_id>/adicionar-estatistica/", views.adicionar_estatistica, name="adicionar_estatistica"),
    path('carreira/<int:carreira_id>/estatisticas-temporada/', views.estatisticas_temporada, name='estatisticas_temporada'),
    path('carreira/<int:carreira_id>/campeonatos/', views.campeonatos, name='campeonatos'),
    path('campeonatos/toggle/', views.toggle_campeonato_status, name='toggle_campeonato_status'),
    path('jogador/titular/toggle/', views.toggle_jogador_titular, name='toggle_jogador_titular'),
    
    path('carreira/<int:carreira_id>/jogadores/', views.jogadores, name='jogadores'),
    path('carreira/jogadores/pesquisar/', views.pesquisar_jogadores, name='pesquisar_jogadores'),
    
    path('estatistica/excluir/<int:estatistica_id>/', views.excluir_estatistica, name='excluir_estatistica'),
    path('estatistica/editar/<int:estatistica_id>/', views.editar_estatistica, name='editar_estatistica'),
    
    path('adicionar_campeonato/<int:carreira_id>', views.adicionar_campeonato, name='adicionar_campeonato'),

    
    
    path('times/pesquisar/', views.pesquisar_times, name='pesquisar_times'),
    path('treinadores/pesquisar/', views.pesquisar_treinadores, name='pesquisar_treinadores'),
    
    path('jogador/demitir/<int:jogador_id>/<int:carreira_id>', views.demitir_jogador, name='demitir_jogador'),
    path('jogador/contratar/', views.contratar_jogador_existente, name='contratar_jogador_existente'),
    path('jogador/contratar_novo/', views.contratar_jogador_novo, name='contratar_jogador_novo'),
    path('jogador/detalhes/<int:carreira_id>/<int:jogador_id>', views.detalhes_jogador, name='detalhes_jogador'),
    
    
    
    
    path('criar/carreira', views.criar_carreira, name='criar_carreira'),
    path('criar/time', views.criar_time, name='criar_time'),
    path('criar/treinador', views.criar_treinador, name='criar_treinador'),
    
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),
    
]


