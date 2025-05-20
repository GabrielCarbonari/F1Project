#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar drivers.json com dados corretos da Wikipedia
"""

import os
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Caminho para os arquivos
WIKI_FILE = os.path.expanduser("~/Desktop/List of Formula One drivers - Wikipedia.html")
DRIVERS_JSON = "data/drivers.json"
UPDATED_DRIVERS_JSON = "data/drivers_updated.json"

def parse_date(date_str):
    """Converte uma string de data para formato consistente."""
    if not date_str or date_str == "Unknown" or "?" in date_str:
        return ""
    
    # Limpar qualquer texto entre parênteses
    date_str = re.sub(r'\([^)]*\)', '', date_str).strip()
    
    # Tentar vários formatos de data
    formats = [
        "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d %B %Y", 
        "%B %d, %Y", "%d.%m.%Y", "%Y"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            continue
    
    # Se ainda não conseguiu parsear, tentar extrair apenas o ano
    year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
    if year_match:
        year = year_match.group(0)
        return f"01/01/{year}"  # Usar 1º de janeiro como padrão
    
    return date_str  # Retornar a string original se falhar tudo

def clean_stat_value(value):
    """Limpa valores estatísticos com problemas."""
    if not value or value in ["Unknown", "N/A", "–", "-"]:
        return "0"
    
    # Converter para string
    value_str = str(value).strip()
    
    # Remover parênteses, colchetes e seu conteúdo
    value_str = re.sub(r'\[\d+\]|\(\d+\)', '', value_str)
    
    # Remover pontos extras
    value_str = re.sub(r'\.\.+', '', value_str).rstrip('.')
    
    # Extrair apenas números
    num_match = re.match(r'^(\d+)', value_str)
    if num_match:
        return num_match.group(1)
    
    # Se ficar vazio após limpeza, usar '0'
    if not value_str.strip():
        return "0"
    
    return value_str.strip()

def extract_drivers_from_wikipedia():
    """Extrai dados de pilotos do arquivo HTML da Wikipedia."""
    print(f"Lendo arquivo Wikipedia de {WIKI_FILE}")
    
    try:
        with open(WIKI_FILE, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except Exception as e:
        print(f"Erro ao ler arquivo Wikipedia: {e}")
        return {}
    
    soup = BeautifulSoup(html_content, 'html.parser')
    drivers_data = {}
    
    # Encontrar a tabela principal de pilotos
    main_table = soup.find('table', {'class': 'wikitable'})
    if not main_table:
        print("Tabela principal não encontrada no HTML")
        return {}
    
    # Processar linhas da tabela
    rows = main_table.find_all('tr')
    for row in rows[1:]:  # Pular o cabeçalho
        cells = row.find_all(['td', 'th'])
        if len(cells) < 8:  # Verificar se há células suficientes
            continue
        
        # Extrair dados básicos
        try:
            name_cell = cells[0]
            name = name_cell.get_text().strip()
            
            # Colunas da tabela Wikipedia
            nationality = cells[1].get_text().strip()
            seasons = cells[2].get_text().strip()
            championships = clean_stat_value(cells[3].get_text().strip())
            entries = clean_stat_value(cells[4].get_text().strip())
            starts = clean_stat_value(cells[5].get_text().strip())
            poles = clean_stat_value(cells[6].get_text().strip())
            wins = clean_stat_value(cells[7].get_text().strip())
            
            # Dados adicionais se disponíveis
            podiums = "0"
            fastest_laps = "0"
            
            if len(cells) > 8:
                podiums = clean_stat_value(cells[8].get_text().strip())
            
            if len(cells) > 9:
                fastest_laps = clean_stat_value(cells[9].get_text().strip())
            
            # Verificar links para data de nascimento/morte
            birth_date = ""
            death_date = ""
            
            # Tentar extrair datas de links ou textos
            links = name_cell.find_all('a')
            for link in links:
                title = link.get('title', '')
                if "born" in title.lower():
                    match = re.search(r'born\s+(.*?)(?:\)|;|$)', title)
                    if match:
                        birth_date = parse_date(match.group(1).strip())
                
                if "died" in title.lower():
                    match = re.search(r'died\s+(.*?)(?:\)|;|$)', title)
                    if match:
                        death_date = parse_date(match.group(1).strip())
            
            # Criar entrada do piloto
            driver_data = {
                "Name": name,
                "Nationality": nationality.replace('[50]', '').strip(),  # Corrigir bug específico
                "Seasons": seasons,
                "Championships": championships,
                "Race entries": entries,
                "Race starts": starts,
                "Pole positions": poles,
                "Wins": wins,
                "Podiums": podiums,
                "Fastest laps": fastest_laps,
                "BirthDate": birth_date,
                "DeathDate": death_date
            }
            
            # Armazenar usando o nome como chave
            drivers_data[name] = driver_data
            
        except Exception as e:
            print(f"Erro ao processar piloto: {e}")
            continue
    
    print(f"Extraídos {len(drivers_data)} pilotos da Wikipedia")
    return drivers_data

def update_drivers_json():
    """Atualiza o arquivo drivers.json com dados da Wikipedia."""
    try:
        # Carregar dados existentes
        with open(DRIVERS_JSON, 'r', encoding='utf-8') as file:
            existing_drivers = json.load(file)
        
        print(f"Carregados {len(existing_drivers)} pilotos do arquivo existente")
        
        # Extrair dados da Wikipedia
        wiki_drivers = extract_drivers_from_wikipedia()
        
        # Lista para armazenar drivers atualizados
        updated_drivers = []
        
        # Atualizar cada piloto existente
        for driver in existing_drivers:
            driver_name = driver.get("Name", "")
            
            # Se o piloto existe nos dados da Wikipedia, atualizar estatísticas
            if driver_name in wiki_drivers:
                wiki_data = wiki_drivers[driver_name]
                
                # Manter a imagem existente
                image = driver.get("image", "")
                if image:
                    wiki_data["image"] = image
                
                # Atualizar datas apenas se não existirem ou forem inválidas
                if not driver.get("BirthDate") or "?" in driver.get("BirthDate", ""):
                    pass  # Usa a data da Wikipedia já definida
                else:
                    wiki_data["BirthDate"] = driver.get("BirthDate")
                
                if not driver.get("DeathDate") or "?" in driver.get("DeathDate", ""):
                    pass  # Usa a data da Wikipedia já definida
                else:
                    wiki_data["DeathDate"] = driver.get("DeathDate")
                
                # Adicionar o driver atualizado
                updated_drivers.append(wiki_data)
            else:
                # Limpar estatísticas existentes
                cleaned_driver = {
                    "Name": driver_name,
                    "Nationality": driver.get("Nationality", "").replace('[50]', '').strip(),
                    "Seasons": driver.get("Seasons", ""),
                    "Championships": clean_stat_value(driver.get("Championships", "0")),
                    "Race entries": clean_stat_value(driver.get("Race entries", "0")),
                    "Race starts": clean_stat_value(driver.get("Race starts", "0")),
                    "Pole positions": clean_stat_value(driver.get("Pole positions", "0")),
                    "Wins": clean_stat_value(driver.get("Wins", "0")),
                    "Podiums": clean_stat_value(driver.get("Podiums", "0")),
                    "Fastest laps": clean_stat_value(driver.get("Fastest laps", "0")),
                    "BirthDate": driver.get("BirthDate", ""),
                    "DeathDate": driver.get("DeathDate", "")
                }
                
                # Manter a imagem existente
                image = driver.get("image", "")
                if image:
                    cleaned_driver["image"] = image
                
                updated_drivers.append(cleaned_driver)
        
        # Salvar os dados atualizados
        with open(UPDATED_DRIVERS_JSON, 'w', encoding='utf-8') as file:
            json.dump(updated_drivers, file, ensure_ascii=False, indent=4)
        
        print(f"Dados atualizados salvos em {UPDATED_DRIVERS_JSON}")
        return True
    
    except Exception as e:
        print(f"Erro ao atualizar drivers.json: {e}")
        return False

def main():
    """Função principal."""
    print("Iniciando atualização de dados dos pilotos...")
    start_time = time.time()
    
    success = update_drivers_json()
    
    end_time = time.time()
    duration = end_time - start_time
    
    if success:
        print(f"Atualização concluída com sucesso em {duration:.2f} segundos!")
    else:
        print("Atualização falhou")

if __name__ == "__main__":
    main()
