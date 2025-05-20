import json
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import wikipediaapi

# Inicializar a API da Wikipedia
wiki_wiki = wikipediaapi.Wikipedia('Formula1DriverUpdater/1.0', 'en')

def parse_date(date_text):
    """Parse date from various formats to DD/MM/YYYY"""
    if not date_text:
        return None
        
    # Padrões comuns de data na Wikipedia
    patterns = [
        r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})',  # 17 October 1969
        r'(\d{4})-(\d{2})-(\d{2})',  # 1969-10-17
        r'(\d{1,2})/(\d{1,2})/(\d{4})'  # 17/10/1969
    ]
    
    for pattern in patterns:
        match = re.search(pattern, date_text)
        if match:
            try:
                if len(match.groups()) == 3 and match.group(2) in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                    # Formato 17 October 1969
                    day = int(match.group(1))
                    month_names = {
                        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                    }
                    month = month_names[match.group(2)]
                    year = int(match.group(3))
                    # Validar data
                    if validate_date(day, month, year):
                        return f"{day:02d}/{month:02d}/{year}"
                elif re.match(r'\d{4}-\d{2}-\d{2}', match.group(0)):
                    # Formato YYYY-MM-DD
                    year = int(match.group(1))
                    month = int(match.group(2))
                    day = int(match.group(3))
                    # Validar data
                    if validate_date(day, month, year):
                        return f"{day:02d}/{month:02d}/{year}"
                else:
                    # Formato DD/MM/YYYY
                    day = int(match.group(1))
                    month = int(match.group(2))
                    year = int(match.group(3))
                    # Validar data
                    if validate_date(day, month, year):
                        return f"{day:02d}/{month:02d}/{year}"
            except (ValueError, IndexError):
                continue
    
    return None


def validate_date(day, month, year):
    """Validate if the date is potentially valid"""
    # Verificar limites básicos
    if year < 1850 or year > 2025:  # Pilotos de F1 não nasceram antes de 1850
        return False
    
    if month < 1 or month > 12:
        return False
        
    # Verificar dias por mês
    days_in_month = [0, 31, 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 
                    31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    
    if day < 1 or day > days_in_month[month]:
        return False
        
    return True

# Função para buscar informações na Wikipedia usando a API
def get_wikipedia_info(driver_name):
    print(f"Buscando informações para: {driver_name}")
    
    # Tentativa 1: buscar pelo nome exato
    page = wiki_wiki.page(driver_name)
    
    # Tentativa 2: buscar com '(racing driver)' ou '(Formula One driver)'
    if not page.exists() or 'may refer to' in page.summary:
        page = wiki_wiki.page(f"{driver_name} (racing driver)")
    
    if not page.exists() or 'may refer to' in page.summary:
        page = wiki_wiki.page(f"{driver_name} (Formula One driver)")
    
    # Se ainda não encontrou, usar o método de busca
    if not page.exists() or 'may refer to' in page.summary:
        search_name = driver_name.replace(" ", "+")
        search_url = f"https://en.wikipedia.org/w/index.php?search={search_name}+Formula+1+driver"
        response = requests.get(search_url)
        
        # Se foi redirecionado para uma página específica
        if "Special:Search" not in response.url:
            page_title = response.url.split('/')[-1].replace('_', ' ')
            page = wiki_wiki.page(page_title)
        else:
            # Tentar encontrar o link correto nos resultados da busca
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.select('.mw-search-result-heading a')
            
            if not search_results:
                print(f"Nenhum resultado encontrado para {driver_name}")
                return None, None
            
            # Usar o primeiro resultado
            page_title = search_results[0].text
            page = wiki_wiki.page(page_title)
    
    if not page.exists():
        print(f"Página não encontrada para {driver_name}")
        return None, None
    
    # Agora acessar o HTML para extrair datas mais facilmente
    response = requests.get(page.fullurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extrair informações da infobox
    infobox = soup.select_one('.infobox')
    if not infobox:
        print(f"Infobox não encontrada para {driver_name}")
        return None, None
    
    # Procurar datas de nascimento e morte
    birth_date = None
    death_date = None
    
    # Método 1: Procurar nas linhas da infobox
    rows = infobox.select('tr')
    for row in rows:
        header = row.select_one('th')
        if not header:
            continue
            
        header_text = header.text.strip()
        
        if 'Born' in header_text:
            date_cell = row.select_one('td')
            if date_cell:
                date_text = date_cell.text
                birth_date = parse_date(date_text)
        
        if 'Died' in header_text or 'Death' in header_text:
            date_cell = row.select_one('td')
            if date_cell:
                date_text = date_cell.text
                death_date = parse_date(date_text)
    
    # Método 2: Procurar em elementos específicos
    if not birth_date:
        birth_element = soup.select_one('.bday')
        if birth_element:
            birth_date = parse_date(birth_element.text)
    
    # Método 3: Procurar na primeira frase
    if not birth_date or not death_date:
        first_para = soup.select_one('#mw-content-text p')
        if first_para:
            para_text = first_para.text
            # Procurar datas entre parênteses na primeira frase
            date_matches = re.findall(r'\((.*?\d{1,2}\s+[a-zA-Z]+\s+\d{4}.*?)\)', para_text)
            
            if len(date_matches) >= 1 and not birth_date:
                birth_date = parse_date(date_matches[0])
                
            if len(date_matches) >= 2 and not death_date:
                death_date = parse_date(date_matches[1])
    
    print(f"Encontrado: Nascimento: {birth_date}, Falecimento: {death_date}")
    return birth_date, death_date

# Função para verificar se uma data está em formato inválido
def is_invalid_date(date_str):
    if not date_str:
        return False
        
    # Verificar padrões de data inválidos
    invalid_patterns = [
        r'\d+ to \d+',          # 45 to 1947
        r'\d+ and \d+',         # 94 and 2004
        r'\s+and\s+',            # and
        r'^\s*$'                 # string vazia
    ]
    
    return any(re.search(pattern, date_str) for pattern in invalid_patterns)

# Carregar o JSON atual
print("Carregando JSON...")
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Contador para acompanhamento
total_drivers = len(drivers)
processed = 0
updated = 0

# Dados manualmente verificados para pilotos importantes
manual_driver_dates = {
    "Juan Manuel Fangio": {"birth": "24/06/1911", "death": "17/07/1995"},
    "Ayrton Senna": {"birth": "21/03/1960", "death": "01/05/1994"},
    "Michael Schumacher": {"birth": "03/01/1969", "death": ""},
    "Lewis Hamilton": {"birth": "07/01/1985", "death": ""},
    "Duncan Hamilton": {"birth": "30/04/1920", "death": "13/05/1994"},  # Corrigido
    "Sebastian Vettel": {"birth": "03/07/1987", "death": ""},
    "Max Verstappen": {"birth": "30/09/1997", "death": ""},
    "Phil Hill": {"birth": "20/04/1927", "death": "28/08/2008"},
    "Alain Prost": {"birth": "24/02/1955", "death": ""},
    "Niki Lauda": {"birth": "22/02/1949", "death": "20/05/2019"},
    "James Hunt": {"birth": "29/08/1947", "death": "15/06/1993"}
}

# Pilotos que precisam de atenção especial
priority_drivers = list(manual_driver_dates.keys())

# Atualizar cada piloto
for driver in drivers:
    processed += 1
    driver_name = driver["Name"]
    
    # Verificar se é um piloto com datas manualmente verificadas
    if driver_name in manual_driver_dates:
        print(f"[{processed}/{total_drivers}] {driver_name} - usando dados verificados manualmente")
        driver["BirthDate"] = manual_driver_dates[driver_name]["birth"]
        driver["DeathDate"] = manual_driver_dates[driver_name]["death"]
        updated += 2
        continue

    # Verificar se as datas estão em formato inválido ou se é um piloto prioritário
    needs_update = (is_invalid_date(driver.get("BirthDate", "")) or 
                   is_invalid_date(driver.get("DeathDate", "")))
                   
    if not needs_update:
        print(f"[{processed}/{total_drivers}] {driver_name} já possui datas válidas. Pulando...")
        continue

    # Buscar informações da Wikipedia
    birth_date, death_date = get_wikipedia_info(driver_name)

    # Atualizar o driver com as novas informações
    if birth_date:
        driver["BirthDate"] = birth_date
        updated += 1

    if death_date:
        driver["DeathDate"] = death_date
        updated += 1
        
    # Salvar o progresso a cada 10 pilotos
    if processed % 10 == 0 or driver_name in priority_drivers:
        print(f"Salvando progresso... ({processed}/{total_drivers}, {updated} datas atualizadas)")
        with open('data/drivers_dates_updated.json', 'w', encoding='utf-8') as f:
            json.dump(drivers, f, indent=4, ensure_ascii=False)
    
    # Pausa para evitar sobrecarga no servidor
    time.sleep(1)

# Salvar o JSON atualizado
print("Salvando JSON final...")
with open('data/drivers_dates_updated.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, indent=4, ensure_ascii=False)

print(f"Concluído! Processados {processed} pilotos, atualizadas {updated} datas.")
