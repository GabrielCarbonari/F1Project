import json

# Carregar o arquivo JSON
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

# Procurar e atualizar Adolfo Schwelm Cruz
for driver in drivers_data:
    if driver["Name"] == "Adolfo Schwelm Cruz":
        print(f"Encontrado Adolfo Schwelm Cruz:")
        print(f"  Data de nascimento atual: {driver['BirthDate']}")
        print(f"  Data de morte atual: {driver['DeathDate']}")
        
        # Atualizar a data de morte
        driver["DeathDate"] = "10/06/2012"
        print(f"  Nova data de morte: {driver['DeathDate']}")
        break

# Salvar o arquivo JSON atualizado
with open('data/drivers.json', 'w', encoding='utf-8') as file:
    json.dump(drivers_data, file, indent=4)

print("\nArquivo JSON atualizado com sucesso!")
