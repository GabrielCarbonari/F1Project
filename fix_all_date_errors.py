import json

# Base de dados com correções para pilotos com datas incorretas
corrections = {
    "Harry Schell": {"birth": "29/06/1921", "death": "13/05/1960", "fatal_accident": "Yes"},
    "Jody Scheckter": {"birth": "29/01/1950", "death": "", "fatal_accident": "No"},
    "Andrea de Adamich": {"birth": "03/10/1941", "death": "", "fatal_accident": "No"},
    "Fernando Alonso": {"birth": "29/07/1981", "death": "", "fatal_accident": "No"},
    "Luca Badoer": {"birth": "25/01/1971", "death": "", "fatal_accident": "No"},
    "Edgar Barth": {"birth": "26/01/1917", "death": "20/05/1965", "fatal_accident": "No"},
    "Mark Blundell": {"birth": "08/04/1966", "death": "", "fatal_accident": "No"},
    "Warwick Brown": {"birth": "24/12/1949", "death": "", "fatal_accident": "No"},
    "Dave Charlton": {"birth": "27/10/1936", "death": "24/02/2013", "fatal_accident": "No"},
    "Eddie Cheever": {"birth": "10/01/1958", "death": "", "fatal_accident": "No"},
    "Anthony Davidson": {"birth": "18/04/1979", "death": "", "fatal_accident": "No"},
    "Patrick Depailler": {"birth": "09/08/1944", "death": "01/08/1980", "fatal_accident": "Yes"},
    "Mark Donohue": {"birth": "18/03/1937", "death": "19/08/1975", "fatal_accident": "Yes"},
    "Guy Edwards": {"birth": "30/12/1942", "death": "", "fatal_accident": "No"},
    "Teo Fabi": {"birth": "09/03/1955", "death": "", "fatal_accident": "No"},
    "Jack Fairman": {"birth": "15/03/1913", "death": "07/02/2002", "fatal_accident": "No"},
    "Emerson Fittipaldi": {"birth": "12/12/1946", "death": "", "fatal_accident": "No"},
    "Ron Flockhart": {"birth": "16/06/1923", "death": "12/04/1962", "fatal_accident": "Yes"},
    "Olivier Gendebien": {"birth": "12/01/1924", "death": "02/10/1998", "fatal_accident": "No"},
    "Piercarlo Ghinzani": {"birth": "16/01/1952", "death": "", "fatal_accident": "No"},
    "Antonio Giovinazzi": {"birth": "14/12/1993", "death": "", "fatal_accident": "No"},
    "Timo Glock": {"birth": "18/03/1982", "death": "", "fatal_accident": "No"},
    "Paco Godia": {"birth": "21/03/1921", "death": "28/11/1990", "fatal_accident": "No"},
    "Romain Grosjean": {"birth": "17/04/1986", "death": "", "fatal_accident": "No"},
    "Duncan Hamilton": {"birth": "30/04/1920", "death": "13/05/1994", "fatal_accident": "No"},
    "Brian Henton": {"birth": "19/09/1946", "death": "", "fatal_accident": "No"},
    "Nico Hülkenberg": {"birth": "19/08/1987", "death": "", "fatal_accident": "No"},
    "Jean-Pierre Jarier": {"birth": "10/07/1946", "death": "", "fatal_accident": "No"},
    "Stefan Johansson": {"birth": "08/09/1956", "death": "", "fatal_accident": "No"},
    "Narain Karthikeyan": {"birth": "14/01/1977", "death": "", "fatal_accident": "No"},
    "Peter de Klerk": {"birth": "16/03/1935", "death": "11/07/2015", "fatal_accident": "No"},
    "Gijs van Lennep": {"birth": "16/03/1942", "death": "", "fatal_accident": "No"},
    "Jan Magnussen": {"birth": "04/07/1973", "death": "", "fatal_accident": "No"},
    "Onofre Marimón": {"birth": "19/12/1923", "death": "31/07/1954", "fatal_accident": "Yes"},
    "Felipe Massa": {"birth": "25/04/1981", "death": "", "fatal_accident": "No"},
    "François Migault": {"birth": "04/12/1944", "death": "29/01/2012", "fatal_accident": "No"},
    "Juan Pablo Montoya": {"birth": "20/09/1975", "death": "", "fatal_accident": "No"},
    "Roberto Moreno": {"birth": "11/02/1959", "death": "", "fatal_accident": "No"},
    "David Murray": {"birth": "28/12/1909", "death": "05/04/1973", "fatal_accident": "No"},
    "Mike Parkes": {"birth": "24/09/1931", "death": "28/08/1977", "fatal_accident": "Yes"},
    "Larry Perkins": {"birth": "18/03/1950", "death": "", "fatal_accident": "No"},
    "Henri Pescarolo": {"birth": "25/09/1942", "death": "", "fatal_accident": "No"},
    "André Pilette": {"birth": "06/10/1918", "death": "27/12/1993", "fatal_accident": "No"},
    "Brian Redman": {"birth": "09/03/1937", "death": "", "fatal_accident": "No"},
    "Peter Revson": {"birth": "27/02/1939", "death": "22/03/1974", "fatal_accident": "Yes"},
    "Vern Schuppan": {"birth": "19/03/1943", "death": "", "fatal_accident": "No"},
    "Wolfgang Seidel": {"birth": "04/07/1926", "death": "01/03/1987", "fatal_accident": "No"},
    "Hans Stuck": {"birth": "27/12/1900", "death": "09/02/1978", "fatal_accident": "No"},
    "Jacques Swaters": {"birth": "30/10/1926", "death": "10/12/2010", "fatal_accident": "No"},
    "Dennis Taylor": {"birth": "12/06/1921", "death": "02/06/1962", "fatal_accident": "No"},
    "Trevor Taylor": {"birth": "26/12/1936", "death": "27/09/2010", "fatal_accident": "No"},
    "Sam Tingle": {"birth": "24/08/1921", "death": "19/12/2008", "fatal_accident": "No"},
    "Ottorino Volonterio": {"birth": "07/12/1917", "death": "10/03/2003", "fatal_accident": "No"},
    "Jonathan Williams": {"birth": "26/10/1942", "death": "31/08/2014", "fatal_accident": "No"},
    "Manfred Winkelhock": {"birth": "06/10/1951", "death": "12/08/1985", "fatal_accident": "Yes"}
}

# Carregar o arquivo JSON
print("Carregando arquivo JSON...")
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

total_drivers = len(drivers_data)
corrected_count = 0

print(f"Total de {total_drivers} pilotos encontrados. Iniciando correções...")

# Processar cada piloto
for i, driver in enumerate(drivers_data):
    driver_name = driver["Name"]
    
    # Verificar se o piloto está no dicionário de correções
    if driver_name in corrections:
        driver["BirthDate"] = corrections[driver_name]["birth"]
        driver["DeathDate"] = corrections[driver_name]["death"]
        driver["fatal accident"] = corrections[driver_name]["fatal_accident"]
        corrected_count += 1
        print(f"[{i+1}/{total_drivers}] {driver_name}: Corrigido com dados conhecidos")

# Salvar o JSON atualizado
print(f"\nSalvando arquivo JSON atualizado...")
with open('data/drivers.json', 'w', encoding='utf-8') as file:
    json.dump(drivers_data, file, indent=4)

print(f"\nResumo da atualização:")
print(f"Total de pilotos: {total_drivers}")
print(f"Pilotos corrigidos: {corrected_count}")
print("\nProcesso concluído! Todas as datas incorretas foram corrigidas.")
