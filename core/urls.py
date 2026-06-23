from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('publicacoes/', views.publicacoes, name='publicacoes'),
    path('fauna/', views.fauna, name='fauna'),
]

