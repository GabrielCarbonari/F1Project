import json
import requests
from bs4 import BeautifulSoup
import time
import datetime
import re
from urllib.parse import quote

def is_date_valid(date_str):
    """Verifica se uma data está em formato válido e dentro de intervalos razoáveis"""
    if not date_str or date_str.strip() == "":
        return False  # Data vazia é inválida neste contexto
        
    # Verificar padrão DD/MM/YYYY
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
        return False
        
    try:
        day, month, year = map(int, date_str.split('/'))
        
        # Verificar limites razoáveis para pilotos de F1
        current_year = datetime.datetime.now().year
        
        # Nenhum piloto de F1 nasceu depois de 2010 ou antes de 1880
        if year < 1880 or year > 2010:
            return False
            
        # Nenhum piloto morreu antes de 1900 ou no futuro
        if year > current_year:
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

def get_wikipedia_info(driver_name):
    """Busca informações sobre um piloto na Wikipedia"""
    search_url = f"https://en.wikipedia.org/w/index.php?search={quote(driver_name)}+Formula+1+driver&title=Special:Search"
    
    try:
        response = requests.get(search_url, timeout=10)
        
        # Se foi redirecionado direto para uma página
        if "Special:Search" not in response.url:
            page_url = response.url
        else:
            # Caso contrário, procurar nos resultados
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.select('.mw-search-result-heading a')
            
            if not search_results:
                # Tentar busca alternativa sem "Formula 1"
                search_url = f"https://en.wikipedia.org/w/index.php?search={quote(driver_name)}+racing+driver&title=Special:Search"
                response = requests.get(search_url, timeout=10)
                
                if "Special:Search" not in response.url:
                    page_url = response.url
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    search_results = soup.select('.mw-search-result-heading a')
                    
                    if not search_results:
                        return None, None
                    
                    page_url = "https://en.wikipedia.org" + search_results[0]['href']
            else:
                page_url = "https://en.wikipedia.org" + search_results[0]['href']
        
        # Agora temos a URL da página, buscar informações
        response = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        birth_date = None
        death_date = None
        
        # Verificar na infobox
        infobox = soup.select_one('.infobox')
        if infobox:
            # Procurar por "Born" e "Died" na infobox
            for row in infobox.select('tr'):
                header = row.select_one('th')
                if not header:
                    continue
                
                header_text = header.text.strip()
                
                if 'Born' in header_text:
                    birth_info = row.select_one('td').text.strip()
                    # Extrair data no formato DD Month YYYY
                    birth_match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', birth_info)
                    if birth_match:
                        day = int(birth_match.group(1))
                        month_names = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        month = month_names[birth_match.group(2)]
                        year = int(birth_match.group(3))
                        birth_date = f"{day:02d}/{month:02d}/{year}"
                
                if 'Died' in header_text:
                    death_info = row.select_one('td').text.strip()
                    # Extrair data no formato DD Month YYYY
                    death_match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', death_info)
                    if death_match:
                        day = int(death_match.group(1))
                        month_names = {
                            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                        }
                        month = month_names[death_match.group(2)]
                        year = int(death_match.group(3))
                        death_date = f"{day:02d}/{month:02d}/{year}"
        
        # Se não encontrou na infobox, procurar no primeiro parágrafo
        if not birth_date or not death_date:
            first_para = soup.select_one('#mw-content-text p')
            if first_para:
                para_text = first_para.text
                
                # Procurar data de nascimento
                if not birth_date:
                    birth_match = re.search(r'born\s+(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', para_text)
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
                    death_match = re.search(r'died\s+(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', para_text)
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
        print(f"Erro ao buscar {driver_name}: {e}")
        return None, None

# Dicionário com datas verificadas manualmente para pilotos específicos
manual_dates = {
    "Walt Hansgen": {"birth": "28/10/1919", "death": "07/04/1966"},
    "John Love": {"birth": "07/12/1924", "death": "25/04/2005"},
    "Pete Lovely": {"birth": "11/04/1926", "death": "13/05/2011"},
    "Slim Borgudd": {"birth": "23/02/1946", "death": "23/02/2023"},
    "Alberto Colombo": {"birth": "23/02/1946", "death": "07/01/2024"},
    "David Coulthard": {"birth": "27/03/1971", "death": ""},
    "Wilson Fittipaldi": {"birth": "25/12/1943", "death": "23/02/2024"},
    "Timo Glock": {"birth": "18/03/1982", "death": ""},
    "Jean-Pierre Jabouille": {"birth": "01/10/1942", "death": "02/02/2023"},
    "Rupert Keegan": {"birth": "26/02/1955", "death": ""},
    "Pastor Maldonado": {"birth": "09/03/1985", "death": ""},
    "Jochen Mass": {"birth": "30/09/1946", "death": ""},
    "Kenneth McAlpine": {"birth": "21/09/1920", "death": "03/11/2021"},
    "Jolyon Palmer": {"birth": "20/01/1991", "death": ""},
    "Hermano da Silva Ramos": {"birth": "07/12/1925", "death": "30/09/2023"},
    "Alan Rees": {"birth": "12/01/1938", "death": ""},
    "Carlos Reutemann": {"birth": "12/04/1942", "death": "07/07/2021"},
    "Basil van Rooyen": {"birth": "19/04/1939", "death": ""},
    "David Walker": {"birth": "10/06/1941", "death": ""}
}

# Carregar dados dos pilotos
print("Carregando arquivo de pilotos...")
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Estatísticas
total_drivers = len(drivers)
fixed_birth_dates = 0
fixed_death_dates = 0
processed = 0

# Primeiro, aplicar as correções manuais
print("Aplicando correções manuais...")
for driver in drivers:
    name = driver["Name"]
    if name in manual_dates:
        old_birth = driver.get("BirthDate", "")
        old_death = driver.get("DeathDate", "")
        
        if old_birth != manual_dates[name]["birth"]:
            driver["BirthDate"] = manual_dates[name]["birth"]
            print(f"Corrigido {name}: nascimento {old_birth} -> {manual_dates[name]['birth']}")
            fixed_birth_dates += 1
            
        if old_death != manual_dates[name]["death"]:
            driver["DeathDate"] = manual_dates[name]["death"]
            print(f"Corrigido {name}: morte {old_death} -> {manual_dates[name]['death']}")
            fixed_death_dates += 1

# Agora, verificar todos os pilotos com datas ausentes ou inválidas
print("\nVerificando pilotos com datas ausentes ou inválidas...")
for driver in drivers:
    processed += 1
    name = driver["Name"]
    
    # Pular pilotos já corrigidos manualmente
    if name in manual_dates:
        continue
    
    birth_date = driver.get("BirthDate", "")
    death_date = driver.get("DeathDate", "")
    
    # Verificar se as datas são válidas
    birth_valid = is_date_valid(birth_date)
    death_valid = death_date == "" or is_date_valid(death_date)  # Data de morte vazia é válida (piloto vivo)
    
    # Pular pilotos com datas válidas
    if birth_valid and death_valid:
        continue
    
    print(f"[{processed}/{total_drivers}] Verificando {name}...")
    
    # Buscar informações na Wikipedia
    new_birth, new_death = get_wikipedia_info(name)
    
    # Atualizar data de nascimento se necessário
    if not birth_valid and new_birth:
        print(f"  Atualizando data de nascimento: {birth_date} -> {new_birth}")
        driver["BirthDate"] = new_birth
        fixed_birth_dates += 1
    
    # Atualizar data de morte se necessário
    if not death_valid and new_death:
        print(f"  Atualizando data de morte: {death_date} -> {new_death}")
        driver["DeathDate"] = new_death
        fixed_death_dates += 1
    
    # Salvar a cada 10 pilotos processados para evitar perda de dados
    if processed % 10 == 0:
        with open('data/drivers.json', 'w', encoding='utf-8') as f:
            json.dump(drivers, f, ensure_ascii=False, indent=4)
        print(f"  Progresso salvo: {processed}/{total_drivers}")
    
    # Pausa para não sobrecarregar a Wikipedia
    time.sleep(1)

# Salvar o arquivo final
with open('data/drivers.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, ensure_ascii=False, indent=4)

print("\nProcesso concluído!")
print(f"Total de pilotos: {total_drivers}")
print(f"Datas de nascimento corrigidas: {fixed_birth_dates}")
print(f"Datas de morte corrigidas: {fixed_death_dates}")
print("Arquivo 'data/drivers.json' foi atualizado.")
