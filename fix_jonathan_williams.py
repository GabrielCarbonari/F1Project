import json

# Dados corretos para Jonathan Williams
jonathan_williams_correction = {
    "Name": "Jonathan Williams",
    "Nationality": "United Kingdom",
    "Seasons": "1967",
    "Championships": "0",
    "Race entries": "1",
    "Race starts": "1",
    "Pole positions": "0",
    "Wins": "0",
    "Podiums": "0",
    "Fastest laps": "0",
    "BirthDate": "26/10/1942",
    "DeathDate": "31/08/2014",
    "fatal accident": "No"
}

# Carregar o arquivo drivers.json
print("Carregando arquivo drivers.json...")
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

# Verificar se Jonathan Williams já existe na lista
driver_found = False
for i, driver in enumerate(drivers_data):
    if driver["Name"] == "Jonathan Williams":
        print(f"Atualizando registro existente de Jonathan Williams...")
        drivers_data[i] = jonathan_williams_correction
        driver_found = True
        break

# Se não encontrado, adicionar o registro
if not driver_found:
    print("Adicionando novo registro para Jonathan Williams...")
    drivers_data.append(jonathan_williams_correction)

# Salvar o arquivo atualizado
print("Salvando arquivo drivers.json atualizado...")
with open('data/drivers.json', 'w', encoding='utf-8') as file:
    json.dump(drivers_data, file, indent=4, ensure_ascii=False)

print("\nAtualização concluída com sucesso!")
print(f"Dados de Jonathan Williams atualizados:")
print(f"Data de Nascimento: {jonathan_williams_correction['BirthDate']}")
print(f"Data de Falecimento: {jonathan_williams_correction['DeathDate']}")
print(f"Acidente Fatal: {jonathan_williams_correction['fatal accident']}")
