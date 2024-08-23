from django.urls import path
from django.shortcuts import redirect
from . import views
urlpatterns = [
    path('home/', views.home, name="home"),
    path('cadastro_filial/', views.cadastro_filial, name="cadastro_filial"),
    path('editar_saldo/<int:id>/', views.editar_saldo, name="editar_saldo"),
]