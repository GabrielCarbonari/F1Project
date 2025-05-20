import json
import datetime

# Carregar dados dos pilotos
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Lista de pilotos que sabemos estarem vivos (ativos recentemente ou aposentados há pouco tempo)
known_living_drivers = [
    "Adrian Sutil",
    "Fernando Alonso",
    "Lewis Hamilton",
    "Sebastian Vettel",
    "Max Verstappen",
    "Charles Leclerc",
    "Sergio Perez",
    "Daniel Ricciardo",
    "Lando Norris",
    "Oscar Piastri",
    "Carlos Sainz Jr.",
    "Pierre Gasly",
    "Esteban Ocon",
    "Kevin Magnussen",
    "Alexander Albon",
    "Valtteri Bottas",
    "Lance Stroll",
    "Nico Hulkenberg",
    "Logan Sargeant",
    "Zhou Guanyu",
    "George Russell",
    "Yuki Tsunoda",
    "Liam Lawson",
    "Robert Kubica",
    "Kimi Raikkonen",
    "Romain Grosjean",
    "Marcus Ericsson",
    "Brendon Hartley",
    "Esteban Gutierrez",
    "Jean-Eric Vergne",
    "Kamui Kobayashi",
    "Bruno Senna",
    "Timo Glock",
    "Heikki Kovalainen",
    "Vitaly Petrov",
    "Jaime Alguersuari",
    "Lucas di Grassi",
    "Pastor Maldonado",
    "Kazuki Nakajima",
    "Anthony Davidson",
    "Takuma Sato",
    "Juan Pablo Montoya"
]

# Verificar pilotos
errors_found = 0
for driver in drivers:
    name = driver["Name"]
    # Verificar se o piloto tem data de morte mas é conhecido por estar vivo
    if name in known_living_drivers and driver.get("DeathDate") and driver["DeathDate"].strip():
        print(f"ERRO: {name} está marcado como falecido em {driver['DeathDate']}, mas deve estar vivo.")
        errors_found += 1
        # Corrigir o erro
        driver["DeathDate"] = ""
        
    # Verificar outras datas potencialmente problemáticas
    if driver.get("BirthDate") and driver.get("DeathDate") and driver["DeathDate"].strip():
        # Verificar se a data de morte é posterior a 2022 para pilotos recentes (prováveis erros)
        try:
            if "/" in driver["DeathDate"]:
                day, month, year = map(int, driver["DeathDate"].split("/"))
                if year > 2022:
                    print(f"SUSPEITO: {name} tem data de morte futura/improvável: {driver['DeathDate']}")
                    errors_found += 1
                    # Corrigir presumindo que é um erro
                    driver["DeathDate"] = ""
                    
            # Verificar se a data de nascimento é recente (após 1990) mas tem data de morte
            if "/" in driver["BirthDate"]:
                day, month, year = map(int, driver["BirthDate"].split("/"))
                if year > 1990 and driver["DeathDate"].strip():
                    print(f"SUSPEITO: {name} nasceu em {driver['BirthDate']} e está marcado como falecido em {driver['DeathDate']} (improvável)")
                    errors_found += 1
                    # Corrigir presumindo que é um erro
                    driver["DeathDate"] = ""
        except:
            # Ignorar erros de formato de data
            pass

# Se encontrou erros, salvar o arquivo corrigido
if errors_found > 0:
    with open('data/drivers.json', 'w', encoding='utf-8') as f:
        json.dump(drivers, f, ensure_ascii=False, indent=4)
    print(f"\nCorrigidos {errors_found} erros. Arquivo 'data/drivers.json' foi atualizado.")
else:
    print("\nNenhum erro encontrado.")
