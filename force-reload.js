// Script para forçar o recarregamento da página ignorando o cache
(function() {
    // Adicionar parâmetro de versão único para forçar atualização
    const url = new URL(window.location.href);
    
    // Se já tiver um parâmetro de versão, atualiza-o
    if (url.searchParams.has('v')) {
        url.searchParams.set('v', new Date().getTime());
    } else {
        url.searchParams.append('v', new Date().getTime());
    }
    
    // Se for uma recarregamento forçado, não faz nada para evitar loop
    if (!window.performance || window.performance.navigation.type !== window.performance.navigation.TYPE_RELOAD) {
        window.location.href = url.toString();
    }
    
    // Forçar recarregamento de CSS
    const links = document.getElementsByTagName('link');
    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        if (link.rel === 'stylesheet') {
            const href = link.href.split('?')[0];
            link.href = href + '?v=' + new Date().getTime();
        }
    }
})();
