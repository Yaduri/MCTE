from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/signup/", views.signup, name="signup"),
    path('auth/', include('django.contrib.auth.urls')),
    path('carreira/selecionar', views.carreira, name='carreira'),
    path('carreira/<int:id>', views.carreira, name='carreira'),
    
    path('criar/carreira', views.criar_carreira, name='criar_carreira'),
    path('criar/time', views.criar_time, name='criar_time'),
    path('criar/treinador', views.criar_treinador, name='criar_treinador'),
    
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),
    
]