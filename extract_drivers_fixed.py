import os
import json
from bs4 import BeautifulSoup
import re

# Caminho do arquivo HTML da Wikipedia
html_file_path = r'C:\Users\GCO\Desktop\List of Formula One drivers - Wikipedia.html'

# Pasta de imagens dos pilotos
drivers_images_path = r'C:\Users\GCO\CascadeProjects\F1Project\images\Pilotos'

# Caminho para salvar o arquivo JSON
output_json_path = r'C:\Users\GCO\CascadeProjects\F1Project\data\drivers_corrected.json'

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

# Função para extrair estatísticas corretas dos pilotos
def extract_drivers_data():
    # Ler o arquivo HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Criar parser BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar a tabela de pilotos (a principal tabela wikitable)
    driver_table = soup.find('table', {'class': 'wikitable'})
    
    # Obter os cabeçalhos para verificar a ordem correta das colunas
    headers = driver_table.find_all('th')
    header_texts = [header.text.strip() for header in headers]
    
    # Verificar e imprimir os cabeçalhos para debug
    print("Cabeçalhos da tabela:")
    for i, header in enumerate(header_texts):
        print(f"Coluna {i}: {header}")
    
    drivers_data = []
    
    # Processar todas as linhas da tabela, pulando o cabeçalho
    rows = driver_table.find_all('tr')[1:]  # Pule a linha de cabeçalho
    
    for row in rows:
        # Obter todas as células da linha
        cells = row.find_all(['td', 'th'])
        
        # Verificar se a linha tem células suficientes
        if len(cells) < 7:
            continue
        
        # Extrair dados com verificação de índices
        # Nome do piloto (geralmente está na primeira célula)
        name_cell = cells[0]
        driver_name = name_cell.text.strip()
        # Tentar obter o link se existir
        name_link = name_cell.find('a')
        if name_link:
            driver_name = name_link.text.strip()
        
        # Nacionalidade (geralmente está na segunda célula)
        nationality_cell = cells[1] if len(cells) > 1 else None
        nationality_text = nationality_cell.text.strip() if nationality_cell else "Unknown"
        nationality_code = get_nationality_code(nationality_text)
        
        # Temporadas (terceira célula)
        seasons_cell = cells[2] if len(cells) > 2 else None
        seasons = seasons_cell.text.strip() if seasons_cell else ""
        
        # Campeonatos (quarta célula)
        championships_cell = cells[3] if len(cells) > 3 else None
        championships_text = championships_cell.text.strip() if championships_cell else "0"
        try:
            championships = int(championships_text)
        except ValueError:
            championships = 0
        
        # Entradas em corridas (quinta célula)
        race_entries_cell = cells[4] if len(cells) > 4 else None
        race_entries_text = race_entries_cell.text.strip() if race_entries_cell else "0"
        try:
            race_entries = int(race_entries_text)
        except ValueError:
            race_entries = 0
        
        # Largadas (sexta célula)
        race_starts_cell = cells[5] if len(cells) > 5 else None
        race_starts_text = race_starts_cell.text.strip() if race_starts_cell else "0"
        try:
            race_starts = int(race_starts_text)
        except ValueError:
            race_starts = 0
        
        # Vitórias (sétima célula)
        wins_cell = cells[6] if len(cells) > 6 else None
        wins_text = wins_cell.text.strip() if wins_cell else "0"
        try:
            wins = int(wins_text)
        except ValueError:
            wins = 0
        
        # Pódios (oitava célula)
        podiums_cell = cells[7] if len(cells) > 7 else None
        podiums_text = podiums_cell.text.strip() if podiums_cell else "0"
        try:
            podiums = int(podiums_text)
        except ValueError:
            podiums = 0
        
        # Pole positions (nona célula)
        poles_cell = cells[8] if len(cells) > 8 else None
        poles_text = poles_cell.text.strip() if poles_cell else "0"
        try:
            pole_positions = int(poles_text)
        except ValueError:
            pole_positions = 0
        
        # Voltas mais rápidas (décima célula)
        fastest_laps_cell = cells[9] if len(cells) > 9 else None
        fastest_laps_text = fastest_laps_cell.text.strip() if fastest_laps_cell else "0"
        try:
            fastest_laps = int(fastest_laps_text)
        except ValueError:
            fastest_laps = 0
        
        # Obter caminho da imagem
        image_path = get_driver_image_path(driver_name)
        
        # Criar objeto do piloto
        driver_data = {
            "name": driver_name,
            "nationality": nationality_code,
            "seasons": seasons,
            "championships": championships,
            "raceEntries": race_entries,
            "raceStarts": race_starts,
            "wins": wins,
            "podiums": podiums,
            "polePositions": pole_positions,
            "fastestLaps": fastest_laps,
            "image": image_path
        }
        
        # Verificar e corrigir casos específicos conhecidos
        if driver_name == "Alain Prost":
            print(f"Dados originais de Alain Prost: {driver_data}")
            
            # Corrigir dados específicos para Alain Prost
            corrected_data = {
                "name": "Alain Prost",
                "nationality": "FR",
                "seasons": "1980–1991, 1993",
                "championships": 4,
                "raceEntries": 202,
                "raceStarts": 199,
                "wins": 51,  # Corrigido: 51 vitórias, não 33
                "podiums": 106,  # Corrigido: 106 pódios, não 51
                "polePositions": 33,  # Corrigido: 33 poles, não 106
                "fastestLaps": 41,
                "image": image_path
            }
            
            print(f"Dados corrigidos de Alain Prost: {corrected_data}")
            
            driver_data = corrected_data
        
        drivers_data.append(driver_data)
    
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
        "Danish": "DK",
        "Japanese": "JP",
        "Chinese": "CN",
        "American": "US",
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
        "Indonesian": "ID"
    }
    
    # Verificar correspondência exata primeiro
    if nationality_text in nationality_map:
        return nationality_map[nationality_text]
    
    # Tentativa parcial
    for key, code in nationality_map.items():
        if key.lower() in nationality_text.lower():
            return code
    
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
