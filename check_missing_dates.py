import json

def count_missing_dates():
    # Carregar o arquivo JSON com os pilotos
    try:
        with open('data/drivers.json', 'r', encoding='utf-8') as f:
            drivers = json.load(f)
        print(f"Total de pilotos: {len(drivers)}")
        
        # Contar pilotos com datas
        with_birth_date = 0
        with_death_date = 0
        
        # Contar pilotos sem datas
        without_birth_date = 0
        without_death_date = 0
        
        # Pilotos com datas inválidas
        invalid_birth_date = 0
        
        for driver in drivers:
            # Verificar data de nascimento
            if "BirthDate" in driver and driver["BirthDate"] and driver["BirthDate"].strip():
                if "and" in driver["BirthDate"] or len(driver["BirthDate"]) <= 4:
                    invalid_birth_date += 1
                else:
                    with_birth_date += 1
            else:
                without_birth_date += 1
            
            # Verificar data de morte
            if "DeathDate" in driver and driver["DeathDate"] and driver["DeathDate"].strip():
                with_death_date += 1
            else:
                without_death_date += 1
        
        print(f"\nPilotos com data de nascimento: {with_birth_date}")
        print(f"Pilotos com data de nascimento inválida: {invalid_birth_date}")
        print(f"Pilotos sem data de nascimento: {without_birth_date}")
        print(f"Total pilotos faltando data de nascimento: {without_birth_date + invalid_birth_date}")
        
        print(f"\nPilotos com data de morte: {with_death_date}")
        print(f"Pilotos sem data de morte: {without_death_date}")
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    count_missing_dates()
