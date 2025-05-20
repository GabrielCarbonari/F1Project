/**
 * Script para forçar o recarregamento dos dados de pilotos sem usar cache
 */

document.addEventListener('DOMContentLoaded', () => {
    // Adicionar botão de recarregamento
    const controlPanel = document.querySelector('.control-panel') || document.body;
    
    const reloadButton = document.createElement('button');
    reloadButton.id = 'reload-data-btn';
    reloadButton.className = 'btn btn-warning';
    reloadButton.innerHTML = '<i class="fas fa-sync-alt"></i> Recarregar Dados';
    reloadButton.style.marginLeft = '10px';
    
    // Inserir botão na interface
    controlPanel.appendChild(reloadButton);
    
    // Adicionar evento de clique
    reloadButton.addEventListener('click', forceReloadData);
});

/**
 * Força o recarregamento dos dados sem usar cache
 */
async function forceReloadData() {
    try {
        // Mostrar overlay de carregamento
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
        
        console.log('Forçando recarregamento dos dados de pilotos...');
        
        // Adicionar timestamp à URL para forçar o bypass do cache
        const timestamp = new Date().getTime();
        const url = `./data/drivers.json?v=${timestamp}`;
        console.log(`Carregando dados de: ${url}`);
        
        // Usar cabeçalhos para evitar cache
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            cache: 'no-store'
        });
        
        // Limpar o localStorage também
        localStorage.removeItem('f1DriversData');
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Verificar se temos um array de pilotos
        if (Array.isArray(data)) {
            // Substituir os dados globais
            window.allDrivers = data;
            
            // Redesenhar a interface
            if (typeof renderDrivers === 'function') {
                renderDrivers();
            }
            
            console.log(`Dados recarregados com sucesso! ${data.length} pilotos carregados.`);
            
            // Verificar Jonathan Williams
            const jonathan = data.find(d => d.Name === 'Jonathan Williams');
            if (jonathan) {
                console.log('Dados de Jonathan Williams:', jonathan);
            }
            
            // Exibir mensagem de sucesso
            alert(`Dados recarregados com sucesso!\nPilotos carregados: ${data.length}`);
        } else {
            throw new Error('Formato de dados inválido');
        }
    } catch (error) {
        console.error('Erro ao recarregar dados:', error);
        alert(`Erro ao recarregar dados: ${error.message}`);
    } finally {
        // Ocultar overlay de carregamento
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }
}
