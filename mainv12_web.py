
import flet as ft
import flet.canvas as canvas
import asyncio
import requests

# Estado global compartido entre todas las sesiones
estado = {"pokemon_id": 1}


def obtener_datos_pokemon(pokemon_id):
    try:
        url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        url_especie = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
        datos_pokemon = requests.get(url_pokemon).json()
        datos_especie = requests.get(url_especie).json()
        nombre = datos_pokemon['name'].capitalize()
        tipos = ", ".join([t['type']['name'] for t in datos_pokemon['types']])
        peso = datos_pokemon['weight'] / 10
        altura = datos_pokemon['height'] / 10
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
            "descripcion": descripcion,
            "id": datos_pokemon['id']
        }
    except Exception as e:
        print(f"Error: {e}")
        return None


async def main(page: ft.Page):
    page.title = "Pokedex Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.RED_400
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    pokemon_actual = estado["pokemon_id"]

    # Escalado: referencia 500px de ancho (igual que la versión escritorio)
    def esc(x):
        w = page.width if page.width and page.width > 0 else 500
        return x * min(w / 500, 1.4)

    # --- ELEMENTOS DE UI ---
    texto = ft.Text(value="Cargando...", color=ft.Colors.BLACK, size=esc(14))
    imagen = ft.Image(
        src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        width=esc(150),
        height=esc(150),
        fit="contain",
    )
    luz_azul = ft.Container(
        width=esc(40), height=esc(40),
        bgcolor=ft.Colors.BLUE,
        border_radius=50,
        border=ft.Border.all(3, ft.Colors.WHITE),
    )

    # --- FUNCIONES DE EVENTO ---
    def actualizar_ui(datos):
        if datos:
            texto.value = (
                f"Nombre: {datos['nombre']}\n"
                f"N° Pokédex: {datos['id']}\n"
                f"Peso: {datos['peso']} kg\n"
                f"Altura: {datos['altura']} m\n"
                f"Tipo: {datos['tipos']}\n\n"
                f"{datos['descripcion']}"
            )
            imagen.src = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{datos['id']}.png"
            page.update()

    # --- PUBSUB: sincronización en tiempo real entre sesiones ---
    def on_cambio_pokemon(nuevo_id):
        nonlocal pokemon_actual
        pokemon_actual = nuevo_id
        async def _fetch():
            datos = await asyncio.to_thread(obtener_datos_pokemon, nuevo_id)
            actualizar_ui(datos)
        page.run_task(_fetch)

    page.pubsub.subscribe(on_cambio_pokemon)
    page.on_disconnect = lambda _: page.pubsub.unsubscribe_all()

    # --- DIAMANTE CON FLECHAS (igual que escritorio, con async) ---
    def flecha_diamante_canvas():
        async def siguiente(e=None):
            nonlocal pokemon_actual
            pokemon_actual = 1 if pokemon_actual >= 151 else pokemon_actual + 1
            estado["pokemon_id"] = pokemon_actual
            page.pubsub.send_all(pokemon_actual)

        async def anterior(e=None):
            nonlocal pokemon_actual
            pokemon_actual = 151 if pokemon_actual <= 1 else pokemon_actual - 1
            estado["pokemon_id"] = pokemon_actual
            page.pubsub.send_all(pokemon_actual)

        sz = esc(60)
        return ft.Container(
            width=sz, height=sz,
            content=ft.Stack([
                ft.Container(
                    width=sz, height=sz,
                    content=canvas.Canvas([
                        # Diamante blanco (borde exterior)
                        canvas.Path([
                            canvas.Path.MoveTo(sz / 2, sz * 0.05),
                            canvas.Path.LineTo(sz * 0.95, sz / 2),
                            canvas.Path.LineTo(sz / 2, sz * 0.95),
                            canvas.Path.LineTo(sz * 0.05, sz / 2),
                            canvas.Path.Close(),
                        ]),
                        canvas.Fill(ft.Colors.WHITE),
                        # Diamante negro (interior)
                        canvas.Path([
                            canvas.Path.MoveTo(sz / 2, sz * 0.20),
                            canvas.Path.LineTo(sz * 0.80, sz / 2),
                            canvas.Path.LineTo(sz / 2, sz * 0.80),
                            canvas.Path.LineTo(sz * 0.20, sz / 2),
                            canvas.Path.Close(),
                        ]),
                        canvas.Fill(ft.Colors.BLACK),
                        # Flecha arriba (triángulo blanco)
                        canvas.Path([
                            canvas.Path.MoveTo(sz / 2, sz * 0.28),
                            canvas.Path.LineTo(sz * 0.62, sz * 0.46),
                            canvas.Path.LineTo(sz * 0.38, sz * 0.46),
                            canvas.Path.Close(),
                        ]),
                        canvas.Fill(ft.Colors.WHITE),
                        # Flecha abajo (triángulo blanco)
                        canvas.Path([
                            canvas.Path.MoveTo(sz / 2, sz * 0.72),
                            canvas.Path.LineTo(sz * 0.62, sz * 0.54),
                            canvas.Path.LineTo(sz * 0.38, sz * 0.54),
                            canvas.Path.Close(),
                        ]),
                        canvas.Fill(ft.Colors.WHITE),
                    ], width=sz, height=sz),
                ),
                # Mitad superior → siguiente; mitad inferior → anterior
                ft.Column([
                    ft.Container(
                        expand=True,
                        content=ft.GestureDetector(
                            on_tap=siguiente,
                            content=ft.Container(bgcolor="transparent"),
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.GestureDetector(
                            on_tap=anterior,
                            content=ft.Container(bgcolor="transparent"),
                        ),
                    ),
                ], width=sz, height=sz),
            ])
        )

    # --- ESTRUCTURA VISUAL ---
    superior = ft.Row([
        luz_azul,
        ft.Container(width=esc(15), height=esc(15), bgcolor=ft.Colors.RED_200, border_radius=50),
        ft.Container(width=esc(15), height=esc(15), bgcolor=ft.Colors.YELLOW, border_radius=50),
        ft.Container(width=esc(15), height=esc(15), bgcolor=ft.Colors.GREEN, border_radius=50),
    ], alignment="center")

    centro = ft.Container(
        content=imagen,
        width=esc(300),
        height=esc(250),
        bgcolor=ft.Colors.BLACK,
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(10, ft.Colors.GREY_300),
    )

    inferior = ft.Row([
        ft.Container(
            width=esc(300),
            content=ft.Row([
                ft.Container(
                    content=texto,
                    padding=esc(20),
                    width=esc(200),
                    height=esc(200),
                    bgcolor=ft.Colors.GREEN_300,
                    border_radius=10,
                    alignment=ft.Alignment.TOP_LEFT,
                ),
                ft.Container(
                    content=flecha_diamante_canvas(),
                    alignment=ft.Alignment.CENTER,
                ),
            ], alignment="end"),
        ),
    ], alignment="center")

    page.add(
        ft.Column([
            ft.Text("POKEDEX", size=esc(30), weight="bold", color=ft.Colors.RED_800),
            superior,
            centro,
            inferior,
        ], horizontal_alignment="center", spacing=esc(20), scroll=ft.ScrollMode.AUTO)
    )

    # Carga inicial sin bloquear
    datos_iniciales = await asyncio.to_thread(obtener_datos_pokemon, estado["pokemon_id"])
    actualizar_ui(datos_iniciales)

    # Bucle de parpadeo
    while True:
        try:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.Colors.BLUE_200
            page.update()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.Colors.BLUE
            page.update()
        except Exception:
            print("Sesión perdida, esperando nueva conexión...")
            break


print("Iniciando servidor Flet...")
ft.run(main, view="web_browser", host="0.0.0.0", port=8666)