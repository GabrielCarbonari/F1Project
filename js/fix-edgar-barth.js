/**
 * Script para corrigir o texto do país do Edgar Barth
 */
document.addEventListener('DOMContentLoaded', function() {
    // Função para corrigir o país do Edgar Barth
    function fixEdgarBarthCountry() {
        // Encontrar todos os cards do Edgar Barth
        document.querySelectorAll('.driver-card').forEach(function(card) {
            const nameEl = card.querySelector('.driver-name');
            if (!nameEl || nameEl.textContent.trim() !== 'Edgar Barth') return;
            
            // Marcar o card para identificação
            card.setAttribute('data-driver-name', 'Edgar Barth');
            
            // Encontrar o elemento do país
            const countryEl = card.querySelector('.driver-country');
            if (!countryEl) return;
            
            // Solução radical: substituir completamente o elemento
            const newCountryEl = document.createElement('div');
            newCountryEl.className = countryEl.className;
            newCountryEl.textContent = 'Germany';
            
            // Copiar a bandeira (primeiro filho, se existir)
            const flag = countryEl.querySelector('img');
            if (flag) {
                newCountryEl.appendChild(flag.cloneNode(true));
            }
            
            // Substituir o elemento antigo pelo novo
            countryEl.parentNode.replaceChild(newCountryEl, countryEl);
            console.log('Elemento de país do Edgar Barth substituído completamente');
        });
    }
    
    // Aplicar a correção em vários momentos
    window.addEventListener('load', fixEdgarBarthCountry);
    
    // Observer para detectar mudanças na DOM
    const observer = new MutationObserver(function() {
        setTimeout(fixEdgarBarthCountry, 100);
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Aplicar quando mudar de página ou após busca
    document.addEventListener('click', function(e) {
        if (e.target.closest('.page-btn') || e.target.closest('#search-btn')) {
            setTimeout(fixEdgarBarthCountry, 300);
        }
    });
    
    // Aplicar imediatamente e com atraso
    fixEdgarBarthCountry();
    setTimeout(fixEdgarBarthCountry, 500);
});
