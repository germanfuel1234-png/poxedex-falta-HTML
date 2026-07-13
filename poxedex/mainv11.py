import flet as ft
import asyncio
import flet.canvas as canvas
import requests

pokemon_actual = 0

async def main(page: ft.Page):
    page.title = "Pokédex Responsive"
    page.window_resizable = True
    page.padding = 0
    page.margin = 0
    page.bgcolor = ft.Colors.RED_600
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
    }
    page.theme = ft.Theme(font_family="zpix")

    async def evento_get_pokemon(e):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual += 1
        else:
            pokemon_actual -= 1
        numero = (pokemon_actual % 150) + 1
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url
        # Obtener datos del Pokémon
        import requests
        datos = obtener_datos_pokemon(numero)
        texto.value = f"Nombre: {datos['nombre']}\nN° Pokédex: {numero}\nPeso: {datos['peso']} kg\nAltura: {datos['altura']} m\nTipo: {datos['tipos']}\n\n{datos['descripcion']}"
        page.update()

    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.Colors.BLUE_100
            page.update()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.Colors.BLUE
            page.update()

    scale_w = page.width / 720 if page.width > 0 else 1
    scale_h = page.height / 1280 if page.height > 0 else 1
    scale = min(scale_w, scale_h)

    def esc(x): return x * scale

    luz_azul = ft.Container(width=esc(70), height=esc(70), left=esc(5), top=esc(5), bgcolor=ft.Colors.BLUE, border_radius=50)
    boton_azul = ft.Stack([
        ft.Container(width=esc(80), height=esc(80), bgcolor=ft.Colors.WHITE, border_radius=50),
        luz_azul,
    ])

    items_superior = [
        ft.Container(boton_azul, width=esc(80), height=esc(80)),
        ft.Container(width=esc(40), height=esc(40), bgcolor=ft.Colors.RED_200, border_radius=50),
        ft.Container(width=esc(40), height=esc(40), bgcolor=ft.Colors.YELLOW, border_radius=50),
        ft.Container(width=esc(40), height=esc(40), bgcolor=ft.Colors.GREEN, border_radius=50),
    ]

    imagen = ft.Image(
        src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        width=esc(150),
        height=esc(150),
        top=esc(175),
        right=esc(275),
    )

    stack_central = ft.Stack(
        [
            ft.Container(width=esc(600), height=esc(400), bgcolor=ft.Colors.WHITE, border_radius=20),
            ft.Container(width=esc(550), height=esc(350), bgcolor=ft.Colors.BLACK, top=esc(25), left=esc(25)),
            imagen,
        ]
    )

    triangulo = canvas.Canvas([
        canvas.Path([
            canvas.Path.MoveTo(esc(40), esc(0)),
            canvas.Path.LineTo(esc(0), esc(50)),
            canvas.Path.LineTo(esc(80), esc(50)),
            canvas.Path.Close(),
        ]),
        canvas.Fill(ft.Colors.BLACK),
    ], width=esc(80), height=esc(50))

    flecha_superior = ft.Container(triangulo, width=esc(80), height=esc(50), on_click=evento_get_pokemon)

    flechas = ft.Column(
        [
            flecha_superior,
            ft.Container(triangulo, width=esc(80), height=esc(50), rotate=ft.Rotate(angle=3.14159), on_click=evento_get_pokemon),
        ]
    )

    datos_inicial = obtener_datos_pokemon(1)
    texto = ft.Text(
        value=f"Nombre: {datos_inicial['nombre']}\nN° Pokédex: 1\nPeso: {datos_inicial['peso']} kg\nAltura: {datos_inicial['altura']} m\nTipo: {datos_inicial['tipos']}\n\n{datos_inicial['descripcion']}",
        color=ft.Colors.BLACK,
        size=esc(28)
    )

    items_inferior = [
        ft.Container(width=esc(50)),
        ft.Container(texto, padding=esc(20), width=esc(450), height=esc(320), bgcolor=ft.Colors.GREEN_800, border_radius=30),
        ft.Container(width=esc(30)),
        ft.Container(flechas, width=esc(120), height=esc(180)),
    ]

    superior = ft.Container(content=ft.Row(items_superior, alignment="center"), width=esc(600), height=esc(80), margin=ft.Margin.only(top=esc(40)))
    centro = ft.Container(stack_central, width=esc(600), height=esc(400), margin=ft.Margin.only(top=esc(40)), alignment="center")
    inferior = ft.Container(content=ft.Row(items_inferior), width=esc(600), height=esc(400), margin=ft.Margin.only(top=esc(80)))

    col = ft.Column(spacing=0, controls=[superior, centro, inferior], horizontal_alignment="center")

    contenedor = ft.Container(col, bgcolor=ft.Colors.RED_600, alignment="topCenter", expand=True)



    page.add(contenedor)
    page.update()
    await blink()

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

ft.run(main)
