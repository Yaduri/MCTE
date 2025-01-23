from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/signup/", views.signup, name="signup"),
    path('auth/', include('django.contrib.auth.urls')),
    path('carreira/', views.carreira, name='carreira'),
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),
]