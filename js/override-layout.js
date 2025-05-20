/**
 * Script para forçar o layout de 5 cards por linha
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Aplicando layout forçado de 5 cards por linha...');
    
    // Função para aplicar o layout
    function applyLayout() {
        // Aumentar o container principal
        const mainContainer = document.querySelector('main');
        if (mainContainer) {
            mainContainer.style.maxWidth = '1500px';
        }
        
        // Configurar o grid para 5 colunas
        const driversContainer = document.querySelector('.drivers-container');
        if (driversContainer) {
            driversContainer.style.gridTemplateColumns = 'repeat(5, 1fr)';
            driversContainer.style.gap = '1.5rem'; // Manter o espaçamento original
            console.log('Layout de 5 cards por linha aplicado com sucesso!');
        }
    }
    
    // Aplicar imediatamente
    applyLayout();
    
    // Aplicar novamente após um pequeno delay para garantir
    setTimeout(applyLayout, 500);
    
    // Observar mudanças no DOM que possam afetar o container
    const observer = new MutationObserver(() => {
        applyLayout();
    });
    
    // Observar o container de drivers ou seu pai
    const containerOrParent = document.querySelector('.drivers-container') || document.querySelector('main');
    if (containerOrParent) {
        observer.observe(containerOrParent, {
            childList: true,
            subtree: true
        });
    }
});
