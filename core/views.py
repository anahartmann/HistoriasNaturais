from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Animal, Fenomeno, GrupoTaxonomico, Local, Pesquisador, Publicacao

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animais'] = Animal.objects.all()
        context['pesquisadores'] = Pesquisador.objects.all()
        context['publicacoes'] = Publicacao.objects.all()
        return context


def converter_para_int(valor):
    try:
        return int(valor) if valor else None
    except ValueError:
        return None


def fauna(request):
    search = request.GET.get('search')
    fenomeno_selecionado = converter_para_int(request.GET.get('fenomeno'))
    grupo_selecionado = converter_para_int(request.GET.get('grupo'))
    local_selecionado = converter_para_int(request.GET.get('local'))

    animais = Animal.objects.all()

    if search:
        animais = animais.filter(
            Q(nome_comum__icontains=search) |
            Q(nome_cientifico__icontains=search)
        )

    if fenomeno_selecionado:
        animais = animais.filter(fenomeno_id=fenomeno_selecionado)

    if grupo_selecionado:
        animais = animais.filter(grupo_id=grupo_selecionado)

    if local_selecionado:
        animais = animais.filter(local__id=local_selecionado)

    animais = animais.distinct()

    paginator = Paginator(animais, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    parametros = request.GET.copy()
    if 'page' in parametros:
        del parametros['page']

    query_string = parametros.urlencode()
    page_prefix = f'{query_string}&' if query_string else ''

    dados = {
        'page_obj': page_obj,
        'fenomenos': Fenomeno.objects.all().order_by('nome'),
        'grupos': GrupoTaxonomico.objects.all().order_by('nome'),
        'locais': Local.objects.all().order_by('nome'),
        'search': search or '',
        'fenomeno_selecionado': fenomeno_selecionado,
        'grupo_selecionado': grupo_selecionado,
        'local_selecionado': local_selecionado,
        'page_prefix': page_prefix,
    }

    return render(request, 'imagens.html', dados)

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def publicacoes(request):
    return render(request, 'publicacao.html')
