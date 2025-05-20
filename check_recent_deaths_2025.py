import json
import requests
from bs4 import BeautifulSoup
import time
import datetime
from urllib.parse import quote

def get_death_info(driver_name):
    """Busca informações sobre a morte de um piloto na Wikipedia"""
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
                return None
                
            # Usar o primeiro resultado
            page_url = "https://en.wikipedia.org" + search_results[0]['href']
        
        # Agora temos a URL da página, buscar informações sobre morte
        response = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Verificar se há informação sobre morte na infobox
        infobox = soup.select_one('.infobox')
        if infobox:
            # Procurar por "Died" na infobox
            for row in infobox.select('tr'):
                header = row.select_one('th')
                if not header:
                    continue
                    
                if 'Died' in header.text:
                    # Encontrou informação sobre morte
                    death_info = row.select_one('td').text.strip()
                    return death_info
        
        # Verificar no primeiro parágrafo se há menção a "died"
        first_para = soup.select_one('#mw-content-text p')
        if first_para and 'died' in first_para.text.lower():
            return first_para.text
            
        # Não encontrou informação sobre morte, provavelmente está vivo
        return None
        
    except Exception as e:
        print(f"Erro ao buscar {driver_name}: {e}")
        return None

# Lista de pilotos já confirmados mortos recentemente mas que podem não estar no arquivo
known_deaths = {
    "Alberto Colombo": {"death_date": "07/01/2024"},
    "Wilson Fittipaldi": {"death_date": "23/02/2024"},
    "Jean-Pierre Jabouille": {"death_date": "02/02/2023"},
    "Patrick Tambay": {"death_date": "04/12/2022"},
    "Carlos Reutemann": {"death_date": "07/07/2021"},
    "Phil Hill": {"death_date": "28/08/2008"},
    "Ken Block": {"death_date": "02/01/2023"},
    "Reine Wisell": {"death_date": "20/03/2022"}
}

# Carregar dados dos pilotos
print("Carregando arquivo de pilotos...")
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Estatísticas de verificação
total_drivers = len(drivers)
checked = 0
updated = 0
error_list = []

# Primeiro, atualizar os pilotos com mortes conhecidas
for driver in drivers:
    name = driver["Name"]
    if name in known_deaths:
        old_death_date = driver.get("DeathDate", "")
        new_death_date = known_deaths[name]["death_date"]
        
        if old_death_date != new_death_date:
            print(f"Atualizando data de morte de {name}: {old_death_date} -> {new_death_date}")
            driver["DeathDate"] = new_death_date
            updated += 1

# Salvar o arquivo atualizado
with open('data/drivers.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, ensure_ascii=False, indent=4)

# Verificar uma amostra de pilotos mais antigos que talvez tenham falecido
# (foco em pilotos que não temos data de morte registrada)
print("\nVerificando mortes recentes de pilotos...")
sample_size = 50  # Número de pilotos a verificar
checked_count = 0

for driver in drivers:
    if checked_count >= sample_size:
        break
        
    name = driver["Name"]
    birth_date = driver.get("BirthDate", "")
    death_date = driver.get("DeathDate", "")
    
    # Pular pilotos que já têm data de morte ou são muito recentes
    if death_date or name in known_deaths:
        continue
        
    # Tentar verificar se pilotos nascidos antes de 1950 faleceram
    try:
        if birth_date:
            birth_year = int(birth_date.split('/')[-1])
            if birth_year < 1950:
                print(f"Verificando {name} (nascido em {birth_year})...")
                death_info = get_death_info(name)
                
                if death_info and ('died' in death_info.lower() or 'death' in death_info.lower()):
                    print(f"ENCONTROU INFORMAÇÃO DE MORTE para {name}: {death_info}")
                    error_list.append(f"{name}: {death_info}")
                
                # Pausa para não sobrecarregar a Wikipedia
                time.sleep(1)
                checked_count += 1
    except Exception as e:
        print(f"Erro ao processar {name}: {e}")

# Relatório final
print("\nRelatório de verificação:")
print(f"Total de pilotos verificados: {updated + checked_count}")
print(f"Datas de morte atualizadas: {updated}")
print(f"Pilotos com possíveis mortes não registradas: {len(error_list)}")

if error_list:
    print("\nLista de pilotos com possíveis mortes não registradas:")
    for error in error_list:
        print(f"- {error}")

print("\nVerificação concluída. Arquivo 'data/drivers.json' foi atualizado.")
