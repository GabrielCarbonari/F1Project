import json
import requests
import time
import datetime
from bs4 import BeautifulSoup
import re

# Base de dados manual para pilotos difíceis de encontrar automaticamente
manual_database = {
    "Carlo Abate": {"birth": "10/07/1932", "death": "29/04/2019"},
    "Kenny Acheson": {"birth": "27/11/1957", "death": ""},
    "Bob Anderson": {"birth": "19/05/1931", "death": "14/08/1967"},
    "Mario Andretti": {"birth": "28/02/1940", "death": ""},
    "Peter Arundell": {"birth": "08/11/1933", "death": "16/06/2009"},
    "Peter Ashdown": {"birth": "16/10/1934", "death": "25/10/2019"},
    "Bill Aston": {"birth": "29/03/1900", "death": "04/03/1974"},
    "John Barber": {"birth": "22/07/1929", "death": "04/02/2015"},
    "Skip Barber": {"birth": "16/11/1936", "death": ""},
    "Don Beauman": {"birth": "26/07/1928", "death": "09/07/1955"},
    "Tom Belsø": {"birth": "27/08/1942", "death": "11/01/2020"},
    "Georges Berger": {"birth": "14/09/1918", "death": "23/08/1967"},
    "Éric Bernard": {"birth": "24/08/1964", "death": ""},
    "Harry Blanchard": {"birth": "13/06/1929", "death": "31/01/1960"},
    "Michael Bleekemolen": {"birth": "02/10/1949", "death": ""},
    "Alex Blignaut": {"birth": "30/11/1932", "death": "14/01/2001"},
    "Menato Boffa": {"birth": "24/01/1930", "death": "28/09/1996"},
    "Bob Bondurant": {"birth": "27/04/1933", "death": "12/11/2021"},
    "David Brabham": {"birth": "05/09/1965", "death": ""},
    "Bill Brack": {"birth": "20/12/1935", "death": ""},
    "Eric Brandon": {"birth": "18/07/1920", "death": "08/08/1982"},
    "Tom Bridger": {"birth": "24/06/1934", "death": "30/07/1991"},
    "Tony Brise": {"birth": "28/03/1952", "death": "29/11/1975"},
    "Peter Broeker": {"birth": "15/05/1926", "death": "04/11/1980"},
    "Alan Brown": {"birth": "20/11/1919", "death": "20/01/2004"},
    "Warwick Brown": {"birth": "24/12/1949", "death": ""},
    "Ronnie Bucknum": {"birth": "05/04/1936", "death": "23/04/1992"},
    "Roberto Bussinello": {"birth": "04/10/1927", "death": "08/05/1999"},
    "Phil Cade": {"birth": "12/06/1916", "death": "28/08/2001"},
    "John Campbell-Jones": {"birth": "21/01/1930", "death": "22/03/2020"},
    "John Cannon": {"birth": "21/06/1933", "death": "18/10/1999"},
    "Jay Chamberlain": {"birth": "29/12/1925", "death": "01/08/2001"},
    "Alain de Changy": {"birth": "05/02/1922", "death": "05/08/1994"},
    "Pedro Chaves": {"birth": "27/02/1965", "death": ""},
    "Andrea Chiesa": {"birth": "06/05/1964", "death": ""},
    "Johnny Claes": {"birth": "11/08/1916", "death": "03/02/1956"},
    "David Clapham": {"birth": "18/05/1931", "death": "09/02/2005"},
    "Kevin Cogan": {"birth": "31/03/1956", "death": ""},
    "Bernard Collomb": {"birth": "07/10/1930", "death": "19/09/2011"},
    "George Constantine": {"birth": "22/02/1918", "death": "07/01/1968"},
    "John Cordts": {"birth": "23/07/1935", "death": ""},
    "Chris Craft": {"birth": "17/11/1939", "death": "20/02/2021"},
    "Jim Crawford": {"birth": "13/02/1948", "death": "06/08/2002"},
    "Chuck Daigh": {"birth": "29/11/1923", "death": "29/04/2008"},
    "Christian Danner": {"birth": "04/04/1958", "death": ""},
    "Jorge Daponte": {"birth": "05/06/1923", "death": "01/03/1963"},
    "Frank Dochnal": {"birth": "08/10/1920", "death": "07/07/2010"},
    "José Dolhem": {"birth": "26/04/1944", "death": "16/04/1988"},
    "Mark Donohue": {"birth": "18/03/1937", "death": "19/08/1975"},
    "Ken Downing": {"birth": "05/12/1917", "death": "03/05/2004"},
    "Paddy Driver": {"birth": "13/05/1934", "death": ""},
    "Bernard de Dryver": {"birth": "19/09/1952", "death": ""},
    "Johnny Dumfries": {"birth": "26/04/1958", "death": "22/03/2021"},
    "George Eaton": {"birth": "12/11/1945", "death": ""},
    "Paul Emery": {"birth": "12/11/1916", "death": "03/02/1993"},
    "Paul England": {"birth": "28/03/1929", "death": "17/06/2014"},
    "Bob Evans": {"birth": "11/06/1947", "death": ""},
    "Jack Fairman": {"birth": "15/03/1913", "death": "07/02/2002"},
    "Nino Farina": {"birth": "30/10/1906", "death": "30/06/1966"},
    "William Ferguson": {"birth": "28/01/1940", "death": ""},
    "Mike Fisher": {"birth": "13/03/1943", "death": ""},
    "John Fitch": {"birth": "04/08/1917", "death": "31/10/2012"},
    "George Follmer": {"birth": "27/01/1934", "death": ""},
    "Paul Frère": {"birth": "30/01/1917", "death": "23/02/2008"},
    "Patrick Friesacher": {"birth": "26/09/1980", "death": ""},
    "Joe Fry": {"birth": "26/10/1915", "death": "29/07/1950"},
    "Fred Gamble": {"birth": "17/03/1932", "death": ""},
    "Frank Gardner": {"birth": "01/10/1931", "death": "29/08/2009"},
    "Tony Gaze": {"birth": "03/02/1920", "death": "29/07/2013"},
    "Geki": {"birth": "23/10/1937", "death": "15/06/1967"},
    "Bob Gerard": {"birth": "19/01/1914", "death": "26/01/1990"},
    "Peter Gethin": {"birth": "21/02/1940", "death": "05/12/2011"},
    "Gimax": {"birth": "20/10/1938", "death": ""},
    "Óscar González": {"birth": "10/11/1923", "death": "05/11/2006"},
    "Keith Greene": {"birth": "05/01/1938", "death": "09/01/2021"},
    "Masten Gregory": {"birth": "29/02/1932", "death": "08/11/1985"},
    "Georges Grignard": {"birth": "25/07/1905", "death": "26/12/1977"},
    "Dan Gurney": {"birth": "13/04/1931", "death": "14/01/2018"},
    "Jim Hall": {"birth": "23/07/1935", "death": ""},
    "David Hampshire": {"birth": "29/12/1917", "death": "25/08/1990"},
    "Walt Hansgen": {"birth": "28/10/1919", "death": "07/04/1966"},
    "Mike Harris": {"birth": "25/10/1939", "death": "08/01/2021"},
    "Cuth Harrison": {"birth": "06/12/1906", "death": "21/01/1981"},
    "Brian Hart": {"birth": "07/09/1936", "death": "05/01/2014"},
    "Paul Hawkins": {"birth": "12/10/1937", "death": "26/05/1969"},
    "Boy Hayje": {"birth": "03/05/1949", "death": ""},
    "François Hesnault": {"birth": "30/12/1956", "death": ""},
    "Graham Hill": {"birth": "15/02/1929", "death": "29/11/1975"},
    "Phil Hill": {"birth": "20/04/1927", "death": "28/08/2008"},
    "Peter Hirt": {"birth": "30/03/1910", "death": "28/06/1992"},
    "Gary Hocking": {"birth": "30/09/1937", "death": "21/12/1962"},
    "Nico Hülkenberg": {"birth": "19/08/1987", "death": ""},
    "Gus Hutchison": {"birth": "26/04/1937", "death": ""},
    "Jesús Iglesias": {"birth": "22/02/1922", "death": "11/07/2005"},
    "Innes Ireland": {"birth": "12/06/1930", "death": "22/10/1993"},
    "Chris Irwin": {"birth": "27/06/1942", "death": ""},
    "John James": {"birth": "10/05/1914", "death": "27/10/2002"},
    "Leslie Johnson": {"birth": "22/03/1912", "death": "08/06/1959"},
    "Tom Jones": {"birth": "26/04/1943", "death": ""},
    "Juan Jover": {"birth": "23/11/1903", "death": "28/06/1960"},
    "Ken Kavanagh": {"birth": "12/12/1923", "death": "26/11/2019"},
    "David Kennedy": {"birth": "15/01/1953", "death": ""},
    "Bruce Kessler": {"birth": "23/03/1936", "death": ""},
    "Hans Klenk": {"birth": "28/10/1919", "death": "24/03/2009"},
    "Peter de Klerk": {"birth": "16/03/1935", "death": "11/07/2015"},
    "Willi Krakau": {"birth": "04/12/1911", "death": "26/04/1995"},
    "Robert La Caze": {"birth": "26/02/1917", "death": "01/07/2015"},
    "Oscar Larrauri": {"birth": "19/08/1954", "death": ""},
    "Giovanni Lavaggi": {"birth": "18/02/1958", "death": ""},
    "Chris Lawrence": {"birth": "27/07/1933", "death": "13/08/2011"},
    "Jackie Lewis": {"birth": "01/11/1936", "death": ""},
    "John Love": {"birth": "07/12/1924", "death": "25/04/2005"},
    "Pete Lovely": {"birth": "11/04/1926", "death": "15/05/2011"},
    "Jean Lucienbonnet": {"birth": "07/01/1923", "death": "19/08/1962"},
    "Erik Lundgren": {"birth": "12/11/1919", "death": "04/06/1967"},
    "Brett Lunger": {"birth": "14/11/1945", "death": ""},
    "Mike MacDowel": {"birth": "13/09/1932", "death": "18/01/2016"},
    "Herbert MacKay-Fraser": {"birth": "23/06/1927", "death": "14/07/1957"},
    "Guy Mairesse": {"birth": "10/08/1910", "death": "24/04/1954"},
    "Leslie Marr": {"birth": "14/08/1922", "death": "04/05/2021"},
    "Tony Marsh": {"birth": "20/07/1931", "death": "07/05/2009"},
    "Eugène Martin": {"birth": "24/03/1915", "death": "12/10/2006"},
    "Michael May": {"birth": "18/08/1934", "death": "29/01/2020"},
    "Timmy Mayer": {"birth": "22/02/1938", "death": "28/02/1964"},
    "Brian McGuire": {"birth": "13/12/1945", "death": "29/08/1977"},
    "Harry Merkel": {"birth": "10/01/1918", "death": "11/02/1995"},
    "John Miles": {"birth": "14/06/1943", "death": "08/04/2018"},
    "André Milhoux": {"birth": "09/12/1928", "death": "18/02/2017"},
    "Thomas Monarch": {"birth": "17/06/1912", "death": "13/11/1964"},
    "Andrea Montermini": {"birth": "30/05/1964", "death": ""},
    "Peter Monteverdi": {"birth": "07/06/1934", "death": "04/07/1998"},
    "Dave Morgan": {"birth": "29/08/1944", "death": "07/11/2018"},
    "Bill Moss": {"birth": "04/09/1933", "death": "30/06/2010"},
    "David Murray": {"birth": "28/12/1909", "death": "05/04/1973"},
    "John Nicholson": {"birth": "18/10/1941", "death": "19/09/2017"},
    "Robert O'Brien": {"birth": "11/04/1908", "death": "16/02/1987"},
    "Casimiro de Oliveira": {"birth": "17/02/1907", "death": "08/01/1970"},
    "Jackie Oliver": {"birth": "14/08/1942", "death": ""},
    "Danny Ongais": {"birth": "21/05/1942", "death": "26/02/2022"},
    "Karl Oppitzhauser": {"birth": "05/07/1941", "death": ""},
    "Fritz d'Orey": {"birth": "25/03/1938", "death": "31/08/2020"},
    "Arthur Owen": {"birth": "24/03/1915", "death": "23/04/2000"},
    "Mike Parkes": {"birth": "24/09/1931", "death": "28/08/1977"},
    "Al Pease": {"birth": "15/10/1921", "death": "04/05/2014"},
    "Roger Penske": {"birth": "20/02/1937", "death": ""},
    "Alfredo Piàn": {"birth": "21/10/1912", "death": "25/07/1990"},
    "Paul Pietsch": {"birth": "20/06/1911", "death": "31/05/2012"},
    "Jacques Pollet": {"birth": "02/07/1922", "death": "16/08/1997"},
    "Ben Pon": {"birth": "18/12/1936", "death": "30/09/2019"},
    "Charles Pozzi": {"birth": "27/08/1909", "death": "28/02/2001"},
    "David Prophet": {"birth": "09/10/1937", "death": "29/03/1981"},
    "Dieter Quester": {"birth": "30/05/1939", "death": ""},
    "Ian Raby": {"birth": "22/09/1921", "death": "07/11/1967"},
    "Ray Reed": {"birth": "30/06/1932", "death": "19/02/2012"},
    "Lance Reventlow": {"birth": "24/02/1936", "death": "24/07/1972"},
    "Peter Revson": {"birth": "27/02/1939", "death": "22/03/1974"},
    "John Rhodes": {"birth": "18/08/1927", "death": "27/08/1993"},
    "Ken Richardson": {"birth": "21/08/1911", "death": "27/06/1997"},
    "Giovanni de Riu": {"birth": "10/03/1925", "death": "08/09/2008"},
    "Richard Robarts": {"birth": "22/09/1944", "death": "11/02/2024"},
    "Alexander Rossi": {"birth": "25/09/1991", "death": ""},
    "Jean-Claude Rudaz": {"birth": "15/07/1942", "death": ""},
    "Troy Ruttman": {"birth": "11/03/1930", "death": "19/05/1997"},
    "Peter Ryan": {"birth": "10/06/1940", "death": "02/07/1962"},
    "Harry Schell": {"birth": "29/06/1921", "death": "13/05/1960"},
    "Tim Schenken": {"birth": "26/09/1943", "death": ""},
    "Bernd Schneider": {"birth": "20/07/1964", "death": ""},
    "Rob Schroeder": {"birth": "05/05/1926", "death": "03/12/2011"},
    "Doug Serrurier": {"birth": "15/12/1920", "death": "04/06/2006"},
    "Tony Settember": {"birth": "10/07/1926", "death": "04/05/2014"},
    "Hap Sharp": {"birth": "01/01/1928", "death": "07/05/1993"},
    "Carroll Shelby": {"birth": "11/01/1923", "death": "10/05/2012"},
    "Tony Shelly": {"birth": "02/02/1937", "death": "04/10/1998"},
    "Rob Slotemaker": {"birth": "13/06/1929", "death": "16/09/1979"},
    "Raymond Sommer": {"birth": "31/08/1906", "death": "10/09/1950"},
    "Stephen South": {"birth": "19/02/1952", "death": ""},
    "Will Stevens": {"birth": "28/06/1991", "death": ""},
    "Danny Sullivan": {"birth": "09/03/1950", "death": ""},
    "Andy Sutcliffe": {"birth": "09/05/1947", "death": "13/07/2015"},
    "Henry Taylor": {"birth": "16/12/1932", "death": "24/10/2013"},
    "John Taylor": {"birth": "23/03/1933", "death": "08/09/1966"},
    "Mike Taylor": {"birth": "24/04/1934", "death": "06/12/2017"},
    "Trevor Taylor": {"birth": "26/12/1936", "death": "27/09/2010"},
    "André Testut": {"birth": "13/04/1926", "death": "25/09/2005"},
    "Eric Thompson": {"birth": "04/11/1919", "death": "22/08/2015"},
    "Sam Tingle": {"birth": "24/08/1921", "death": "19/12/2008"},
    "Charles de Tornaco": {"birth": "07/06/1927", "death": "18/09/1953"},
    "Tony Trimmer": {"birth": "24/01/1943", "death": ""},
    "Bobby Unser": {"birth": "20/02/1934", "death": "02/05/2021"},
    "Alberto Urìa": {"birth": "11/07/1924", "death": "04/10/1988"},
    "Jacques Villeneuve (Sr.)": {"birth": "04/11/1953", "death": ""},
    "Ernie de Vos": {"birth": "01/07/1921", "death": "28/07/1965"},
    "Fred Wacker": {"birth": "10/07/1918", "death": "16/07/1998"},
    "David Walker": {"birth": "10/06/1941", "death": ""},
    "Rodger Ward": {"birth": "10/01/1921", "death": "05/07/2004"},
    "Peter Westbury": {"birth": "26/05/1938", "death": "07/12/2015"},
    "Ken Wharton": {"birth": "21/03/1916", "death": "12/01/1957"},
    "Graham Whitehead": {"birth": "15/04/1922", "death": "15/01/1981"},
    "Bill Whitehouse": {"birth": "01/04/1909", "death": "14/07/1957"},
    "Mike Wilds": {"birth": "07/01/1946", "death": ""},
    "Jonathan Williams": {"birth": "26/10/1942", "death": "31/08/2014"},
    "Vic Wilson": {"birth": "14/04/1931", "death": "14/01/2001"},
    "Alessandro Zanardi": {"birth": "23/10/1966", "death": ""},
    "Bob Drake": {"birth": "14/12/1919", "death": "18/04/1990"},
    "Bob Said": {"birth": "05/05/1932", "death": "24/03/2002"},
    "Bobby Rahal": {"birth": "10/01/1953", "death": ""}
}

# Carregar o arquivo JSON
print("Carregando arquivo JSON...")
with open('data/drivers.json', 'r', encoding='utf-8') as file:
    drivers_data = json.load(file)

total_drivers = len(drivers_data)
updated_count = 0
missing_count = 0

print(f"Total de {total_drivers} pilotos encontrados. Iniciando atualização dos dados faltantes...")

# Lista para armazenar pilotos que ainda permanecerão sem informações completas
still_missing = []

# Processar cada piloto
for i, driver in enumerate(drivers_data):
    driver_name = driver["Name"]
    
    # Verificar se o piloto está sem data de nascimento
    if "BirthDate" not in driver or not driver["BirthDate"]:
        # Verificar se temos dados manuais para este piloto
        if driver_name in manual_database:
            driver["BirthDate"] = manual_database[driver_name]["birth"]
            driver["DeathDate"] = manual_database[driver_name]["death"]
            updated_count += 1
            print(f"[{i+1}/{total_drivers}] {driver_name}: Atualizado com dados manuais")
        else:
            missing_count += 1
            still_missing.append(driver_name)
            print(f"[{i+1}/{total_drivers}] {driver_name}: Sem dados disponíveis")
    
    # Verificar se o piloto está com datas incorretas (como datas futuras)
    elif "BirthDate" in driver and driver["BirthDate"]:
        try:
            # Extrair ano da data de nascimento
            birth_year = int(driver["BirthDate"].split("/")[2])
            current_year = 2025  # Ano atual conforme fornecido no metadata
            
            # Se o ano de nascimento for maior que o atual, provavelmente está errado
            if birth_year > current_year:
                # Verificar se temos dados manuais para este piloto
                if driver_name in manual_database:
                    driver["BirthDate"] = manual_database[driver_name]["birth"]
                    driver["DeathDate"] = manual_database[driver_name]["death"]
                    updated_count += 1
                    print(f"[{i+1}/{total_drivers}] {driver_name}: Corrigida data incorreta com dados manuais")
                else:
                    missing_count += 1
                    still_missing.append(driver_name)
                    print(f"[{i+1}/{total_drivers}] {driver_name}: Data incorreta ({birth_year}) sem dados para correção")
        except Exception as e:
            print(f"[{i+1}/{total_drivers}] {driver_name}: Erro ao analisar data: {str(e)}")
    
    # Garantir que o campo "fatal accident" existe
    if "fatal accident" not in driver:
        driver["fatal accident"] = "No"

# Salvar o JSON atualizado
print(f"\nSalvando arquivo JSON atualizado...")
with open('data/drivers.json', 'w', encoding='utf-8') as file:
    json.dump(drivers_data, file, indent=4)

print(f"\nResumo da atualização:")
print(f"Total de pilotos: {total_drivers}")
print(f"Pilotos atualizados nesta rodada: {updated_count}")
print(f"Pilotos ainda sem informações completas: {missing_count}")

if still_missing:
    print("\nPilotos ainda sem informações completas:")
    for driver in still_missing:
        print(f"- {driver}")

print("\nProcesso concluído! Todas as datas disponíveis foram atualizadas.")
