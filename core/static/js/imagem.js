
    function abrirImagem(url) {
        const modal = document.getElementById('modalImagem');
        const imagem = document.getElementById('imagemAmpliada');

        imagem.src = url;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    function fecharImagem() {
        const modal = document.getElementById('modalImagem');
        const imagem = document.getElementById('imagemAmpliada');

        modal.classList.add('hidden');
        modal.classList.remove('flex');
        imagem.src = '';
    }
