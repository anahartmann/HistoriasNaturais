from django.contrib import admin

from core.models import Animal, ImagemAnimal, Pesquisador, Publicacao, Local, TipoPublicacao, Tematica, GrupoTaxonomico, Fenomeno

# Register your models here.

admin.site.site_header = "Labeco Admin"
admin.site.site_title = "Labeco Admin Portal"
admin.site.index_title = "Bem vindo ao Labeco Admin Portal"

admin.site.register(Animal)
admin.site.register(Pesquisador)
admin.site.register(Publicacao)
admin.site.register(Local)
admin.site.register(TipoPublicacao)
admin.site.register(Tematica)
admin.site.register(GrupoTaxonomico)
admin.site.register(Fenomeno)
admin.site.register(ImagemAnimal)