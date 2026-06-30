import uuid

from django.db import models
from PIL import Image

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from stdimage.models import StdImageField

def buscar_ext(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class Animal(models.Model):
    nome_comum = models.CharField('Nome Comum', max_length=100)
    nome_cientifico = models.CharField('Nome Científico', max_length=100)
    grupo = models.ForeignKey('core.GrupoTaxonomico', verbose_name='Grupo Taxonômico', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
    
    def __str__(self):        
        return self.nome_comum
    
class ImagemAnimal(models.Model):
    animal = models.ForeignKey('core.Animal', verbose_name='Animal', on_delete=models.CASCADE)
    fenomeno = models.ForeignKey('core.Fenomeno', verbose_name='Fenômeno', on_delete=models.CASCADE)
    local = models.ForeignKey('core.Local', verbose_name='Locais', on_delete=models.CASCADE)
    midia = models.FileField('Mídia (Foto ou Vídeo)', upload_to=buscar_ext, null=True, blank=True)

    class Meta:
        verbose_name = 'Imagem de Animal'
        verbose_name_plural = 'Imagens de Animais'
    def __str__(self):
        return f'{self.animal.nome_comum} - {self.fenomeno.nome} - {self.local.nome}'

class Pesquisador(models.Model):
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', max_length=100)
    #titulo so pode ser doutor ou mestre, por isso é uma escolha entre essas duas opções
    TITULOS = [
        ('Doutor', 'Doutor'),
        ('Mestre', 'Mestre'),
        ('Graduando', 'Graduando'),
        ('Pós-Doutor', 'Pós-Doutor'),
        ('Mestrando', 'Mestrando'),
        ('Doutorando', 'Doutorando'),
    ]
    titulo = models.CharField('Título', max_length=10, choices=TITULOS, default='Graduando')
    lattes = models.URLField('Lattes', max_length=1000, null=True, blank=True)
    foto = StdImageField('Foto', upload_to=buscar_ext, variations={'thumb': (300, 300)}, null=True, blank=True)

    class Meta:
        verbose_name = 'Pesquisador'
        verbose_name_plural = 'Pesquisadores'
    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    #tipo de publicação (artigo, livro, capítulo de livro), temática, autores, grupo taxonômico e ano de publicação.
    titulo = models.CharField('Título', max_length=100)
    tipo = models.ForeignKey('core.TipoPublicacao', verbose_name='Tipo de Publicação', on_delete=models.CASCADE)
    tematica = models.ForeignKey('core.Tematica', verbose_name='Temática', on_delete=models.CASCADE)
    autores = models.ManyToManyField('core.Pesquisador', verbose_name='Autores')
    grupo = models.ForeignKey('core.GrupoTaxonomico', verbose_name='Grupo Taxonômico', on_delete=models.CASCADE)
    ano = models.IntegerField('Ano de Publicação')
    link = models.URLField('Link', max_length=1000)
    pesquisa = models.ForeignKey('core.Pesquisa', verbose_name='Pesquisa', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'
    def __str__(self):
        return self.titulo

class TipoPublicacao(models.Model):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Tipo de Publicação'
        verbose_name_plural = 'Tipos de Publicações'

    def __str__(self):
        return self.nome

class Tematica(models.Model):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Temática'
        verbose_name_plural = 'Temáticas'

    def __str__(self):
        return self.nome

class GrupoTaxonomico(models.Model):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Grupo Taxonômico'
        verbose_name_plural = 'Grupos Taxonômicos'

    def __str__(self):
        return self.nome

class Fenomeno(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', max_length=2000)

    class Meta:
        verbose_name = 'Fenômeno'
        verbose_name_plural = 'Fenômenos'

    def __str__(self):
        return self.nome

class Local(models.Model):
    nome = models.CharField('Nome', max_length=100, unique=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'

    def __str__(self):
        return self.nome

    
class Pesquisa(models.Model):
    titulo = models.CharField('Título', max_length=100)
    descricao = models.TextField('Descrição', max_length=2000)
    pesquisadores = models.ManyToManyField('core.Pesquisador', verbose_name='Pesquisadores')
    TITULOS = [
        ('Doutorado', 'Doutorado'),
        ('Mestrado', 'Mestrado'),
        ('Graduação', 'Graduação'),
        ('Pós-Doutorado', 'Pós-Doutorado'),
    ]
    nivel = models.CharField('Nível', max_length=100, choices=TITULOS)
    STATUS = [
        ('Em andamento', 'Em andamento'),
        ('Concluída', 'Concluída'),
        ('Interrompida', 'Interrompida'),
    ]
    status = models.CharField('Status', max_length=100, choices=STATUS)
    class Meta:
        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'

    def __str__(self):
        return self.titulo

