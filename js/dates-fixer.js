// Script para garantir que as datas apareçam corretamente
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, aguardando renderização dos cards...');
    
    // Aguardar 1 segundo para garantir que todos os cards foram renderizados
    setTimeout(function() {
        console.log('Iniciando o processamento das datas...');
        
        // Carregar o arquivo JSON diretamente - com timestamp para evitar cache
        fetch('data/drivers_clean.json?v=' + new Date().getTime())
            .then(response => response.json())
            .then(drivers => {
                console.log('Dados carregados com sucesso:', drivers.length);
                console.log('Primeiro piloto:', drivers[0]);
                
                // Para cada card de piloto na página
                const cards = document.querySelectorAll('.driver-card');
                console.log('Cards encontrados:', cards.length);
                
                cards.forEach(card => {
                    // Obter o nome do piloto do card
                    const nameElement = card.querySelector('.driver-name');
                    if (!nameElement) {
                        console.log('Elemento de nome não encontrado');
                        return;
                    }
                    
                    const cardName = nameElement.textContent;
                    console.log('Processando piloto:', cardName);
                    
                    // Encontrar o piloto correspondente no JSON
                    const driver = drivers.find(d => d.Name === cardName);
                    
                    if (driver) {
                        console.log('Dados encontrados para:', cardName, driver);
                        
                        // Acessar diretamente os elementos
                        const birthText = card.querySelector('.birth-date-text');
                        const deathText = card.querySelector('.death-date-text');
                        const birthItem = card.querySelector('.birth-item');
                        const deathItem = card.querySelector('.death-item');
                        
                        // Verificar elementos
                        if (!birthText || !deathText || !birthItem || !deathItem) {
                            console.log('Elementos de data não encontrados para', cardName);
                            return;
                        }
                        
                        // Limpar e forçar estilo inline
                        birthItem.setAttribute('style', 'display: none;');
                        deathItem.setAttribute('style', 'display: none;');
                        
                        // Verificar e definir data de nascimento
                        if (driver.BirthDate && driver.BirthDate.length > 4 && !driver.BirthDate.includes('and')) {
                            birthText.textContent = driver.BirthDate;
                            birthItem.setAttribute('style', 'display: inline-flex !important;');
                            console.log(`${cardName}: Nascimento ${driver.BirthDate}`);
                        }
                        
                        // Verificar e definir data de morte
                        if (driver.DeathDate && driver.DeathDate.length > 4) {
                            deathText.textContent = driver.DeathDate;
                            deathItem.setAttribute('style', 'display: inline-flex !important;');
                            console.log(`${cardName}: Falecimento ${driver.DeathDate}`);
                        }
                        
                        // Garantir que a linha de datas esteja visível
                        const datesRow = card.querySelector('.dates-row');
                        if (datesRow) {
                            datesRow.style.display = 'flex';
                        }
                    }
                });
            })
            .catch(error => console.error('Erro ao carregar dados:', error));
    }, 1000);
});
