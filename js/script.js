console.log('Iniciando carregamento de F1 Drivers Album');

// Variáveis globais para paginação e filtros
let allDrivers = [];
let currentPage = 1;
let driversPerPage = 20;
let currentFilter = 'name';
let isAscending = true;
let searchTerm = '';

// DOM Elements
const driversGrid = document.getElementById('drivers-grid');
const filterSelect = document.getElementById('filter-select');
const sortOrderBtn = document.getElementById('sort-order-btn');
const prevPageBtn = document.getElementById('prev-page');
const nextPageBtn = document.getElementById('next-page');
const pageInfo = document.getElementById('page-info');
const pageInput = document.getElementById('page-input');
const goToPageBtn = document.getElementById('go-to-page-btn');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const loadingOverlay = document.getElementById('loading-overlay');

// Inicializar a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Carregar dados
        allDrivers = await safeLoadJSON('./data/drivers.json');
        console.log(`Carregados ${allDrivers.length} pilotos`);
        
        // Verificar e limpar datas inválidas e dados problemáticos
        const invalidDates = allDrivers.filter(driver => {
            const birthDate = driver.BirthDate ? new Date(driver.BirthDate) : null;
            return !birthDate || isNaN(birthDate) || birthDate > new Date();
        });
        console.log(`Pilotos com data inválida: ${invalidDates.length}`);
        
        // Limpar quaisquer dados problemáticos em Nationality
        allDrivers.forEach(driver => {
            // Corrigir problemas como "Argentina [50]" para "Argentina"
            if (driver.Nationality && driver.Nationality.includes('[')) {
                driver.Nationality = driver.Nationality.replace(/\s*\[\d+\]\s*/, '');
            }
        });
        
        // Configurar event listeners
        setupEventListeners();
        
        // Renderizar pilotos
        renderDrivers();
        
        // Ocultar tela de carregamento
        if (loadingOverlay) loadingOverlay.style.display = 'none';
        
    } catch (error) {
        console.error('Erro ao carregar aplicação:', error);
        showCriticalError('Falha ao carregar dados dos pilotos');
    }
});

// Configurar event listeners
function setupEventListeners() {
    if (filterSelect) {
        filterSelect.addEventListener('change', handleFilterChange);
    }
    
    if (sortOrderBtn) {
        sortOrderBtn.addEventListener('click', toggleSortOrder);
    }
    
    if (prevPageBtn) {
        prevPageBtn.addEventListener('click', goToPrevPage);
    }
    
    if (nextPageBtn) {
        nextPageBtn.addEventListener('click', goToNextPage);
    }
    
    if (searchBtn) {
        searchBtn.addEventListener('click', handleSearch);
    }
    
    if (searchInput) {
        searchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                handleSearch();
            }
        });
    }
    
    if (goToPageBtn) {
        goToPageBtn.addEventListener('click', goToSpecificPage);
    }
    
    if (pageInput) {
        pageInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                goToSpecificPage();
            }
        });
    }
}

// Carregar JSON de forma segura
async function safeLoadJSON(url) {
    try {
        // Adicionar timestamp para evitar cache
        const timestamp = new Date().getTime();
        const urlWithTimestamp = `${url}?v=${timestamp}`;
        console.log(`Carregando dados de: ${urlWithTimestamp}`);
        
        const response = await fetch(urlWithTimestamp, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            cache: 'no-store'
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Garantir que temos um array de pilotos
        if (Array.isArray(data)) {
            return data;
        } else if (typeof data === 'object') {
            // Se for um objeto, converter para array
            return Object.values(data);
        } else {
            throw new Error('Formato de dados inválido');
        }
    } catch (error) {
        console.error('Erro ao carregar JSON:', error);
        throw error;
    }
}

// Lidar com mudança de filtro
function handleFilterChange() {
    currentFilter = filterSelect.value;
    currentPage = 1;
    renderDrivers();
}

// Alternar ordem de classificação
function toggleSortOrder() {
    isAscending = !isAscending;
    sortOrderBtn.innerHTML = isAscending ? '<i class="fas fa-sort-up"></i>' : '<i class="fas fa-sort-down"></i>';
    renderDrivers();
}

// Ir para página anterior
function goToPrevPage() {
    if (currentPage > 1) {
        currentPage--;
        animatePageTransition(() => {
            renderDrivers();
        });
    }
}

// Ir para próxima página
function goToNextPage() {
    const totalPages = Math.ceil(filterAndSortDrivers().length / driversPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        animatePageTransition(() => {
            renderDrivers();
        });
    }
}

// Animação de transição entre páginas
function animatePageTransition(callback) {
    if (!driversGrid) return callback();
    
    driversGrid.classList.add('page-transition-out');
    
    setTimeout(() => {
        callback();
        
        setTimeout(() => {
            driversGrid.classList.remove('page-transition-out');
            driversGrid.classList.add('page-transition-in');
            
            setTimeout(() => {
                driversGrid.classList.remove('page-transition-in');
            }, 300);
        }, 50);
    }, 300);
}

// Atualizar informações de página
function updatePageInfo() {
    const totalPages = Math.ceil(filterAndSortDrivers().length / driversPerPage);
    
    if (pageInfo) {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }
    
    if (prevPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
    }
    
    if (nextPageBtn) {
        nextPageBtn.disabled = currentPage === totalPages;
    }
    
    if (pageInput) {
        pageInput.max = totalPages;
        pageInput.value = currentPage;
    }
}

// Lidar com busca
function handleSearch() {
    if (!searchInput) return;
    
    searchTerm = searchInput.value.toLowerCase().trim();
    currentPage = 1;
    renderDrivers();
}

// Ir para página específica
function goToSpecificPage() {
    if (!pageInput) return;
    
    const page = parseInt(pageInput.value);
    const totalPages = Math.ceil(filterAndSortDrivers().length / driversPerPage);
    
    if (page >= 1 && page <= totalPages && page !== currentPage) {
        currentPage = page;
        animatePageTransition(() => {
            renderDrivers();
        });
    } else {
        // Restaurar valor anterior
        pageInput.value = currentPage;
    }
}

// Normalizar nome de países
function normalizeCountryName(countryName) {
    if (!countryName) return '';
    
    // Corrigir países específicos conforme solicitado
    if (countryName.includes('West Germany') || countryName.includes('East Germany')) {
        return countryName.replace(/(?:West|East)\s+Germany/g, 'Germany');
    }
    
    if (countryName.includes('Rhodesia')) {
        return countryName.replace(/Rhodesia/g, 'Zimbabwe');
    }
    
    return countryName;
}

// Função para analisar e converter campos numéricos corretamente
function parseNumericField(value) {
    if (value === undefined || value === null) return 0;
    
    // Se for uma string, limpar e converter
    if (typeof value === 'string') {
        // Remover qualquer texto não numérico no início (manter apenas dígitos e pontos)
        const cleanValue = value.trim().replace(/^[^0-9]*/, '');
        // Pegar apenas os números iniciais (antes de qualquer texto ou símbolos especiais)
        const numMatch = cleanValue.match(/^\d+/);
        if (numMatch) {
            return parseInt(numMatch[0], 10);
        }
        return 0;
    }
    
    // Se já for um número, retornar como está
    if (typeof value === 'number') {
        return value;
    }
    
    return 0;
}

// Função para formatar datas em um formato que o JavaScript possa entender corretamente
function formatDate(dateString) {
    if (!dateString) return null;
    
    // Verificar se é no formato DD/MM/YYYY (comum em dados europeus)
    if (dateString.includes('/')) {
        const parts = dateString.split('/');
        if (parts.length === 3) {
            // Converter para formato YYYY-MM-DD que o JavaScript entende bem
            return `${parts[2]}-${parts[1]}-${parts[0]}`;
        }
    }
    
    // Se não estiver em um formato reconhecido, retornar como está
    return dateString;
}

// Filtrar e ordenar pilotos
function filterAndSortDrivers() {
    // Normalizar países nos dados antes de filtrar/ordenar
    allDrivers.forEach(driver => {
        if (driver.Nationality) {
            driver.Nationality = normalizeCountryName(driver.Nationality);
        }
    });
    
    // Filtrar por termo de busca
    let filteredDrivers = allDrivers;
    
    if (searchTerm) {
        filteredDrivers = allDrivers.filter(driver => {
            const name = (driver.name || driver.Name || '').toLowerCase();
            const nationality = (driver.Nationality || '').toLowerCase();
            
            return name.includes(searchTerm) || nationality.includes(searchTerm);
        });
    }
    
    // Ordenar por filtro atual
    filteredDrivers.sort((a, b) => {
        let valA, valB;
        
        switch (currentFilter) {
            case 'name':
                valA = (a.name || a.Name || '').toLowerCase();
                valB = (b.name || b.Name || '').toLowerCase();
                break;
            case 'country':
                valA = (a.Nationality || '').toLowerCase();
                valB = (b.Nationality || '').toLowerCase();
                break;
            case 'wins':
                // Garantir que dados numéricos sejam convertidos corretamente
                valA = parseNumericField(a.Wins);
                valB = parseNumericField(b.Wins);
                break;
            case 'championships':
                valA = parseNumericField(a.Championships);
                valB = parseNumericField(b.Championships);
                break;
            case 'age':
                // Ordenar pela data de nascimento, da mais antiga para mais nova
                const birthDateA = a.BirthDate ? new Date(formatDate(a.BirthDate)) : new Date(0);
                const birthDateB = b.BirthDate ? new Date(formatDate(b.BirthDate)) : new Date(0);
                // Retornar diretamente para evitar o código de comparação padrão abaixo
                return isAscending ? birthDateA - birthDateB : birthDateB - birthDateA;
            case 'seasons':
                // Contar quantos anos o piloto competiu (número de temporadas)
                const seasonsA = a.Seasons ? String(a.Seasons).split(/[,\-]/).filter(Boolean).length : 0;
                const seasonsB = b.Seasons ? String(b.Seasons).split(/[,\-]/).filter(Boolean).length : 0;
                valA = seasonsA;
                valB = seasonsB;
                break;
            case 'raceStarts':
                valA = parseNumericField(a['Race starts']);
                valB = parseNumericField(b['Race starts']);
                break;
            case 'raceEntries':
                valA = parseNumericField(a['Race entries']);
                valB = parseNumericField(b['Race entries']);
                break;
            case 'polePositions':
                valA = parseNumericField(a['Pole positions']);
                valB = parseNumericField(b['Pole positions']);
                break;
            case 'podiums':
                valA = parseNumericField(a.Podiums);
                valB = parseNumericField(b.Podiums);
                break;
            case 'fastestLaps':
                valA = parseNumericField(a['Fastest laps']);
                valB = parseNumericField(b['Fastest laps']);
                break;
            default:
                valA = (a.name || a.Name || '').toLowerCase();
                valB = (b.name || b.Name || '').toLowerCase();
        }
        
        // Para tipos numéricos, garantir que sejam tratados como números para comparação
        if (['wins', 'championships', 'seasons', 'raceStarts', 'raceEntries', 'polePositions', 'podiums', 'fastestLaps'].includes(currentFilter)) {
            valA = Number(valA) || 0;
            valB = Number(valB) || 0;
        }
        
        // Comparar valores
        if (valA < valB) return isAscending ? -1 : 1;
        if (valA > valB) return isAscending ? 1 : -1;
        return 0;
    });
    
    return filteredDrivers;
}

// Renderizar pilotos
function renderDrivers() {
    if (!driversGrid) return;
    
    // Forçar limpeza de dados antes de renderizar
    if (window.allDrivers && Array.isArray(window.allDrivers)) {
        window.allDrivers.forEach(driver => {
            // Corrigir problemas com nacionalidade
            if (driver.Nationality && driver.Nationality.includes('[')) {
                driver.Nationality = driver.Nationality.replace(/\s*\[\d+\]\s*/g, '');
            }
            
            // Corrigir problemas com "..." em todos os campos numéricos
            ['Pole positions', 'Wins', 'Podiums', 'Championships', 'Race entries', 'Race starts', 'Fastest laps'].forEach(stat => {
                if (driver[stat]) {
                    const value = String(driver[stat]);
                    if (value.includes('...') || value.endsWith('..') || value.match(/^\d+\.\./) || value === '1..') {
                        const numMatch = value.match(/^(\d+)/);
                        driver[stat] = numMatch ? numMatch[1] : '0';
                    }
                }
            });
        });
    }
    
    const drivers = filterAndSortDrivers();
    const startIndex = (currentPage - 1) * driversPerPage;
    const endIndex = startIndex + driversPerPage;
    const driversToShow = drivers.slice(startIndex, endIndex);
    driversGrid.innerHTML = '';
    
    if (driversToShow.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'Nenhum piloto encontrado';
        driversGrid.appendChild(noResults);
    } else {
        driversToShow.forEach(driver => {
            const card = createDriverCard(driver);
            driversGrid.appendChild(card);
        });
    }
    
    updatePageInfo();
}

// Criar card de piloto
function createDriverCard(driver) {
    // Criar elemento do card
    const driverCard = document.createElement('div');
    driverCard.className = 'driver-card';
    
    // Imagem do piloto
    const driverImage = document.createElement('div');
    driverImage.className = 'driver-image';
    
    const img = document.createElement('img');
    // Usamos path relativo e verificamos se é http(s)
    let imageSrc = driver.image || 'images/f1-logo.svg';
    if (imageSrc && !imageSrc.startsWith('http') && !imageSrc.startsWith('images/')) {
        imageSrc = `images/${imageSrc}`;
    }
    img.src = imageSrc;
    img.alt = driver.Name || 'F1 Driver';
    img.onerror = function() {
        console.log(`Erro ao carregar imagem: ${this.src}`);
        this.src = 'images/f1-logo.svg';
    };
    
    driverImage.appendChild(img);
    driverCard.appendChild(driverImage);
    
    // Informações do piloto
    const driverInfo = document.createElement('div');
    driverInfo.className = 'driver-info';
    
    // Nome e ícones de campeonato
    const nameContainer = document.createElement('div');
    nameContainer.className = 'name-container';
    
    const driverName = document.createElement('h2');
    driverName.className = 'driver-name';
    driverName.textContent = driver.Name || 'Piloto';
    
    const championshipIcons = document.createElement('div');
    championshipIcons.className = 'championship-icons';
    
    // Adicionar ícones para cada campeonato
    const championships = parseInt(driver.Championships) || 0;
    const pilotName = driver.Name || '';
    
    // Determinar a classe CSS apropriada com base no nome do piloto
    let iconClass = 'championship-icon';
    if (pilotName.includes('Michael Schumacher')) {
        iconClass += ' icon-schumacher';
    } else if (pilotName.includes('Lewis Hamilton')) {
        iconClass += ' icon-hamilton';
    } else if (pilotName.includes('Juan Manuel Fangio')) {
        iconClass += ' icon-fangio';
    } else if (pilotName.includes('Sebastian Vettel') || pilotName.includes('Vettel')) {
        iconClass += ' icon-vettel';
    } else if (pilotName.includes('Max Verstappen') || pilotName.includes('Verstappen')) {
        iconClass += ' icon-verstappen';
    }
    
    for (let i = 0; i < championships; i++) {
        const icon = document.createElement('img');
        icon.src = 'images/laurel wreath.svg';
        icon.alt = 'Championship';
        icon.className = iconClass;
        championshipIcons.appendChild(icon);
    }
    
    nameContainer.appendChild(driverName);
    nameContainer.appendChild(championshipIcons);
    driverInfo.appendChild(nameContainer);
    
    // Nacionalidade com bandeira
    const nationality = document.createElement('div');
    nationality.className = 'nationality';
    
    const flag = document.createElement('img');
    flag.className = 'flag';
    const countryCode = formatCountryCode(driver.Nationality);
    flag.src = `https://flagsapi.com/${countryCode}/flat/32.png`;
    flag.alt = driver.Nationality || '';
    flag.onerror = function() {
        this.style.display = 'none';
    };
    
    const countryName = document.createElement('span');
    countryName.className = 'country-name';
    countryName.textContent = driver.Nationality || '';
    
    nationality.appendChild(flag);
    nationality.appendChild(countryName);
    driverInfo.appendChild(nationality);
    
    // Datas (nascimento/morte)
    const datesRow = document.createElement('div');
    datesRow.className = 'dates-row';
    
    // Data de nascimento
    const birthItem = document.createElement('span');
    birthItem.className = 'date-item birth-item';
    
    const birthIcon = document.createElement('img');
    birthIcon.src = 'images/red circle.svg';
    birthIcon.className = 'birth-icon';
    birthIcon.alt = 'Born';
    
    const birthDateText = document.createElement('span');
    birthDateText.className = 'birth-date-text';
    birthDateText.textContent = driver.BirthDate || '';
    
    birthItem.appendChild(birthIcon);
    birthItem.appendChild(birthDateText);
    datesRow.appendChild(birthItem);
    
    // Data de morte (se existir)
    if (driver.DeathDate) {
        const deathItem = document.createElement('span');
        deathItem.className = 'date-item death-item';
        
        const deathIcon = document.createElement('img');
        deathIcon.src = 'images/cross.svg';
        deathIcon.className = 'death-icon';
        deathIcon.alt = 'Died';
        
        const deathDateText = document.createElement('span');
        deathDateText.className = 'death-date-text';
        deathDateText.textContent = driver.DeathDate;
        
        deathItem.appendChild(deathIcon);
        deathItem.appendChild(deathDateText);
        datesRow.appendChild(deathItem);
    }
    
    driverInfo.appendChild(datesRow);
    
    // Temporadas - centralizado como na imagem de referência
    const seasonsStat = document.createElement('div');
    seasonsStat.className = 'stat seasons-stat';
    seasonsStat.style.textAlign = 'center';
    seasonsStat.style.marginBottom = '0.4rem';
    seasonsStat.style.padding = '0.2rem 0';
    seasonsStat.style.borderBottom = '1px dashed #e2e2e4';
    
    // Adicionar atributos para CSS seletivo
    if (driver.Name) {
        seasonsStat.setAttribute('data-driver-name', driver.Name);
    }
    
    // Adicionar atributo para temporadas longas
    const seasonsText = driver.Seasons || '';
    if (seasonsText.length > 12) {
        seasonsStat.setAttribute('data-long-seasons', 'true');
    }
    
    // Criar um único span para 'Seasons:' + anos (sem espaço entre eles)
    const seasonsLabel = document.createElement('span');
    seasonsLabel.className = 'label';
    seasonsLabel.textContent = 'Seasons:';
    seasonsLabel.style.marginRight = '0';
    seasonsLabel.style.paddingRight = '0';
    
    const seasonsValue = document.createElement('span');
    
    // Definir classe base e garantir que não haja espaço
    seasonsValue.className = 'value seasons-value';
    seasonsValue.style.marginLeft = '0';
    seasonsValue.style.paddingLeft = '0';
    seasonsValue.style.display = 'inline';
    
    // O CSS vai cuidar do ajuste de fonte para drivers específicos com o data-driver-name
    
    seasonsValue.textContent = seasonsText;
    
    // Montar a estrutura centralizada
    seasonsStat.appendChild(seasonsLabel);
    seasonsStat.appendChild(seasonsValue);
    driverInfo.appendChild(seasonsStat);
    
    // Stats
    const stats = document.createElement('div');
    stats.className = 'stats';
    
    // Championships
    const championshipsStat = document.createElement('div');
    championshipsStat.className = 'stat';
    championshipsStat.style.whiteSpace = 'nowrap';
    
    const champLabel = document.createElement('span');
    champLabel.className = 'label';
    champLabel.textContent = 'Championships:';
    champLabel.style.marginRight = '0.05rem';
    
    const champValue = document.createElement('span');
    champValue.className = 'value championships-value';
    champValue.textContent = cleanStatValue(driver.Championships);
    
    championshipsStat.appendChild(champLabel);
    championshipsStat.appendChild(champValue);
    stats.appendChild(championshipsStat);
    
    // Race entries
    const entriesStat = document.createElement('div');
    entriesStat.className = 'stat';
    entriesStat.style.whiteSpace = 'nowrap';
    
    const entriesLabel = document.createElement('span');
    entriesLabel.className = 'label';
    entriesLabel.textContent = 'Race entries:';
    entriesLabel.style.marginRight = '0.05rem';
    
    const entriesValue = document.createElement('span');
    entriesValue.className = 'value race-entries-value';
    entriesValue.textContent = cleanStatValue(driver['Race entries']);
    
    entriesStat.appendChild(entriesLabel);
    entriesStat.appendChild(entriesValue);
    stats.appendChild(entriesStat);
    
    // Race starts
    const startsStat = document.createElement('div');
    startsStat.className = 'stat';
    startsStat.style.whiteSpace = 'nowrap';
    
    const startsLabel = document.createElement('span');
    startsLabel.className = 'label';
    startsLabel.textContent = 'Race starts:';
    startsLabel.style.marginRight = '0.05rem';
    
    const startsValue = document.createElement('span');
    startsValue.className = 'value race-starts-value';
    startsValue.textContent = cleanStatValue(driver['Race starts']);
    
    startsStat.appendChild(startsLabel);
    startsStat.appendChild(startsValue);
    stats.appendChild(startsStat);
    
    // Wins
    const winsStat = document.createElement('div');
    winsStat.className = 'stat';
    winsStat.style.whiteSpace = 'nowrap';
    
    const winsLabel = document.createElement('span');
    winsLabel.className = 'label';
    winsLabel.textContent = 'Wins:';
    winsLabel.style.marginRight = '0.05rem';
    
    const winsValue = document.createElement('span');
    winsValue.className = 'value wins-value';
    winsValue.textContent = cleanStatValue(driver.Wins);
    
    winsStat.appendChild(winsLabel);
    winsStat.appendChild(winsValue);
    stats.appendChild(winsStat);
    
    // Podiums
    const podiumsStat = document.createElement('div');
    podiumsStat.className = 'stat';
    podiumsStat.style.whiteSpace = 'nowrap';
    
    const podiumsLabel = document.createElement('span');
    podiumsLabel.className = 'label';
    podiumsLabel.textContent = 'Podiums:';
    podiumsLabel.style.marginRight = '0.05rem';
    
    const podiumsValue = document.createElement('span');
    podiumsValue.className = 'value podiums-value';
    podiumsValue.textContent = cleanStatValue(driver.Podiums);
    
    podiumsStat.appendChild(podiumsLabel);
    podiumsStat.appendChild(podiumsValue);
    stats.appendChild(podiumsStat);
    
    // Pole positions
    const polesStat = document.createElement('div');
    polesStat.className = 'stat';
    polesStat.style.whiteSpace = 'nowrap';
    
    const polesLabel = document.createElement('span');
    polesLabel.className = 'label';
    polesLabel.textContent = 'Pole positions:';
    polesLabel.style.marginRight = '0.05rem';
    
    const polesValue = document.createElement('span');
    polesValue.className = 'value pole-positions-value';
    polesValue.textContent = cleanStatValue(driver['Pole positions']);
    
    polesStat.appendChild(polesLabel);
    polesStat.appendChild(polesValue);
    stats.appendChild(polesStat);
    
    // Fastest laps
    const lapsStat = document.createElement('div');
    lapsStat.className = 'stat';
    lapsStat.style.whiteSpace = 'nowrap';
    
    const lapsLabel = document.createElement('span');
    lapsLabel.className = 'label';
    lapsLabel.textContent = 'Fastest laps:';
    lapsLabel.style.marginRight = '0.05rem';
    
    const lapsValue = document.createElement('span');
    lapsValue.className = 'value fastest-laps-value';
    lapsValue.textContent = cleanStatValue(driver['Fastest laps']);
    
    lapsStat.appendChild(lapsLabel);
    lapsStat.appendChild(lapsValue);
    stats.appendChild(lapsStat);
    
    driverInfo.appendChild(stats);
    driverCard.appendChild(driverInfo);
    
    return driverCard;
}

// Formatação de código de país para exibição da bandeira
function formatCountryCode(nationality) {
    // Se já for um código válido de duas letras, retorna ele mesmo
    if (nationality && nationality.length === 2 && nationality.toUpperCase() === nationality) {
        return nationality;
    }
    
    // Mapeamento de nomes de países para códigos ISO de 2 letras para a API de bandeiras
    const countryCodeMap = {
        // Europa
        'British': 'GB', 'UK': 'GB', 'England': 'GB', 'Scottish': 'GB', 'United Kingdom': 'GB',
        'German': 'DE', 'Germany': 'DE', 'Deutschland': 'DE',
        'Italian': 'IT', 'Italy': 'IT', 'Italia': 'IT',
        'French': 'FR', 'France': 'FR',
        'Spanish': 'ES', 'Spain': 'ES', 'España': 'ES',
        'Finnish': 'FI', 'Finland': 'FI',
        'Dutch': 'NL', 'Netherlands': 'NL', 'Holland': 'NL',
        'Belgian': 'BE', 'Belgium': 'BE',
        'Swiss': 'CH', 'Switzerland': 'CH',
        'Austrian': 'AT', 'Austria': 'AT',
        'Portuguese': 'PT', 'Portugal': 'PT',
        'Swedish': 'SE', 'Sweden': 'SE',
        'Danish': 'DK', 'Denmark': 'DK',
        'Polish': 'PL', 'Poland': 'PL',
        'Russian': 'RU', 'Russia': 'RU',
        'Monegasque': 'MC', 'Monaco': 'MC',
        'Irish': 'IE', 'Ireland': 'IE',
        'Czech': 'CZ', 'Czechia': 'CZ', 'Czech Republic': 'CZ',
        'Hungarian': 'HU', 'Hungary': 'HU',
        'Norwegian': 'NO', 'Norway': 'NO',
        'Liechtenstein': 'LI',
        'Rhodesian': 'ZW', 'Rhodesia': 'ZW',
        'Luxembourg': 'LU',
        'Greek': 'GR', 'Greece': 'GR',
        'Andorran': 'AD', 'Andorra': 'AD',
        'San Marino': 'SM', 'Sammarinese': 'SM',
        
        // Américas
        'American': 'US', 'USA': 'US', 'United States': 'US',
        'Canadian': 'CA', 'Canada': 'CA',
        'Mexican': 'MX', 'Mexico': 'MX',
        'Brazilian': 'BR', 'Brazil': 'BR', 'Brasil': 'BR',
        'Argentine': 'AR', 'Argentinian': 'AR', 'Argentina': 'AR',
        'Venezuelan': 'VE', 'Venezuela': 'VE',
        'Colombian': 'CO', 'Colombia': 'CO',
        'Chilean': 'CL', 'Chile': 'CL',
        'Uruguayan': 'UY', 'Uruguay': 'UY',
        
        // Ásia e Oceania
        'Japanese': 'JP', 'Japan': 'JP',
        'Chinese': 'CN', 'China': 'CN',
        'Indian': 'IN', 'India': 'IN',
        'Thai': 'TH', 'Thailand': 'TH',
        'Malaysian': 'MY', 'Malaysia': 'MY',
        'Indonesian': 'ID', 'Indonesia': 'ID',
        'Australian': 'AU', 'Australia': 'AU',
        'New Zealand': 'NZ', 'New Zealander': 'NZ',
        'Singaporean': 'SG', 'Singapore': 'SG',
        
        // África e Oriente Médio
        'South African': 'ZA', 'South Africa': 'ZA',
        'Emirati': 'AE', 'UAE': 'AE', 'United Arab Emirates': 'AE',
        'Moroccan': 'MA', 'Morocco': 'MA',
        'Lebanese': 'LB', 'Lebanon': 'LB',
        'Kuwaiti': 'KW', 'Kuwait': 'KW',
        'Zimbabwe': 'ZW', 'Zimbabwean': 'ZW'
    };
    
    // Buscar correspondência pelo nome do país
    for (const country in countryCodeMap) {
        if (nationality.includes(country)) {
            return countryCodeMap[country];
        }
    }
    
    // Se não encontrar correspondência, retornar código desconhecido
    return 'XX';
}

function monitorarImagens() {
  console.log('[Sistema] Monitorando imagens...');
  
  // Monitora TODAS as imagens dos cards
  document.querySelectorAll('.driver-card img').forEach(img => {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach(() => {
        console.log(`Imagem atualizada: ${img.src}`);
        location.reload();
      });
    });
    
    observer.observe(img, {
      attributes: true,
      attributeFilter: ['src'],
      subtree: true
    });
  });
}

// Atualiza a cada 15s como fallback
setInterval(() => {
  console.log('[Sistema] Verificação periódica de imagens');
  document.querySelectorAll('.driver-card img').forEach(img => {
    img.src = img.src.split('?')[0] + '?' + Date.now();
  });
}, 15000);
