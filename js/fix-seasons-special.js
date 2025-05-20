/**
 * Ajuste para casos especiais de pilotos com muitas temporadas
 * Solução: APENAS diminui o tamanho dos anos, sem tocar na palavra Seasons
 */
document.addEventListener('DOMContentLoaded', function() {
    // Lista de pilotos com muitas temporadas que precisam de ajuste
    const specialDrivers = [
        "André Pilette",
        "Bob Gerard",
        "Louis Chiron",
        "Pedro de la Rosa"
    ];

    // Função única para diminuir APENAS o tamanho dos anos
    function adjustYearsSize() {
        // Para cada piloto especial
        specialDrivers.forEach(driverName => {
            // Encontrar todos os cards do piloto
            document.querySelectorAll('.driver-card').forEach(card => {
                const nameEl = card.querySelector('.driver-name');
                if (!nameEl || nameEl.textContent.trim() !== driverName) return;
                
                // Pegar APENAS o elemento dos anos (value), NÃO a palavra "Seasons"
                const yearsElement = card.querySelector('.seasons-stat .value');
                if (!yearsElement) return;
                
                // APENAS diminuir o tamanho da fonte dos anos
                yearsElement.style.fontSize = '0.7rem';
                
                // Marcar como ajustado para evitar reprocessamento
                card.setAttribute('data-years-adjusted', 'true');
            });
        });
    }

    // Aplicar em todos os momentos importantes
    function applyFixes() {
        setTimeout(adjustYearsSize, 0);
    }

    // Inicialização e recarga
    window.addEventListener('load', applyFixes);
    
    // Observador de mudanças na DOM
    const observer = new MutationObserver(() => applyFixes());
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Eventos de navegação e busca
    document.addEventListener('click', e => {
        if (e.target.closest('.page-btn') || e.target.closest('#search-btn')) {
            setTimeout(applyFixes, 100);
            setTimeout(applyFixes, 300);
        }
    });
    
    // Eventos de busca
    document.querySelector('#search-input')?.addEventListener('input', () => {
        setTimeout(applyFixes, 100);
        setTimeout(applyFixes, 300);
    });
    
    // Aplicar imediatamente e com atraso para garantir
    applyFixes();
    setTimeout(applyFixes, 200);
    setTimeout(applyFixes, 500);
});


