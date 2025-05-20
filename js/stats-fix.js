// Código de estatísticas completo para substituição
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
    champValue.textContent = driver.Championships || '0';
    
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
    entriesValue.textContent = driver['Race entries'] || '0';
    
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
    startsValue.textContent = driver['Race starts'] || '0';
    
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
    winsValue.textContent = driver.Wins || '0';
    
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
    podiumsValue.textContent = driver.Podiums || '0';
    
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
    polesValue.textContent = driver['Pole positions'] || '0';
    
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
    lapsValue.textContent = driver['Fastest laps'] || '0';
    
    lapsStat.appendChild(lapsLabel);
    lapsStat.appendChild(lapsValue);
    stats.appendChild(lapsStat);
    
    driverInfo.appendChild(stats);
