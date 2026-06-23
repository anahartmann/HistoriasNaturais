from django.views.generic import TemplateView
from .models import Animal, Pesquisador, Publicacao

#def index(request):
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animais'] = Animal.objects.all()
        context['pesquisadores'] = Pesquisador.objects.all()
        context['publicacoes'] = Publicacao.objects.all()
        return context
