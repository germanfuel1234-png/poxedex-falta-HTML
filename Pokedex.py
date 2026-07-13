import requests

def obtener_datos_pokemon(pokemon_id):
    url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    url_especie = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"

    datos_pokemon = requests.get(url_pokemon).json()
    datos_especie = requests.get(url_especie).json()

    nombre = datos_pokemon['name'].capitalize()
    tipos = ", ".join([t['type']['name'] for t in datos_pokemon['types']])
    peso = datos_pokemon['weight'] / 10  # hectogramos → kg
    altura = datos_pokemon['height'] / 10  # decímetros → m

    # Buscar la descripción en español
    descripcion = next(
        (entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
         for entry in datos_especie['flavor_text_entries']
         if entry['language']['name'] == 'es'),
        "Sin descripción."
    )

    return {
        "nombre": nombre,
        "tipos": tipos,
        "peso": peso,
        "altura": altura,
        "descripcion": descripcion
    }
