// Script para carregar imagens dos pilotos
console.log('Carregando sistema de imagens de pilotos...');

document.addEventListener('DOMContentLoaded', () => {
    // Esperar um pouco para garantir que todos os cards foram criados
    setTimeout(loadDriverImages, 500);
});

// Função para remover acentos e caracteres especiais
function normalizeString(str) {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
              .replace(/[^\w\s]/gi, '')
              .replace(/\s+/g, ' ')
              .trim();
}

// Função principal para carregar imagens dos pilotos
function loadDriverImages() {
    console.log('Iniciando carregamento de imagens dos pilotos');
    
    // Selecionar todos os cards de pilotos
    const driverCards = document.querySelectorAll('.driver-card');
    let loadedCount = 0;
    let totalCount = driverCards.length;
    
    driverCards.forEach(card => {
        // Obter o nome do piloto e a div da imagem
        const driverName = card.querySelector('.driver-name').textContent;
        const imgElement = card.querySelector('.driver-image img');
        
        if (!driverName || !imgElement) return;
        
        // Tentar carregar a imagem do piloto
        loadDriverImage(driverName, imgElement, () => {
            loadedCount++;
            if (loadedCount % 20 === 0 || loadedCount === totalCount) {
                console.log(`Carregadas ${loadedCount}/${totalCount} imagens de pilotos`);
            }
        });
    });
}

// Função para tentar carregar a imagem de um piloto específico
function loadDriverImage(driverName, imgElement, callback) {
    // Array de extensões para tentar
    const extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
    
    // Nome normalizado (sem acentos)
    const normalizedName = normalizeString(driverName);
    
    // Variações de nome para tentar (original e normalizado)
    const nameVariations = [driverName, normalizedName];
    
    // Placeholder usado enquanto carrega a imagem real
    imgElement.src = 'images/driver-placeholder.png';
    imgElement.alt = driverName;
    
    // Função para tentar a próxima variação do nome ou extensão
    function tryNextVariation(nameIndex, extIndex) {
        if (nameIndex >= nameVariations.length) {
            // Tentamos todas as variações e extensões, usar placeholder padrão
            // Placeholder já foi definido, apenas chamamos o callback
            callback();
            return;
        }
        
        if (extIndex >= extensions.length) {
            // Tentamos todas as extensões para esta variação, passar para a próxima
            tryNextVariation(nameIndex + 1, 0);
            return;
        }
        
        const currentName = nameVariations[nameIndex];
        const currentExt = extensions[extIndex];
        const imagePath = `images/Pilotos/${currentName}.${currentExt}`;
        
        // Criar um objeto Image para verificar se a imagem existe
        const testImage = new Image();
        testImage.onload = function() {
            // A imagem existe e foi carregada, usar este caminho
            imgElement.src = imagePath;
            imgElement.classList.add('loaded');
            
            // Adicionar classe para ajustar estilos do card quando tem imagem
            imgElement.closest('.driver-card').classList.add('has-driver-image');
            
            callback();
        };
        
        testImage.onerror = function() {
            // Esta variação/extensão não existe, tentar a próxima
            tryNextVariation(nameIndex, extIndex + 1);
        };
        
        // Iniciar carregamento da imagem (com timestamp para evitar cache)
        testImage.src = imagePath + '?v=' + Date.now();
    }
    
    // Iniciar tentativas com a primeira variação e extensão
    tryNextVariation(0, 0);
}

// Definir um observador para novos cards que possam ser adicionados dinamicamente
function setupDynamicImageLoader() {
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1 && node.classList.contains('driver-card')) {
                        const driverName = node.querySelector('.driver-name').textContent;
                        const imgElement = node.querySelector('.driver-image img');
                        
                        if (driverName && imgElement) {
                            loadDriverImage(driverName, imgElement, () => {});
                        }
                    }
                });
            }
        });
    });
    
    // Observar o container dos cards
    const driversGrid = document.getElementById('drivers-grid');
    if (driversGrid) {
        observer.observe(driversGrid, { childList: true, subtree: true });
    }
}

// Configurar o observador após o carregamento das imagens iniciais
setTimeout(setupDynamicImageLoader, 1000);
