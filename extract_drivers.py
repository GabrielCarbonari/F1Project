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

# Função para extrair dados dos pilotos
def extract_drivers_data():
    # Ler o arquivo HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Criar parser BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar a tabela de pilotos
    driver_table = soup.find('table', {'class': 'wikitable'})
    
    drivers_data = []
    
    # Pular a linha de cabeçalho
    rows = driver_table.find_all('tr')[1:]
    
    for row in rows:
        columns = row.find_all('td')
        
        if len(columns) >= 7:  # Verificar se a linha tem colunas suficientes
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
            
            # Extrair vitórias
            wins = columns[6].text.strip()
            try:
                wins = int(wins)
            except:
                wins = 0
            
            # Extrair pódios (se disponível)
            podiums = 0
            if len(columns) > 7:
                podiums_text = columns[7].text.strip()
                try:
                    podiums = int(podiums_text)
                except:
                    podiums = 0
            
            # Extrair pole positions (se disponível)
            pole_positions = 0
            if len(columns) > 8:
                poles_text = columns[8].text.strip()
                try:
                    pole_positions = int(poles_text)
                except:
                    pole_positions = 0
            
            # Extrair voltas mais rápidas (se disponível)
            fastest_laps = 0
            if len(columns) > 9:
                fastest_laps_text = columns[9].text.strip()
                try:
                    fastest_laps = int(fastest_laps_text)
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
                "wins": wins,
                "podiums": podiums,
                "polePositions": pole_positions,
                "fastestLaps": fastest_laps,
                "image": image_path
            }
            
            drivers_data.append(driver)
    
    return drivers_data

# Função para obter o código da nacionalidade a partir do texto
def get_nationality_code(nationality_text):
    nationality_map = {
        "United Kingdom": "GB",
        "Great Britain": "GB",
        "UK": "GB",
        "England": "GB",
        "Italy": "IT",
        "France": "FR",
        "Germany": "DE",
        "Brazil": "BR",
        "Australia": "AU",
        "United States": "US",
        "USA": "US",
        "Argentina": "AR",
        "Spain": "ES",
        "Netherlands": "NL",
        "Belgium": "BE",
        "Monaco": "MC",
        "Austria": "AT",
        "Sweden": "SE",
        "Finland": "FI",
        "Switzerland": "CH",
        "Canada": "CA",
        "Japan": "JP",
        "Mexico": "MX",
        "Portugal": "PT",
        "Ireland": "IE",
        "New Zealand": "NZ",
        "Denmark": "DK",
        "South Africa": "ZA",
        "Thailand": "TH",
        "China": "CN",
        "Malaysia": "MY",
        "Russia": "RU",
        "Poland": "PL",
        "Hungary": "HU",
        "Czech Republic": "CZ",
        "Chile": "CL",
        "Colombia": "CO",
        "Uruguay": "UY",
        "Venezuela": "VE",
        "India": "IN",
        "Indonesia": "ID"
    }
    
    # Limpar o texto (remover "flag" e espaços extras)
    cleaned_text = re.sub(r'flagicon', '', nationality_text).strip()
    
    # Procurar o código de nacionalidade
    for country, code in nationality_map.items():
        if country.lower() in cleaned_text.lower():
            return code
    
    # Retornar nacionalidade desconhecida
    return "UN"

# Executar extração de dados
drivers_data = extract_drivers_data()

# Salvar os dados em JSON
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump({"drivers": drivers_data}, json_file, ensure_ascii=False, indent=2)

print(f"Extração concluída. {len(drivers_data)} pilotos extraídos e salvos em {output_json_path}")
