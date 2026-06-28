from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Animal, Fenomeno, GrupoTaxonomico, ImagemAnimal, Local, Pesquisa, Pesquisador, Publicacao, Tematica, TipoPublicacao
import unicodedata

def remover_acentos(texto):
    if not texto:
        return ''
    return ''.join(
        caractere for caractere in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(caractere)
    ).lower()

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
    search = request.GET.get('search', '').strip()
    termo = remover_acentos(search)
    fenomeno_selecionado = converter_para_int(request.GET.get('fenomeno'))
    grupo_selecionado = converter_para_int(request.GET.get('grupo'))
    local_selecionado = converter_para_int(request.GET.get('local'))

    animais = ImagemAnimal.objects.all()

    if fenomeno_selecionado:
        animais = animais.filter(fenomeno_id=fenomeno_selecionado)

    if grupo_selecionado:
        animais = animais.filter(grupo_id=grupo_selecionado)

    if local_selecionado:
        animais = animais.filter(local__id=local_selecionado)

    if termo:
        animais = [
            animal for animal in animais
            if termo in remover_acentos(animal.animal.nome_comum.lower())
            or termo in remover_acentos(animal.animal.nome_cientifico.lower())
        ]
    else:
        animais = list(animais) 
        
    grupos_disponiveis = GrupoTaxonomico.objects.filter(
    imagemanimal__in=animais
    ).distinct().order_by('nome')

    fenomenos_disponiveis = Fenomeno.objects.filter(
    imagemanimal__in=animais
    ).distinct().order_by('nome')

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
        'fenomenos': fenomenos_disponiveis,
        'grupos': grupos_disponiveis,
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
    pesquisadores = Pesquisador.objects.all()
    return render(request, 'sobre.html', {'pesquisadores': pesquisadores})
   

def publicacoes(request):
    search = request.GET.get('search', '').strip()
    termo = remover_acentos(search)
    tematica = converter_para_int(request.GET.get('tematica'))
    grupo_selecionado = converter_para_int(request.GET.get('grupo'))
    ano = converter_para_int(request.GET.get('ano'))
    tipo_publicacao = converter_para_int(request.GET.get('tipo_publicacao'))
    pesquisas = converter_para_int(request.GET.get('pesquisa'))

    publicacoes = Publicacao.objects.all()

    if tematica:
        publicacoes = publicacoes.filter(tematica_id=tematica)
    
    if grupo_selecionado:
        publicacoes = publicacoes.filter(grupo_id=grupo_selecionado)

    if ano:
        publicacoes = publicacoes.filter(ano=ano)

    if tipo_publicacao:
        publicacoes = publicacoes.filter(tipo_id=tipo_publicacao)
    
    if pesquisas:
        publicacoes = publicacoes.filter(pesquisa_id=pesquisas)
   
    if termo:
        publicacoes = [
            publicacao for publicacao in publicacoes
            if termo in remover_acentos(publicacao.titulo.lower())
            or any(termo in remover_acentos(autor.nome.lower()) for autor in publicacao.autores.all())
        ]
    else:
        publicacoes = list(publicacoes)
        
    grupos_disponiveis = GrupoTaxonomico.objects.filter(
    publicacao__in=publicacoes
    ).distinct().order_by('nome')

    tipos_disponiveis = TipoPublicacao.objects.filter(
    publicacao__in=publicacoes
    ).distinct().order_by('nome')

    tematica_disponiveis = Tematica.objects.filter(
    publicacao__in=publicacoes
    ).distinct().order_by('nome')
        
    paginator = Paginator(publicacoes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    parametros = request.GET.copy()
    if 'page' in parametros:
        del parametros['page']

    query_string = parametros.urlencode()
    page_prefix = f'{query_string}&' if query_string else ''

    dados = {
        'page_obj': page_obj,
        'tematicas': tematica_disponiveis,
        'grupos': grupos_disponiveis,
        'anos': Publicacao.objects.values_list('ano', flat=True).distinct().order_by('ano'),
        'pesquisas': Pesquisa.objects.all().order_by('titulo'),
        'tipos_publicacao': tipos_disponiveis,
        'search': search or '',
        'tematica_selecionada': tematica,
        'grupo_selecionado': grupo_selecionado,
        'ano_selecionado': ano,
        'tipo_publicacao_selecionado': tipo_publicacao,
        'pesquisa_selecionada': pesquisas,
        'page_prefix': page_prefix,
    }
    
    return render(request, 'publicacao.html', dados)

def detalhes_animal(request, animal_id):
    animal = get_object_or_404(ImagemAnimal, id=animal_id)
    registros = ImagemAnimal.objects.select_related(
    "local",
    "animal"
    ).filter(animal=animal.animal)
    return render(request, 'animais.html', {'animal': animal, 'registros': registros})

def admin(request):
    return render(request, 'admin.html')

def pesquisas(request):
    search = request.GET.get('search', '').strip()
    termo = remover_acentos(search)
    responsavel = converter_para_int(request.GET.get('responsavel'))
    nivel = converter_para_int(request.GET.get('nivel'))

    pesquisas = Pesquisa.objects.all()
    
    #pode ter mais de um repsonsavel, por isso é necessario filtrar com o metodo filter e nao get
    if responsavel:
        pesquisas = pesquisas.filter(pesquisadores__id=responsavel)

    status = request.GET.get('status')
    if status:
        pesquisas = pesquisas.filter(status=status)

    if nivel:
        pesquisas = pesquisas.filter(nivel_id=nivel)

    responsaveis_disponiveis = Pesquisador.objects.filter(
    pesquisa__in=pesquisas
    ).distinct().order_by('nome')

    if termo:
        pesquisas = [
            p for p in pesquisas
            if termo in remover_acentos(p.titulo.lower())
        ]
    else:
        pesquisas = list(pesquisas)

    paginator = Paginator(pesquisas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    parametros = request.GET.copy()
    if 'page' in parametros:
        del parametros['page']

    query_string = parametros.urlencode()
    page_prefix = f'{query_string}&' if query_string else ''

    dados = {
        'page_obj': page_obj,
        'responsaveis': responsaveis_disponiveis,
        'status': Pesquisa.objects.values_list('status', flat=True).distinct().order_by('status'),
        'niveis': Pesquisa.objects.values_list('nivel', flat=True).distinct().order_by('nivel'),
        'search': search or '',
        'responsavel_selecionado': responsavel,
        'status_selecionado': status,
        'nível_selecionado': nivel,
        'page_prefix': page_prefix,
    }
    
    return render(request, 'pesquisas.html', dados)