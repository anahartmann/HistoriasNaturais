from django.contrib import admin

from core.models import Animal, ImagemAnimal, Pesquisa, Pesquisador, Publicacao, Local, TipoPublicacao, Tematica, GrupoTaxonomico, Fenomeno

# Register your models here.

admin.site.site_header = "Labeco Admin"
admin.site.site_title = "Labeco Admin Portal"
admin.site.index_title = "Bem vindo ao Labeco Admin Portal"

admin.site.register(Animal)
admin.site.register(Pesquisador, list_display=('nome', 'titulo', 'email'))
admin.site.register(Publicacao)
admin.site.register(Local)
admin.site.register(TipoPublicacao)
admin.site.register(Tematica)
admin.site.register(GrupoTaxonomico)
admin.site.register(Fenomeno)
class ImagemAnimalAdmin(admin.ModelAdmin):
    list_display = ('get_animais', 'fenomeno', 'local')
    
    def get_animais(self, obj):
        return ', '.join([a.nome_comum for a in obj.animais.all()])
    get_animais.short_description = 'Animais'

admin.site.register(ImagemAnimal, ImagemAnimalAdmin)
admin.site.register(Pesquisa)