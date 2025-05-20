import json
import requests
import time
import re
from datetime import datetime

# Função para buscar informações na API da Wikipedia
def get_wikipedia_info(driver_name):
    print(f"Buscando informações para: {driver_name}")
    
    # Formatar o nome para URL da Wikipedia
    search_name = driver_name.replace(" ", "+")
    
    # Usar a API da Wikipedia para buscar informações
    api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_name}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        # Tentar busca alternativa
        search_api = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"{driver_name} Formula 1 driver",
            "utf8": 1
        }
        
        search_response = requests.get(search_api, params=params)
        if search_response.status_code != 200 or not search_response.json().get("query", {}).get("search"):
            print(f"Nenhum resultado encontrado para {driver_name}")
            return None, None
            
        # Pegar o primeiro resultado
        title = search_response.json()["query"]["search"][0]["title"]
        api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            print(f"Falha ao acessar página para {driver_name}")
            return None, None
    
    # Extrair o HTML da página
    page_data = response.json()
    
    # Tentar extrair datas do texto
    extract = page_data.get("extract", "")
    
    # Padrões para datas
    birth_pattern = r"born (\d{1,2} \w+ \d{4})"
    death_pattern = r"died (\d{1,2} \w+ \d{4})"
    
    birth_date = None
    death_date = None
    
    # Buscar data de nascimento
    birth_match = re.search(birth_pattern, extract)
    if birth_match:
        birth_date = birth_match.group(1)
        
    # Buscar data de morte
    death_match = re.search(death_pattern, extract)
    if death_match:
        death_date = death_match.group(1)
    
    # Se não encontrou no resumo, buscar na página completa
    if not birth_date or not death_date:
        # Obter o HTML completo da página
        title = page_data.get("title", "").replace(" ", "_")
        html_url = f"https://en.wikipedia.org/w/api.php?action=parse&page={title}&format=json"
        html_response = requests.get(html_url)
        
        if html_response.status_code == 200:
            html_data = html_response.json()
            if "parse" in html_data and "text" in html_data["parse"]:
                html_content = html_data["parse"]["text"]["*"]
                
                # Padrões mais abrangentes
                if not birth_date:
                    birth_matches = re.findall(r"(\d{1,2} \w+ \d{4})", html_content)
                    if birth_matches:
                        birth_date = birth_matches[0]  # Assume primeira data é nascimento
                
                if not death_date:
                    # Procurar padrões de morte
                    death_indicators = ["died", "death", "passed away"]
                    for indicator in death_indicators:
                        if indicator in html_content.lower():
                            # Buscar data próxima ao indicador
                            death_context = html_content[html_content.lower().find(indicator):html_content.lower().find(indicator)+200]
                            death_matches = re.findall(r"(\d{1,2} \w+ \d{4})", death_context)
                            if death_matches:
                                death_date = death_matches[0]
                                break
    
    # Formatar datas se encontradas
    if birth_date:
        try:
            # Tentar converter para formato padrão
            birth_date_obj = datetime.strptime(birth_date, '%d %B %Y')
            birth_date = birth_date_obj.strftime('%d/%m/%Y')
        except:
            pass  # Manter o formato original se falhar
    
    if death_date:
        try:
            # Tentar converter para formato padrão
            death_date_obj = datetime.strptime(death_date, '%d %B %Y')
            death_date = death_date_obj.strftime('%d/%m/%Y')
        except:
            pass  # Manter o formato original se falhar
    
    print(f"Encontrado: Nascimento: {birth_date}, Falecimento: {death_date}")
    return birth_date, death_date

# Carregar o JSON atual
print("Carregando JSON...")
with open('C:\\Users\\GCO\\CascadeProjects\\JSON\\formula1_drivers.json', 'r', encoding='utf-8-sig') as f:
    drivers = json.load(f)

# Contador para acompanhamento
total_drivers = len(drivers)
processed = 0

# Atualizar cada piloto
for driver in drivers:
    processed += 1
    driver_name = driver["Name"]
    
    # Verificar se já tem as datas
    if "BirthDate" in driver and "DeathDate" in driver:
        print(f"[{processed}/{total_drivers}] {driver_name} já possui datas. Pulando...")
        continue
    
    # Buscar informações
    birth_date, death_date = get_wikipedia_info(driver_name)
    
    # Atualizar o driver com as novas informações
    if birth_date:
        driver["BirthDate"] = birth_date
    
    if death_date:
        driver["DeathDate"] = death_date
    
    # Salvar o progresso a cada 5 pilotos
    if processed % 5 == 0:
        print(f"Salvando progresso... ({processed}/{total_drivers})")
        with open('C:\\Users\\GCO\\CascadeProjects\\JSON\\formula1_drivers_updated_v2.json', 'w', encoding='utf-8') as f:
            json.dump(drivers, f, indent=4, ensure_ascii=False)
    
    # Pausa para evitar sobrecarga no servidor
    time.sleep(1)

# Salvar o JSON atualizado
print("Salvando JSON final...")
with open('C:\\Users\\GCO\\CascadeProjects\\JSON\\formula1_drivers_updated_v2.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, indent=4, ensure_ascii=False)

print(f"Concluído! Processados {total_drivers} pilotos.")
