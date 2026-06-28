from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from .models import Animal, Fenomeno, GrupoTaxonomico, ImagemAnimal, Local


class FaunaSearchTests(TestCase):
    def setUp(self):
        self.animal = Animal.objects.create(
            nome_comum='Café do Mato',
            nome_cientifico='Felis catus',
        )
        self.local = Local.objects.create(nome='Mata', latitude=-3.0, longitude=-60.0)
        self.grupo = GrupoTaxonomico.objects.create(nome='Mamíferos')
        self.fenomeno = Fenomeno.objects.create(nome='Fotografia', descricao='Descrição')
        self.imagem = self._create_imagem_animal()

    def _create_imagem_animal(self):
        image = Image.new('RGB', (1, 1), 'white')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        foto = SimpleUploadedFile(
            'teste.jpg',
            buffer.getvalue(),
            content_type='image/jpeg',
        )
        return ImagemAnimal.objects.create(
            animal=self.animal,
            grupo=self.grupo,
            fenomeno=self.fenomeno,
            local=self.local,
            foto=foto,
        )

    def test_search_without_accents_matches_accented_name(self):
        response = self.client.get('/fauna/', {'search': 'cafe'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.imagem, response.context['page_obj'].object_list)
