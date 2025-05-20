import json
import re
import requests
from bs4 import BeautifulSoup
import time
import datetime
from urllib.parse import quote

def is_date_valid(date_str):
    """Verifica se uma data está em formato válido e dentro de intervalos razoáveis"""
    if not date_str or date_str.strip() == "":
        return True  # Data vazia é válida (caso de pilotos vivos sem data de morte)
        
    # Verificar padrão DD/MM/YYYY
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
        return False
        
    try:
        day, month, year = map(int, date_str.split('/'))
        
        # Verificar limites razoáveis para pilotos de F1
        # Nenhum piloto de F1 nasceu antes de 1800 ou depois de 2010
        if year < 1800 or year > 2010:
            return False
            
        # Nenhum piloto morreu antes de 1900 ou no futuro
        current_year = datetime.datetime.now().year
        if "DeathDate" in date_str and (year < 1900 or year > current_year):
            return False
            
        # Verificar se o mês e dia são válidos
        if month < 1 or month > 12:
            return False
            
        days_in_month = [0, 31, 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                      
        if day < 1 or day > days_in_month[month]:
            return False
            
        return True
    except:
        return False

def search_wikipedia(driver_name):
    """Busca a página da Wikipedia para um piloto"""
    search_url = f"https://en.wikipedia.org/w/index.php?search={quote(driver_name)}+Formula+1+driver&title=Special:Search"
    try:
        response = requests.get(search_url, timeout=10)
        
        # Se foi redirecionado direto para uma página
        if "Special:Search" not in response.url:
            return response.url
        
        # Caso contrário, procurar nos resultados
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.select('.mw-search-result-heading a')
        
        if search_results:
            # Usar o primeiro resultado
            result_url = "https://en.wikipedia.org" + search_results[0]['href']
            return result_url
            
        return None
    except Exception as e:
        print(f"Erro ao buscar {driver_name}: {e}")
        return None

def get_dates_from_wikipedia(page_url, driver_name):
    """Extrai datas de nascimento e morte da página da Wikipedia"""
    try:
        response = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        birth_date = None
        death_date = None
        
        # Método 1: Procurar na infobox
        infobox = soup.select_one('.infobox')
        if infobox:
            rows = infobox.select('tr')
            for row in rows:
                header = row.select_one('th')
                if not header:
                    continue
                    
                header_text = header.text.strip()
                value_cell = row.select_one('td')
                
                if not value_cell:
                    continue
                
                # Procurar por "Born" ou "Birth date"
                if 'Born' in header_text or 'Birth date' in header_text:
                    birth_match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', value_cell.text)
                    if birth_match:
                        day = int(birth_match.group(1))
                        month_names = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        month = month_names[birth_match.group(2)]
                        year = int(birth_match.group(3))
                        birth_date = f"{day:02d}/{month:02d}/{year}"
                
                # Procurar por "Died" ou "Death date"
                if 'Died' in header_text or 'Death date' in header_text:
                    death_match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', value_cell.text)
                    if death_match:
                        day = int(death_match.group(1))
                        month_names = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        month = month_names[death_match.group(2)]
                        year = int(death_match.group(3))
                        death_date = f"{day:02d}/{month:02d}/{year}"
        
        # Método 2: Procurar no primeiro parágrafo
        if not birth_date or not death_date:
            first_para = soup.select_one('#mw-content-text p')
            if first_para:
                text = first_para.text
                
                # Procurar data de nascimento
                if not birth_date:
                    birth_match = re.search(r'born\s+(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', text)
                    if birth_match:
                        day = int(birth_match.group(1))
                        month_names = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        month = month_names[birth_match.group(2)]
                        year = int(birth_match.group(3))
                        birth_date = f"{day:02d}/{month:02d}/{year}"
                
                # Procurar data de morte
                if not death_date:
                    death_match = re.search(r'died\s+(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', text)
                    if death_match:
                        day = int(death_match.group(1))
                        month_names = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        month = month_names[death_match.group(2)]
                        year = int(death_match.group(3))
                        death_date = f"{day:02d}/{month:02d}/{year}"
        
        return birth_date, death_date
    except Exception as e:
        print(f"Erro ao processar {driver_name} ({page_url}): {e}")
        return None, None

# Adicionar datas manualmente verificadas para pilotos importantes ou difíceis de buscar
manual_driver_dates = {
    "Juan Manuel Fangio": {"birth": "24/06/1911", "death": "17/07/1995"},
    "Ayrton Senna": {"birth": "21/03/1960", "death": "01/05/1994"},
    "Michael Schumacher": {"birth": "03/01/1969", "death": ""},
    "Lewis Hamilton": {"birth": "07/01/1985", "death": ""},
    "Sebastian Vettel": {"birth": "03/07/1987", "death": ""},
    "Fernando Alonso": {"birth": "29/07/1981", "death": ""},
    "Max Verstappen": {"birth": "30/09/1997", "death": ""},
    "Alan Brown": {"birth": "20/11/1919", "death": "20/01/2004"},
    "Andrea Chiesa": {"birth": "06/05/1964", "death": ""},
    "Carlos Reutemann": {"birth": "12/04/1942", "death": "07/07/2021"},
    "Jean-Pierre Jabouille": {"birth": "01/10/1942", "death": "02/02/2023"},
    "Duncan Hamilton": {"birth": "30/04/1920", "death": "13/05/1994"},
    "Phil Hill": {"birth": "20/04/1927", "death": "28/08/2008"},
    "Adrian Sutil": {"birth": "11/01/1983", "death": ""},
    "Hans Stuck": {"birth": "27/12/1900", "death": "09/02/1978"},
    "Hans-Joachim Stuck": {"birth": "01/01/1951", "death": ""},
    "Jack Brabham": {"birth": "02/04/1926", "death": "19/05/2014"},
    "Alain Prost": {"birth": "24/02/1955", "death": ""},
    "Niki Lauda": {"birth": "22/02/1949", "death": "20/05/2019"}
}

print("Carregando arquivo de pilotos...")
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

total_drivers = len(drivers)
corrected_birth = 0
corrected_death = 0
processed = 0

for driver in drivers:
    processed += 1
    name = driver["Name"]
    
    # Status atual
    current_birth = driver.get("BirthDate", "")
    current_death = driver.get("DeathDate", "")
    
    # Verificar se as datas atuais são válidas
    birth_valid = is_date_valid(current_birth)
    death_valid = is_date_valid(current_death)
    
    # Se ambas são válidas, pular
    if birth_valid and death_valid and name not in manual_driver_dates:
        print(f"[{processed}/{total_drivers}] {name} - datas OK")
        continue
    
    print(f"[{processed}/{total_drivers}] {name} - verificando datas...")
    
    # Usar dados manuais se disponíveis
    if name in manual_driver_dates:
        print(f"  Usando dados verificados manualmente para {name}")
        driver["BirthDate"] = manual_driver_dates[name]["birth"]
        driver["DeathDate"] = manual_driver_dates[name]["death"]
        corrected_birth += 1
        corrected_death += 1
        continue
    
    # Buscar na Wikipedia
    page_url = search_wikipedia(name)
    if not page_url:
        print(f"  Não encontrou página da Wikipedia para {name}")
        continue
    
    birth_date, death_date = get_dates_from_wikipedia(page_url, name)
    
    # Atualizar se encontrou dados
    if birth_date and not birth_valid:
        print(f"  Atualizando data de nascimento de {name}: {current_birth} -> {birth_date}")
        driver["BirthDate"] = birth_date
        corrected_birth += 1
    
    if death_date and not death_valid:
        print(f"  Atualizando data de morte de {name}: {current_death} -> {death_date}")
        driver["DeathDate"] = death_date
        corrected_death += 1
    
    # Salvar a cada 10 pilotos processados
    if processed % 10 == 0:
        with open('data/drivers_all_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(drivers, f, ensure_ascii=False, indent=4)
        print(f"Progresso salvo: {processed}/{total_drivers} pilotos processados")
    
    # Pausa para não sobrecarregar a Wikipedia
    time.sleep(1)

# Salvar arquivo final
with open('data/drivers_all_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, ensure_ascii=False, indent=4)

print(f"\nProcesso concluído!")
print(f"Total de pilotos: {total_drivers}")
print(f"Datas de nascimento corrigidas: {corrected_birth}")
print(f"Datas de morte corrigidas: {corrected_death}")
print("Arquivo salvo como 'data/drivers_all_fixed.json'")
