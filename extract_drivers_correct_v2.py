import os
import json
from bs4 import BeautifulSoup
import re

# Caminho do arquivo HTML da Wikipedia
html_file_path = r'C:\Users\GCO\Desktop\List of Formula One drivers - Wikipedia.html'

# Pasta de imagens dos pilotos
drivers_images_path = r'C:\Users\GCO\CascadeProjects\F1Project\images\Pilotos'

# Caminho para salvar o arquivo JSON
output_json_path = r'C:\Users\GCO\CascadeProjects\F1Project\data\drivers.json'

# Função para obter imagem do piloto
def get_driver_image_path(driver_name):
    # Lista todas as imagens na pasta
    images = os.listdir(drivers_images_path)
    # Remove extensão e caracteres especiais para comparação
    driver_name_cleaned = re.sub(r'[^\w\s]', '', driver_name.strip()).lower()
    
    # Procura a imagem correspondente
    for image in images:
        # Remove extensão para comparação
        image_name = os.path.splitext(image)[0].lower()
        image_name_cleaned = re.sub(r'[^\w\s]', '', image_name)
        
        if driver_name_cleaned == image_name_cleaned:
            return f"images/Pilotos/{image}"
    
    # Imagem padrão se não encontrar
    return "images/f1-logo.svg"

# Função para extrair dados dos pilotos corretamente
def extract_drivers_data():
    # Ler o arquivo HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Criar parser BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar a tabela de pilotos
    driver_table = soup.find('table', {'class': 'wikitable'})
    
    # Verificar cabeçalhos para entender a estrutura da tabela
    headers = driver_table.find_all('th')
    header_texts = [header.text.strip() for header in headers]
    
    print("Cabeçalhos da tabela:")
    for i, header in enumerate(header_texts):
        print(f"Coluna {i}: {header}")
    
    # Na tabela da Wikipedia, os cabeçalhos corretos são:
    # 0: Driver name, 1: Nationality, 2: Seasons competed, 3: Drivers' Championships,
    # 4: Race entries, 5: Race starts, 6: Pole positions, 7: Race wins,
    # 8: Podiums, 9: Fastest laps, 10: Points
    
    # Mapeamento correto dos índices das colunas
    POLE_POSITIONS_INDEX = 6
    RACE_WINS_INDEX = 7
    PODIUMS_INDEX = 8
    FASTEST_LAPS_INDEX = 9
    
    drivers_data = []
    
    # Pular a linha de cabeçalho
    rows = driver_table.find_all('tr')[1:]
    
    for row in rows:
        columns = row.find_all('td')
        
        if len(columns) < 10:  # Verificar se tem colunas suficientes
            continue
        
        # Extrair nome do piloto
        driver_name_element = columns[0].find('a')
        if driver_name_element:
            driver_name = driver_name_element.text.strip()
        else:
            driver_name = columns[0].text.strip()
        
        # Extrair nacionalidade
        nationality_text = columns[1].text.strip()
        nationality_code = get_nationality_code(nationality_text)
        
        # Extrair temporadas
        seasons = columns[2].text.strip()
        
        # Extrair campeonatos
        championships = columns[3].text.strip()
        try:
            championships = int(championships)
        except:
            championships = 0
        
        # Extrair entradas em corridas
        race_entries = columns[4].text.strip()
        try:
            race_entries = int(race_entries)
        except:
            race_entries = 0
        
        # Extrair largadas
        race_starts = columns[5].text.strip()
        try:
            race_starts = int(race_starts)
        except:
            race_starts = 0
        
        # Extrair POLE POSITIONS (coluna 6)
        pole_positions = "0"
        if len(columns) > POLE_POSITIONS_INDEX:
            pole_positions = columns[POLE_POSITIONS_INDEX].text.strip()
        try:
            pole_positions = int(pole_positions)
        except:
            pole_positions = 0
        
        # Extrair VITÓRIAS (coluna 7)
        wins = "0"
        if len(columns) > RACE_WINS_INDEX:
            wins = columns[RACE_WINS_INDEX].text.strip()
        try:
            wins = int(wins)
        except:
            wins = 0
        
        # Extrair PÓDIOS (coluna 8)
        podiums = "0"
        if len(columns) > PODIUMS_INDEX:
            podiums = columns[PODIUMS_INDEX].text.strip()
        try:
            podiums = int(podiums)
        except:
            podiums = 0
        
        # Extrair VOLTAS MAIS RÁPIDAS (coluna 9)
        fastest_laps = "0"
        if len(columns) > FASTEST_LAPS_INDEX:
            fastest_laps = columns[FASTEST_LAPS_INDEX].text.strip()
        try:
            fastest_laps = int(fastest_laps)
        except:
            fastest_laps = 0
        
        # Obter caminho da imagem
        image_path = get_driver_image_path(driver_name)
        
        # Criar objeto do piloto
        driver = {
            "name": driver_name,
            "nationality": nationality_code,
            "seasons": seasons,
            "championships": championships,
            "raceEntries": race_entries,
            "raceStarts": race_starts,
            "polePositions": pole_positions,  # Agora na posição correta
            "wins": wins,                    # Agora na posição correta
            "podiums": podiums,              # Agora na posição correta
            "fastestLaps": fastest_laps,
            "image": image_path
        }
        
        drivers_data.append(driver)
    
    # Ordenar pilotos por nome
    drivers_data.sort(key=lambda x: x["name"])
    
    return drivers_data

# Função para obter o código da nacionalidade a partir do texto
def get_nationality_code(nationality_text):
    # Mapeamento de nacionalidades para códigos de país
    nationality_map = {
        "British": "GB",
        "German": "DE",
        "Finnish": "FI",
        "Spanish": "ES",
        "Dutch": "NL",
        "French": "FR",
        "Brazilian": "BR",
        "Australian": "AU",
        "Monégasque": "MC",
        "Canadian": "CA",
        "Mexican": "MX",
        "Austrian": "AT",
        "Argentine": "AR",
        "Argentinian": "AR",
        "Argentinean": "AR",
        "Danish": "DK",
        "Japanese": "JP",
        "Chinese": "CN",
        "American": "US",
        "USA": "US",
        "United States": "US",
        "Italian": "IT",
        "Thai": "TH",
        "Belgian": "BE",
        "Swiss": "CH",
        "South African": "ZA",
        "New Zealander": "NZ",
        "Irish": "IE",
        "Swedish": "SE",
        "Portuguese": "PT",
        "Russian": "RU",
        "Indian": "IN",
        "Malaysian": "MY",
        "Hungarian": "HU",
        "Czech": "CZ",
        "Polish": "PL",
        "Colombian": "CO",
        "Venezuelan": "VE",
        "Uruguayan": "UY",
        "Chilean": "CL",
        "Indonesian": "ID",
        "East German": "DE",
        "West German": "DE",
        "Rhodesian": "ZW",
        "Liechtensteiner": "LI",
        "Czechoslovak": "CZ"
    }
    
    # Verificar correspondência exata primeiro
    if nationality_text in nationality_map:
        return nationality_map[nationality_text]
    
    # Lista de termos para verificar
    nationality_terms = {
        "GB": ["British", "England", "UK", "United Kingdom", "Scotland", "Welsh", "Northern Ireland"],
        "US": ["American", "USA", "United States"],
        "DE": ["German", "Germany"],
        "FR": ["French", "France"],
        "IT": ["Italian", "Italy"],
        "JP": ["Japanese", "Japan"],
        "BR": ["Brazilian", "Brazil"],
        "ES": ["Spanish", "Spain"],
        "CA": ["Canadian", "Canada"],
        "FI": ["Finnish", "Finland"],
        "AT": ["Austrian", "Austria"],
        "AU": ["Australian", "Australia"],
        "NL": ["Dutch", "Netherlands", "Holland"],
        "CH": ["Swiss", "Switzerland"],
        "BE": ["Belgian", "Belgium"],
        "SE": ["Swedish", "Sweden"],
        "PT": ["Portuguese", "Portugal"],
        "AR": ["Argentine", "Argentinian", "Argentinean", "Argentina"],
        "MC": ["Monégasque", "Monaco", "Monacan"],
        "NZ": ["New Zealand", "New Zealander", "Kiwi"],
        "ZA": ["South Africa", "South African"],
        "DK": ["Danish", "Denmark"],
        "MX": ["Mexican", "Mexico"],
        "CO": ["Colombian", "Colombia"],
        "VE": ["Venezuelan", "Venezuela"],
        "IE": ["Irish", "Ireland"],
        "HU": ["Hungarian", "Hungary"],
        "PL": ["Polish", "Poland"],
        "RU": ["Russian", "Russia"],
        "IN": ["Indian", "India"],
        "CZ": ["Czech", "Czechoslovak", "Czechoslovakia", "Czech Republic"],
        "MY": ["Malaysian", "Malaysia"],
        "UY": ["Uruguayan", "Uruguay"],
        "CL": ["Chilean", "Chile"],
        "CN": ["Chinese", "China"],
        "TH": ["Thai", "Thailand"],
        "ID": ["Indonesian", "Indonesia"],
        "ZW": ["Rhodesian", "Rhodesia", "Zimbabwe", "Zimbabwean"],
        "LI": ["Liechtensteiner", "Liechtenstein"]
    }
    
    # Verificar cada termo
    nationality_lower = nationality_text.lower()
    for code, terms in nationality_terms.items():
        for term in terms:
            if term.lower() in nationality_lower:
                return code
    
    # Casos específicos comuns
    if "Monaco" in nationality_text:
        return "MC"
    
    # Imprimir nacionalidades não identificadas para debug
    print(f"Nacionalidade não identificada: {nationality_text}")
    
    # Retornar um valor padrão se não for encontrado
    return "Unknown"

# Executar a extração
drivers_data = extract_drivers_data()

# Organizar dados em formato JSON
output_data = {"drivers": drivers_data}

# Salvar dados em JSON
with open(output_json_path, 'w', encoding='utf-8') as file:
    json.dump(output_data, file, ensure_ascii=False, indent=2)

print(f"Dados salvos em: {output_json_path}")
print(f"Total de pilotos extraídos: {len(drivers_data)}")
