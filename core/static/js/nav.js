document.addEventListener('DOMContentLoaded', function () {
    const paginaAtual = window.location.pathname.replace(/\/$/, '') || '/';
    const links = document.querySelectorAll('#nav-principal .link-nav');

    links.forEach(function (link) {
        const linkUrl = new URL(link.getAttribute('href'), window.location.origin)
            .pathname
            .replace(/\/$/, '') || '/';

        if (linkUrl === paginaAtual) {
            link.classList.add('ativo');
            link.setAttribute('aria-current', 'page');
        }
    });
});
