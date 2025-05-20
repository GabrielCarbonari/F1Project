import json
import requests
import time
import datetime
from bs4 import BeautifulSoup
import re

# Função para obter dados da Wikipedia para um piloto
def get_driver_info_from_wikipedia(driver_name):
    try:
        # Formatar o nome para a busca na Wikipedia
        search_name = driver_name.replace(" ", "+")
        search_url = f"https://en.wikipedia.org/w/index.php?search={search_name}+Formula+One+driver"
        
        # Primeira tentativa - busca direta
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Verificar se fomos redirecionados para uma página específica
        if 'Search results' in response.text:
            # Tentar pegar o primeiro resultado
            first_result = soup.select_one('.mw-search-result-heading a')
            if first_result:
                driver_url = "https://en.wikipedia.org" + first_result['href']
                response = requests.get(driver_url)
                soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar a infobox
        infobox = soup.select_one('.infobox')
        if not infobox:
            return None, None

        # Procurar data de nascimento
        birth_date = None
        death_date = None
        
        # Procurar na infobox
        rows = infobox.select('tr')
        for row in rows:
            header = row.select_one('th')
            if header and 'Born' in header.text:
                # Buscar data no formato DD Month YYYY
                date_text = row.select_one('td').text
                # Usar regex para extrair datas no formato dia/mês/ano
                date_match = re.search(r'(\d{1,2})[\s]*([A-Za-z]+)[\s]*(\d{4})', date_text)
                if date_match:
                    day, month, year = date_match.groups()
                    month_map = {
                        'January': '01', 'February': '02', 'March': '03', 'April': '04',
                        'May': '05', 'June': '06', 'July': '07', 'August': '08',
                        'September': '09', 'October': '10', 'November': '11', 'December': '12'
                    }
                    if month in month_map:
                        birth_date = f"{day.zfill(2)}/{month_map[month]}/{year}"
                    else:
                        # Tentar com abreviações de mês
                        for full_month, month_num in month_map.items():
                            if month.startswith(full_month[:3]):
                                birth_date = f"{day.zfill(2)}/{month_num}/{year}"
                                break
            
            if header and ('Died' in header.text or 'Death' in header.text):
                # Extrair data de morte similarmente
                date_text = row.select_one('td').text
                date_match = re.search(r'(\d{1,2})[\s]*([A-Za-z]+)[\s]*(\d{4})', date_text)
                if date_match:
                    day, month, year = date_match.groups()
                    month_map = {
                        'January': '01', 'February': '02', 'March': '03', 'April': '04',
                        'May': '05', 'June': '06', 'July': '07', 'August': '08',
                        'September': '09', 'October': '10', 'November': '11', 'December': '12'
                    }
                    if month in month_map:
                        death_date = f"{day.zfill(2)}/{month_map[month]}/{year}"
                    else:
                        # Tentar com abreviações de mês
                        for full_month, month_num in month_map.items():
                            if month.startswith(full_month[:3]):
                                death_date = f"{day.zfill(2)}/{month_num}/{year}"
                                break
        
        return birth_date, death_date
    
    except Exception as e:
        print(f"Erro ao buscar informações para {driver_name}: {str(e)}")
        return None, None

# Função alternativa usando a API DBpedia
def get_driver_info_from_dbpedia(driver_name):
    try:
        sparql_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        
        SELECT ?birthDate ?deathDate WHERE {{
          ?person a dbo:RacingDriver ;
                 foaf:name ?name ;
                 dbo:birthDate ?birthDate .
          OPTIONAL {{ ?person dbo:deathDate ?deathDate }}
          FILTER(CONTAINS(LCASE(?name), LCASE("{driver_name}")))
        }}
        LIMIT 1
        """
        
        url = "https://dbpedia.org/sparql"
        params = {
            "query": sparql_query,
            "format": "json"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data and 'results' in data and 'bindings' in data['results'] and data['results']['bindings']:
            result = data['results']['bindings'][0]
            
            birth_date = None
            if 'birthDate' in result:
                birth_date_raw = result['birthDate']['value']
                birth_date_dt = datetime.datetime.strptime(birth_date_raw.split('T')[0], '%Y-%m-%d')
                birth_date = birth_date_dt.strftime('%d/%m/%Y')
            
            death_date = None
            if 'deathDate' in result:
                death_date_raw = result['deathDate']['value']
                death_date_dt = datetime.datetime.strptime(death_date_raw.split('T')[0], '%Y-%m-%d')
                death_date = death_date_dt.strftime('%d/%m/%Y')
            
            return birth_date, death_date
        
        return None, None
    
    except Exception as e:
        print(f"Erro ao buscar na DBpedia para {driver_name}: {str(e)}")
        return None, None

# Carregar o arquivo JSON atual
print("Carregando arquivo JSON...")
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

total_drivers = len(drivers_data)
updated_count = 0
not_found_count = 0

print(f"Total de {total_drivers} pilotos encontrados. Iniciando atualização...")

# Driver manual database for some problematic drivers
manual_data = {
    "Bob Drake": {"birth": "14/12/1919", "death": "18/04/1990"},
    "Bob Said": {"birth": "05/05/1932", "death": "24/03/2002"},
    "Bobby Rahal": {"birth": "10/01/1953", "death": ""},
    # Add more manual entries here if needed
}

# Lista para armazenar pilotos sem dados encontrados
not_found_drivers = []

# Processar cada piloto
for i, driver in enumerate(drivers_data):
    driver_name = driver["Name"]
    
    # Verificar se já temos dados manuais para este piloto
    if driver_name in manual_data:
        birth_date = manual_data[driver_name]["birth"]
        death_date = manual_data[driver_name]["death"]
        print(f"[{i+1}/{total_drivers}] {driver_name}: Usando dados manuais")
    else:
        # Tentar obter dados da Wikipedia
        birth_date, death_date = get_driver_info_from_wikipedia(driver_name)
        
        # Se não encontrarmos na Wikipedia, tentar DBpedia
        if not birth_date:
            birth_date, death_date = get_driver_info_from_dbpedia(driver_name)
        
        # Adicionar pequeno delay para não sobrecarregar as APIs
        time.sleep(0.5)
    
    # Atualizar os dados se encontrados
    updated = False
    if birth_date:
        driver["BirthDate"] = birth_date
        updated = True
    
    if death_date:
        driver["DeathDate"] = death_date
        # Se temos uma data de morte, assumimos que o acidente fatal é "No" por padrão
        # A menos que já esteja definido como "Yes"
        if "fatal accident" not in driver or driver["fatal accident"] == "":
            driver["fatal accident"] = "No"
    else:
        # Se não há data de morte, garantimos que o campo existe mas está vazio
        if "DeathDate" not in driver:
            driver["DeathDate"] = ""
    
    # Garantir que o campo "fatal accident" existe
    if "fatal accident" not in driver:
        driver["fatal accident"] = "No"
    
    if updated:
        updated_count += 1
        print(f"[{i+1}/{total_drivers}] {driver_name}: Atualizado - Nascimento: {birth_date}, Morte: {death_date or 'N/A'}")
    else:
        not_found_count += 1
        not_found_drivers.append(driver_name)
        print(f"[{i+1}/{total_drivers}] {driver_name}: Não foi possível encontrar informações")

# Salvar o JSON atualizado
print(f"\nSalvando arquivo JSON atualizado...")
with open('data/drivers.json', 'w', encoding='utf-8') as file:
    json.dump(drivers_data, file, indent=4)

print(f"\nResumo da atualização:")
print(f"Total de pilotos: {total_drivers}")
print(f"Pilotos atualizados: {updated_count}")
print(f"Pilotos sem informações encontradas: {not_found_count}")

# Exibir lista de pilotos sem informações encontradas
if not_found_drivers:
    print("\nPilotos sem informações encontradas:")
    for driver in not_found_drivers:
        print(f"- {driver}")

print("\nProcesso concluído!")
