from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('publicacoes/', views.publicacoes, name='publicacoes'),
    path('fauna/', views.fauna, name='fauna'),
    path('fauna/<int:animal_id>/', views.detalhes_animal, name='detalhes_animal'),
    path('admin/', views.admin, name='admin'),
    path('pesquisas/', views.pesquisas, name='pesquisas'),
    path('ver-500/', views.gerar_erro_500, name='ver-500'),
]

