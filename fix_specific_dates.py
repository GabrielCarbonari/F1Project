import json

# Dicionário com datas corretas para pilotos específicos
correct_dates = {
    "Alan Brown": {"birth": "20/11/1919", "death": "20/01/2004"},
    "Andrea Chiesa": {"birth": "06/05/1964", "death": ""},
    "Carlos Reutemann": {"birth": "12/04/1942", "death": "07/07/2021"},
    "Jean-Pierre Jabouille": {"birth": "01/10/1942", "death": "02/02/2023"},
    "Duncan Hamilton": {"birth": "30/04/1920", "death": "13/05/1994"},
    "Adrian Sutil": {"birth": "11/01/1983", "death": ""},
    "Hans Stuck": {"birth": "27/12/1900", "death": "09/02/1978"},
    "Hans-Joachim Stuck": {"birth": "01/01/1951", "death": ""},
    "Dennis Taylor": {"birth": "20/01/1929", "death": "02/06/1991"},
    "Juan Manuel Fangio": {"birth": "24/06/1911", "death": "17/07/1995"},
    "Ayrton Senna": {"birth": "21/03/1960", "death": "01/05/1994"},
    "Michael Schumacher": {"birth": "03/01/1969", "death": ""},
    "Lewis Hamilton": {"birth": "07/01/1985", "death": ""},
    "Sebastian Vettel": {"birth": "03/07/1987", "death": ""},
    "Fernando Alonso": {"birth": "29/07/1981", "death": ""},
    "Max Verstappen": {"birth": "30/09/1997", "death": ""},
    "Charles Leclerc": {"birth": "16/10/1997", "death": ""},
    "Nico Rosberg": {"birth": "27/06/1985", "death": ""},
    "Kimi Räikkönen": {"birth": "17/10/1979", "death": ""},
    "Jenson Button": {"birth": "19/01/1980", "death": ""},
    "Mika Häkkinen": {"birth": "28/09/1968", "death": ""},
    "Damon Hill": {"birth": "17/09/1960", "death": ""},
    "Jacques Villeneuve": {"birth": "09/04/1971", "death": ""},
    "David Coulthard": {"birth": "27/03/1971", "death": ""},
    "Rubens Barrichello": {"birth": "23/05/1972", "death": ""},
    "Pastor Maldonado": {"birth": "09/03/1985", "death": ""},
    "Timo Glock": {"birth": "18/03/1982", "death": ""},
    "Bruno Senna": {"birth": "15/10/1983", "death": ""},
    "Heikki Kovalainen": {"birth": "19/10/1981", "death": ""},
    "Kamui Kobayashi": {"birth": "13/09/1986", "death": ""},
    "Emerson Fittipaldi": {"birth": "12/12/1946", "death": ""},
    "Nelson Piquet": {"birth": "17/08/1952", "death": ""},
    "Wilson Fittipaldi": {"birth": "25/12/1943", "death": ""}
}

# Função para verificar se uma data é potencialmente inválida
def is_date_invalid(date_str):
    if not date_str:
        return False
    
    # Casos óbvios de datas incorretas
    if "and" in date_str or "to" in date_str:
        return True
    
    # Verificar se é uma data no formato correto (DD/MM/YYYY)
    parts = date_str.split("/")
    if len(parts) != 3:
        return True
    
    try:
        day, month, year = map(int, parts)
        
        # Verificar limites razoáveis
        current_year = 2025
        if year < 1850 or year > current_year:
            return True
            
        if month < 1 or month > 12:
            return True
            
        days_in_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if day < 1 or day > days_in_month[month]:
            return True
            
        return False
    except:
        return True

# Carregar o arquivo JSON
print("Carregando arquivo drivers.json...")
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Contador de correções
birth_corrections = 0
death_corrections = 0

# Processar cada piloto
print("Aplicando correções...")
for driver in drivers:
    name = driver["Name"]
    
    # Caso 1: Piloto com datas conhecidas corrigidas
    if name in correct_dates:
        old_birth = driver.get("BirthDate", "")
        old_death = driver.get("DeathDate", "")
        
        driver["BirthDate"] = correct_dates[name]["birth"]
        driver["DeathDate"] = correct_dates[name]["death"]
        
        if old_birth != correct_dates[name]["birth"]:
            birth_corrections += 1
            print(f"Corrigida data de nascimento de {name}: {old_birth} -> {correct_dates[name]['birth']}")
            
        if old_death != correct_dates[name]["death"]:
            death_corrections += 1
            print(f"Corrigida data de morte de {name}: {old_death} -> {correct_dates[name]['death']}")
    
    # Caso 2: Detectar e corrigir datas obviamente inválidas
    else:
        # Verificar data de nascimento
        if "BirthDate" in driver and is_date_invalid(driver["BirthDate"]):
            print(f"Encontrada data de nascimento inválida para {name}: {driver['BirthDate']}")
            # Definir como vazia para ser corrigida depois
            driver["BirthDate"] = ""
            birth_corrections += 1
        
        # Verificar data de morte
        if "DeathDate" in driver and is_date_invalid(driver["DeathDate"]):
            print(f"Encontrada data de morte inválida para {name}: {driver['DeathDate']}")
            # Definir como vazia para ser corrigida depois
            driver["DeathDate"] = ""
            death_corrections += 1

# Salvar o arquivo atualizado
print("Salvando arquivo atualizado...")
with open('data/drivers.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, ensure_ascii=False, indent=4)

print("\nCorreções concluídas!")
print(f"Datas de nascimento corrigidas: {birth_corrections}")
print(f"Datas de morte corrigidas: {death_corrections}")
print("Arquivo drivers.json atualizado com sucesso.")
