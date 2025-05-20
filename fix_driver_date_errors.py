import json
import datetime
import re

# Dados corretos para pilotos específicos com erros conhecidos
corrections = {
    "Harry Schell": {"birth": "29/06/1921", "death": "13/05/1960", "fatal_accident": "Yes"},
    "Jody Scheckter": {"birth": "29/01/1950", "death": "", "fatal_accident": "No"},
    # Adicione mais correções conforme necessário
}

def check_date_format(date_str):
    """Verifica se a data está no formato DD/MM/YYYY"""
    if not date_str:
        return True
    
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    return bool(re.match(pattern, date_str))

def is_date_logical(birth_date, death_date, seasons):
    """Verifica se as datas são logicamente consistentes"""
    if not birth_date:
        return False
    
    try:
        birth_year = int(birth_date.split('/')[-1])
        
        # Verificar se o ano de nascimento é razoável (entre 1880 e 2010)
        if birth_year < 1880 or birth_year > 2010:
            return False
        
        # Se houver data de morte, verificar se é posterior ao nascimento
        if death_date:
            death_year = int(death_date.split('/')[-1])
            if death_year <= birth_year:
                return False
        
        # Se houver temporadas, verificar se a primeira temporada é posterior ao nascimento
        if seasons and '-' in seasons:
            first_season = int(seasons.split('-')[0])
            if birth_year > first_season:
                return False
            
            # Verificar se a primeira temporada é pelo menos 15 anos após o nascimento
            if first_season < birth_year + 15:
                return False
        
        return True
    except Exception as e:
        print(f"Erro ao verificar datas: {e}")
        return False

def main():
    # Carregar o arquivo JSON
    print("Carregando arquivo JSON...")
    with open('data/drivers.json', 'r', encoding='utf-8') as file:
        drivers_data = json.load(file)
    
    total_drivers = len(drivers_data)
    corrected_count = 0
    errors_found = []
    
    # Verificar e corrigir erros
    for i, driver in enumerate(drivers_data):
        driver_name = driver["Name"]
        birth_date = driver.get("BirthDate", "")
        death_date = driver.get("DeathDate", "")
        seasons = driver.get("Seasons", "")
        
        # Verificar se o piloto está no dicionário de correções
        if driver_name in corrections:
            driver["BirthDate"] = corrections[driver_name]["birth"]
            driver["DeathDate"] = corrections[driver_name]["death"]
            driver["fatal accident"] = corrections[driver_name]["fatal_accident"]
            corrected_count += 1
            print(f"[{i+1}/{total_drivers}] {driver_name}: Corrigido com dados conhecidos")
            continue
        
        # Verificar formato das datas
        if not check_date_format(birth_date) or not check_date_format(death_date):
            errors_found.append(f"{driver_name}: Formato de data inválido - Nascimento: {birth_date}, Morte: {death_date}")
            continue
        
        # Verificar consistência lógica das datas
        if not is_date_logical(birth_date, death_date, seasons):
            errors_found.append(f"{driver_name}: Datas ilógicas - Nascimento: {birth_date}, Morte: {death_date}, Temporadas: {seasons}")
            continue
    
    # Salvar o JSON atualizado
    print(f"\nSalvando arquivo JSON atualizado...")
    with open('data/drivers.json', 'w', encoding='utf-8') as file:
        json.dump(drivers_data, file, indent=4)
    
    print(f"\nResumo da verificação:")
    print(f"Total de pilotos: {total_drivers}")
    print(f"Pilotos corrigidos: {corrected_count}")
    
    if errors_found:
        print("\nErros encontrados que precisam de correção manual:")
        for error in errors_found:
            print(f"- {error}")
    
    print("\nProcesso concluído!")

if __name__ == "__main__":
    main()
