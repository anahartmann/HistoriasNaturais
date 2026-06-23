from django.views.generic import TemplateView

from .models import Animal, Pesquisador, Publicacao
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animais'] = Animal.objects.all()
        context['pesquisadores'] = Pesquisador.objects.all()
        context['publicacoes'] = Publicacao.objects.all()
        return context

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def publicacoes(request):
    return render(request, 'publicacao.html')

def fauna(request):
    return render(request, 'imagens.html')