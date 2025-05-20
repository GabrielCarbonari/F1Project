import json
import re

# Carregar o arquivo original
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Função para corrigir formatos
def clean_data(driver):
    # Corrigir caracteres inválidos em Seasons
    if 'Seasons' in driver:
        driver['Seasons'] = re.sub(r'[^0-9\u2013,–\-]', '', driver['Seasons'])
    
    # Corrigir datas inválidas
    if 'BirthDate' in driver and 'and' in driver['BirthDate']:
        parts = driver['BirthDate'].split('and')
        if len(parts[0].strip()) == 2:  # Assume ano
            driver['BirthDate'] = parts[0].strip()
        else:
            driver['BirthDate'] = ''
    
    return driver

# Aplicar correções
drivers_clean = [clean_data(d) for d in drivers]

# Salvar novo arquivo
with open('data/drivers_clean.json', 'w', encoding='utf-8') as f:
    json.dump(drivers_clean, f, indent=2, ensure_ascii=False)

print(f"Arquivo limpo salvo como 'drivers_clean.json' com {len(drivers_clean)} pilotos")
