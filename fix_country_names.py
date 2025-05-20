import json

def normalize_country_name(country_name):
    """Normaliza os nomes de países conforme especificado."""
    if not country_name:
        return ""
    
    # Converter West Germany e East Germany para Germany
    if "West Germany" in country_name or "East Germany" in country_name:
        return country_name.replace("West Germany", "Germany").replace("East Germany", "Germany")
    
    # Converter Rhodesia para Zimbabwe
    if "Rhodesia" in country_name:
        return country_name.replace("Rhodesia", "Zimbabwe")
    
    return country_name

# Carregar o arquivo JSON
print("Carregando arquivo JSON...")
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

total_drivers = len(drivers_data)
updates_count = 0

print(f"Total de {total_drivers} pilotos encontrados. Iniciando correções de países...")

# Processar cada piloto
for i, driver in enumerate(drivers_data):
    if "Nationality" in driver:
        original_nationality = driver["Nationality"]
        new_nationality = normalize_country_name(original_nationality)
        
        if original_nationality != new_nationality:
            driver["Nationality"] = new_nationality
            updates_count += 1
            print(f"[{i+1}/{total_drivers}] {driver['Name']}: {original_nationality} -> {new_nationality}")

# Salvar o JSON atualizado
print(f"\nSalvando arquivo JSON atualizado...")
with open('data/drivers.json', 'w', encoding='utf-8') as file:
    json.dump(drivers_data, file, indent=4, ensure_ascii=False)

print(f"\nResumo da atualização:")
print(f"Total de pilotos: {total_drivers}")
print(f"Nacionalidades corrigidas: {updates_count}")
print("\nProcesso concluído! Todas as nacionalidades foram normalizadas.")
