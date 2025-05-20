import json

# Correções específicas solicitadas
specific_corrections = {
    "Robert Doornbos": "Netherlands",
    "Nikita Mazepin": "Russia",
    "Bertrand Gachot": "Belgium",
    "Gary Hocking": "Zimbabwe"
}

# Carregar o arquivo JSON
print("Carregando arquivo JSON...")
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

total_drivers = len(drivers_data)
updates_count = 0

print(f"Total de {total_drivers} pilotos encontrados. Aplicando correções específicas...")

# Processar cada piloto
for i, driver in enumerate(drivers_data):
    if "Name" in driver and driver["Name"] in specific_corrections:
        original_nationality = driver["Nationality"]
        new_nationality = specific_corrections[driver["Name"]]
        
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
print("\nProcesso concluído! As nacionalidades específicas foram atualizadas.")
