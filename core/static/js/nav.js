document.addEventListener('DOMContentLoaded', function () {
    const paginaAtual = window.location.pathname.replace(/\/$/, '') || '/';
    const linksDesktop = document.querySelectorAll('#nav-principal .link-nav');

    linksDesktop.forEach(function (link) {
        const linkUrl = new URL(link.getAttribute('href'), window.location.origin)
            .pathname
            .replace(/\/$/, '') || '/';

        if (linkUrl === paginaAtual) {
            link.classList.add('ativo');
            link.setAttribute('aria-current', 'page');
        }
    });

    const buttonOpen = document.getElementById('mobile-menu-open');
    const buttonClose = document.getElementById('mobile-menu-close');
    const overlay = document.getElementById('mobile-menu-overlay');
    const menu = document.getElementById('mobile-menu');

    if (!buttonOpen || !menu) return;

    const abrirMenu = () => {
        menu.classList.remove('translate-x-full');
        menu.classList.add('translate-x-0');
        overlay.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    };

    const fecharMenu = () => {
        menu.classList.add('translate-x-full');
        menu.classList.remove('translate-x-0');
        overlay.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    };

    buttonOpen.addEventListener('click', abrirMenu);
    if (buttonClose) buttonClose.addEventListener('click', fecharMenu);
    if (overlay) overlay.addEventListener('click', fecharMenu);

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') fecharMenu();
    });

    document.querySelectorAll('#mobile-menu a').forEach(function (link) {
        link.addEventListener('click', fecharMenu);
    });
});
