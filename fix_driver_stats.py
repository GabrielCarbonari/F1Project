import json
import re

# Função para verificar se um número é maior que outro (com tratamento para valores não-numéricos)
def is_likely_swapped(val1, val2):
    try:
        num1 = int(val1)
        num2 = int(val2)
        # Se o número de poles for maior que o número de pódios, provavelmente estão trocados
        # (quase sempre um piloto tem mais pódios que poles)
        return num1 > num2
    except:
        return False

# Carregar o arquivo JSON
with open('data/drivers.json', 'r', encoding='utf-8') as f:
    drivers = json.load(f)

# Contadores para estatísticas
corrected_seasons = 0
corrected_stats = 0

# Processar cada piloto
for driver in drivers:
    # 1. Corrigir o formato das temporadas (trocar en dash "–" por hífen "-")
    if "Seasons" in driver and driver["Seasons"]:
        old_seasons = driver["Seasons"]
        new_seasons = old_seasons.replace("–", "-")
        if old_seasons != new_seasons:
            driver["Seasons"] = new_seasons
            corrected_seasons += 1
    
    # 2. Verificar se as estatísticas estão consistentes
    # Normalmente: Pódios >= Vitórias >= Poles (na maioria dos casos)
    poles = driver.get("Pole positions", "0")
    wins = driver.get("Wins", "0")
    podiums = driver.get("Podiums", "0")
    
    # Se o número de poles for maior que o número de pódios, provavelmente estão trocados
    if is_likely_swapped(poles, podiums):
        driver["Pole positions"], driver["Podiums"] = podiums, poles
        corrected_stats += 1
    
    # Se o número de vitórias for maior que o número de pódios, provavelmente estão trocados
    if is_likely_swapped(wins, podiums):
        driver["Wins"], driver["Podiums"] = podiums, wins
        corrected_stats += 1

# Salvar o arquivo corrigido
with open('data/drivers_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(drivers, f, ensure_ascii=False, indent=4)

print(f"Temporadas corrigidas: {corrected_seasons}")
print(f"Estatísticas potencialmente corrigidas: {corrected_stats}")
print("Arquivo salvo como 'data/drivers_fixed.json'")
