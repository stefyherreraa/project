mport random
import requests

pokemon_choice = input('Enter a pokemon name: ')
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_choice}"

#La función es utilizada por varias otras funciones para obtener datos de la PokeAPI. 
# Esta función toma el nombre de un Pokemon y devuelve los datos del Pokemon en formato JSON, 
# utilizando la biblioteca requests para realizar una solicitud HTTP a la PokeAPI.

# Definimos una función llamada fetch_data que toma un argumento llamado pokemon_name
def fetch_data(pokemon_name):
    # Hacemos una solicitud HTTP GET a la PokeAPI utilizando el nombre del pokemon como variable en la URL
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    
    # Comprobamos si la respuesta es satisfactoria (código de estado 200)
    if response.status_code == 200:
        # Si es satisfactoria, convertimos la respuesta en un objeto JSON (diccionario de Python)
        data = response.json()
        # Devolvemos el objeto JSON
        return data
    else:
        # Si la respuesta no es satisfactoria, devolvemos None para indicar que no se encontraron datos
        return None


# las estadisticas de tu pokemon
def pokemon_data(pokemon_name):
    # Llama a la función fetch_data para obtener los datos del pokemon
    data = fetch_data(pokemon_name)
    # Si se reciben datos del pokemon
    if data:
        # Accede al valor de HP y peso del pokemon desde los datos
        hp = data['stats'][0]['base_stat']
        weight = data['weight']
        # Imprime el nombre del pokemon, su HP y su peso
        print(f'{pokemon_choice} HP is {hp} and its weight is {weight}.')
    # Si no se reciben datos del pokemon
    else:
        # Imprime un mensaje de error
        print('An error occurred.')

# sacar la cuenta de los pokemones

def count_of_pokemons():
    # Envía una solicitud GET HTTP a la API PokeAPI para obtener información de todos los pokemons.
    response = requests.get('https://pokeapi.co/api/v2/pokemon')
    # Verifica si la solicitud HTTP fue exitosa (código de estado 200).
    if response.status_code == 200:
        # Convierte la respuesta JSON a un diccionario de Python.
        data = response.json()
        # Obtiene el número total de pokemons disponible en la API.
        count = data['count']
        # Imprime el número total de pokemons y devuelve el valor.
        print(f'There are {count} pokemons in total.')
        return count
    else:
        # Si la solicitud HTTP no es exitosa, imprime un mensaje de error y devuelve 0.
        print('An error occurred.')
        return 0
    
# buscar los movimientos del pokemon
def pokemon_moves(pokemon_name):
    # obtener los datos del pokemon
    data = fetch_data(pokemon_name)
    # verificar si los datos se obtuvieron bien
    if data:
        # crear una lista vacía para almacenar los movimientos del pokemon
        moves = []
        # tomar los primeros 5 movimientos del pokemon
        for move in data['moves'][:5]:
            # obtener el nombre del movimiento
            move_name = move['move']['name']
            # añadir el nombre del movimiento a la lista de movimientos
            moves.append(move_name)
        # imprimir los movimientos del pokemon
        print(f'{pokemon_name} moves are: {moves}')
    else:
        # si no se pudieron obtener los datos del pokemon, imprimir un mensaje de error
        print('An error occurred, try again.')

# comparar la vida de tu pokemon con un pokemon random
def compare(pokemon_name):
    data = fetch_data(pokemon_name)  # se obtienen los datos del pokemon introducido
    if data:
        poke_hp = data['stats'][0]['base_stat']  # se obtiene el valor de la estadistica HP
        count = count_of_pokemons()  # se cuenta el total de pokemones en la API
        random_poke_id = random.randint(1, count)  # se genera un ID aleatorio de pokemon
        random_poke_data = fetch_data(random_poke_id)  # se obtienen los datos del pokemon aleatorio
        if random_poke_data:
            random_poke_name = random_poke_data['name']  # se obtiene el nombre del pokemon aleatorio
            rand_pok_hp = random_poke_data['stats'][0]['base_stat']  # se obtiene el valor de la estadistica HP del pokemon aleatorio
            print(f'The random pokemon is: {random_poke_name}')  # se imprime el nombre del pokemon aleatorio
            if rand_pok_hp > poke_hp:
                print(f'{random_poke_name} has more HP than {pokemon_choice}.')  # se compara la HP del pokemon aleatorio con el pokemon introducido
            else:
                print(f'{pokemon_choice} has the same or more HP than {random_poke_name}.')  # se compara la HP del pokemon aleatorio con el pokemon introducido
        else:
            print('An error occurred.')
    else:
        print('An error occurred.')


def get_pokemon_weight(pokemon_name):
    # Se llama a la función fetch_data para obtener los datos del pokemon
    data = fetch_data(pokemon_name)
    if data:
        # Si se obtienen los datos correctamente, se devuelve el peso del pokemon
        return data["weight"]
    else:
        # Si no se pueden obtener los datos, se devuelve None
        return None


def count_heavier_pokemons(pokemon_name):
    # Obtener el peso del Pokémon especificado
    pokemon_weight = get_pokemon_weight(pokemon_name)


    print("please wait a minute")
    # Obtener el número total de pokémon
    count = count_of_pokemons()
    # Establecer valores para buscar la lista de pokémones
    offset = 0
    limit = count
    more_pokemons = True
    count_heavier = 0
    # hacer el loop hasta que no haya más pokémon que buscar
    while more_pokemons:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit={limit}")
        if response.status_code == 200:
            pokemon_list_data = response.json()
            pokemon_list = pokemon_list_data["results"]
            #comparar cada pokemon
            for pokemon in pokemon_list:
                #obtener la informacion del pokemon
                response = requests.get(pokemon["url"])
                if response.status_code == 200:
                    pokemon_data = response.json()
                    pokemon_weight = pokemon_data["weight"]
                    #si el pokemon pesa mas que el indicado al principio agregar 1 al valor total de los mas pesados
                    if pokemon_weight > get_pokemon_weight(pokemon_name):
                        count_heavier += 1
                else:
                    print(f"Failed to retrieve data for {pokemon['name']}")
            #incrementar el offset
            offset += limit
            #si no hay mas salir del loop while
            if offset >= pokemon_list_data["count"]:
                more_pokemons = False
        else:
            print("Failed to retrieve Pokémon list")
    #imprimir el resultado
    print(f'In total there are {count_heavier} pokemons heavier than {pokemon_name}')

def can_evolve(pokemon_name):
    # Construir URL para obtener datos del Pokemon
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)

    # Si la respuesta HTTP es exitosa (código 200)
    if response.status_code == 200:
        # Obtener la URL de la especie del Pokemon
        species_url = response.json()["species"]["url"]
        response = requests.get(species_url)
        # Obtener la URL de la cadena de evolución de la especie del Pokemon
        evolution_chain_url = response.json()["evolution_chain"]["url"]
        response = requests.get(evolution_chain_url)
        # Obtener la cadena de evolución de la especie del Pokemon
        chain = response.json()["chain"]
        # Buscar en la cadena de evolución hasta encontrar el Pokemon solicitado
        while chain["species"]["name"] != pokemon_name:
            chain = chain["evolves_to"][0]
            # Si no hay más evoluciones posibles, el Pokemon no puede evolucionar
            if not chain["evolves_to"]:
                print(f"{pokemon_name} cannot evolve any further.")
                return False
        # Imprimir los nombres de los Pokemon a los que el Pokemon solicitado puede evolucionar
        print(f"{pokemon_name} can evolve into:")
        for evolution in chain["evolves_to"]:
            print(evolution["species"]["name"])
        return True
    else:
        # Si la respuesta HTTP no es exitosa, imprimir mensaje de error y retornar False
        print('Error: Could not retrieve data.')
        return False

#muestra todos los resultados
poke_data = fetch_data(pokemon_choice)
if poke_data:
    pokemon_data(pokemon_choice)
    count_of_pokemons()
    pokemon_moves(pokemon_choice)
    compare(pokemon_choice)
    can_evolve(pokemon_choice)
    count_heavier_pokemons(pokemon_choice)
else:
    print("Could not retrieve information about the Pokémon.")
