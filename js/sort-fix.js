/**
 * Script para corrigir as opções de ordenação no F1 Drivers Album
 */
document.addEventListener('DOMContentLoaded', function() {
    // Referências aos elementos
    const filterSelect = document.getElementById('filter-select');
    const sortOrderBtn = document.getElementById('sort-order-btn');
    
    // Verificar se os elementos existem
    if (!filterSelect || !sortOrderBtn) {
        console.error('Elementos de filtro não encontrados');
        return;
    }
    
    // Adicionar evento de mudança específico
    filterSelect.addEventListener('change', function() {
        const selectedFilter = filterSelect.value;
        console.log('Filtro selecionado:', selectedFilter);
        
        // Aplicar ordenação diretamente
        sortDrivers(selectedFilter, getSortDirection());
    });
    
    // Adicionar evento ao botão de ordem
    sortOrderBtn.addEventListener('click', function() {
        // Inverter a direção atual
        const currentDirection = getSortDirection();
        const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
        
        // Atualizar ícone
        sortOrderBtn.innerHTML = newDirection === 'asc' ? 
            '<i class="fas fa-sort-up"></i>' : 
            '<i class="fas fa-sort-down"></i>';
        
        // Aplicar ordenação com a nova direção
        sortDrivers(filterSelect.value, newDirection);
    });
    
    // Função para obter a direção atual de ordenação
    function getSortDirection() {
        const icon = sortOrderBtn.querySelector('i');
        return icon && icon.classList.contains('fa-sort-up') ? 'asc' : 'desc';
    }
    
    // Função principal de ordenação
    function sortDrivers(filter, direction) {
        // Obter todos os cards de pilotos
        const driversGrid = document.getElementById('drivers-grid');
        if (!driversGrid) return;
        
        const cards = Array.from(driversGrid.querySelectorAll('.driver-card'));
        if (!cards.length) return;
        
        // Ordenar cards
        cards.sort((cardA, cardB) => {
            let valA, valB;
            
            // Extrair valores com base no filtro
            switch (filter) {
                case 'name':
                    valA = cardA.querySelector('.driver-name').textContent.toLowerCase();
                    valB = cardB.querySelector('.driver-name').textContent.toLowerCase();
                    break;
                    
                case 'country':
                    valA = (cardA.querySelector('.driver-country').textContent || '').toLowerCase();
                    valB = (cardB.querySelector('.driver-country').textContent || '').toLowerCase();
                    break;
                    
                case 'wins':
                    valA = getNumericValue(cardA.querySelector('.wins-value'));
                    valB = getNumericValue(cardB.querySelector('.wins-value'));
                    break;
                    
                case 'championships':
                    valA = getNumericValue(cardA.querySelector('.championships-value'));
                    valB = getNumericValue(cardB.querySelector('.championships-value'));
                    break;
                    
                case 'age':
                    // Obter data de nascimento e converter para timestamp
                    const birthA = getBirthDate(cardA);
                    const birthB = getBirthDate(cardB);
                    return direction === 'asc' ? birthA - birthB : birthB - birthA;
                    
                case 'seasons':
                    valA = getSeasonsCount(cardA);
                    valB = getSeasonsCount(cardB);
                    break;
                    
                case 'raceStarts':
                    valA = getNumericValue(cardA.querySelector('.race-starts-value'));
                    valB = getNumericValue(cardB.querySelector('.race-starts-value'));
                    break;
                    
                case 'raceEntries':
                    valA = getNumericValue(cardA.querySelector('.race-entries-value'));
                    valB = getNumericValue(cardB.querySelector('.race-entries-value'));
                    break;
                    
                case 'polePositions':
                    valA = getNumericValue(cardA.querySelector('.pole-positions-value'));
                    valB = getNumericValue(cardB.querySelector('.pole-positions-value'));
                    break;
                    
                case 'podiums':
                    valA = getNumericValue(cardA.querySelector('.podiums-value'));
                    valB = getNumericValue(cardB.querySelector('.podiums-value'));
                    break;
                    
                case 'fastestLaps':
                    valA = getNumericValue(cardA.querySelector('.fastest-laps-value'));
                    valB = getNumericValue(cardB.querySelector('.fastest-laps-value'));
                    break;
                    
                default:
                    valA = cardA.querySelector('.driver-name').textContent.toLowerCase();
                    valB = cardB.querySelector('.driver-name').textContent.toLowerCase();
            }
            
            // Comparar valores
            if (typeof valA === 'number' && typeof valB === 'number') {
                return direction === 'asc' ? valA - valB : valB - valA;
            } else {
                // Comparação de strings
                if (valA < valB) return direction === 'asc' ? -1 : 1;
                if (valA > valB) return direction === 'asc' ? 1 : -1;
                return 0;
            }
        });
        
        // Reordenar os cards no DOM
        cards.forEach(card => driversGrid.appendChild(card));
        
        console.log(`Ordenação aplicada: ${filter} (${direction})`);
    }
    
    // Função auxiliar para obter valor numérico de um elemento
    function getNumericValue(element) {
        if (!element) return 0;
        
        const text = element.textContent.trim();
        const match = text.match(/\d+/);
        return match ? parseInt(match[0], 10) : 0;
    }
    
    // Função para obter data de nascimento a partir do card
    function getBirthDate(card) {
        const birthElement = card.querySelector('.driver-birth-date');
        if (!birthElement) return 0;
        
        // Extrair data no formato DD/MM/YYYY
        const dateText = birthElement.textContent.trim();
        const match = dateText.match(/(\d{2})\/(\d{2})\/(\d{4})/);
        
        if (match) {
            // Converter para formato YYYY-MM-DD para ordenação correta
            return new Date(`${match[3]}-${match[2]}-${match[1]}`).getTime();
        }
        
        return 0;
    }
    
    // Função para contar quantas temporadas o piloto participou
    function getSeasonsCount(card) {
        const seasonsElement = card.querySelector('.seasons-stat .value');
        if (!seasonsElement) return 0;
        
        const seasonsText = seasonsElement.textContent.trim();
        // Contar anos separados por vírgula e intervalos (1951, 1953-1955 conta como 4 temporadas)
        let count = 0;
        
        // Separar por vírgula
        const parts = seasonsText.split(',');
        
        parts.forEach(part => {
            part = part.trim();
            if (part.includes('-')) {
                // É um intervalo, contar os anos
                const range = part.split('-');
                if (range.length === 2) {
                    const start = parseInt(range[0], 10);
                    const end = parseInt(range[1], 10);
                    if (!isNaN(start) && !isNaN(end)) {
                        count += (end - start + 1);
                    } else {
                        // Se não conseguir converter, considerar como 1
                        count += 1;
                    }
                }
            } else {
                // É um ano individual
                count += 1;
            }
        });
        
        return count;
    }
    
    // Aplicar ordenação inicial
    setTimeout(() => {
        console.log('Iniciando ordenação inicial');
        sortDrivers(filterSelect.value, getSortDirection());
    }, 1000);
});
