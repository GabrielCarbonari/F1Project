/**
 * Script para corrigir problemas de exibição nos cards de pilotos
 * Este script força a limpeza de cache e corrige valores problemáticos
 */

// Função para limpar valores estatísticos com problemas
function fixDisplayIssues() {
    console.log("Aplicando correções de exibição...");
    
    // Verificar se já carregou os drivers
    if (!window.allDrivers || !Array.isArray(window.allDrivers)) {
        console.warn("Drivers não carregados ainda, aguardando...");
        return;
    }
    
    // Corrigir valores problemáticos diretamente no array
    window.allDrivers.forEach(driver => {
        // Corrigir problemas com nacionalidade
        if (driver.Nationality && driver.Nationality.includes('[')) {
            driver.Nationality = driver.Nationality.replace(/\s*\[\d+\]\s*/g, '');
            console.log(`Corrigido nacionalidade para ${driver.Name}: ${driver.Nationality}`);
        }
        
        // Corrigir problemas com "..." ou valores truncados
        ['Pole positions', 'Wins', 'Podiums', 'Championships', 'Race entries', 'Race starts', 'Fastest laps'].forEach(stat => {
            if (driver[stat] && (String(driver[stat]).includes('...') || String(driver[stat]).endsWith('..'))) {
                const oldValue = driver[stat];
                driver[stat] = cleanStatValue(driver[stat]);
                console.log(`Corrigido ${stat} para ${driver.Name}: ${oldValue} → ${driver[stat]}`);
            }
        });
    });
    
    console.log("Correções aplicadas, atualizando exibição...");
    // Forçar renderização
    if (typeof renderDrivers === 'function') {
        renderDrivers();
    }
}

// Executar após um breve atraso para garantir que tudo carregou
document.addEventListener('DOMContentLoaded', () => {
    // Tentar uma vez logo após o carregamento
    setTimeout(fixDisplayIssues, 1000);
    
    // E tentar novamente após mais alguns segundos
    setTimeout(fixDisplayIssues, 3000);
});

// Limpar o cache para garantir dados frescos
console.log("Limpando cache do navegador para dados de pilotos...");

// Tentar invalidar cache para o arquivo JSON 
const urls = [
    './data/drivers.json',
    'data/drivers.json',
    window.location.href + 'data/drivers.json'
];

// Forçar recarga com timestamp para ignorar cache
urls.forEach(url => {
    fetch(url + '?t=' + Date.now(), { 
        cache: 'no-store',
        headers: {
            'Cache-Control': 'no-cache'
        }
    })
    .then(resp => resp.json())
    .then(data => {
        console.log(`Recarregados ${data.length} pilotos do ${url}`);
        // Atualizar dados
        if (window.allDrivers && data.length > 0) {
            window.allDrivers = data;
            if (typeof renderDrivers === 'function') {
                renderDrivers();
            }
        }
    })
    .catch(err => console.warn("Erro ao recarregar: ", err));
});
