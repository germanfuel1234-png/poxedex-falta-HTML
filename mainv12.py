
import flet as ft
import asyncio
import flet.canvas as canvas
import requests
import sys

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
    # Flechas canvas personalizadas
    def flecha_diamante_canvas():
        # Canvas único para el diamante y las flechas, áreas de click divididas con Column y Expanded
        def siguiente():
            nonlocal pokemon_actual
            if pokemon_actual >= 151:
                pokemon_actual = 1
            else:
                pokemon_actual += 1
            actualizar_ui(obtener_datos_pokemon(pokemon_actual))
        def anterior():
            nonlocal pokemon_actual
            if pokemon_actual <= 1:
                pokemon_actual = 151
            else:
                pokemon_actual -= 1
            actualizar_ui(obtener_datos_pokemon(pokemon_actual))
        return ft.Container(
            width=esc(60), height=esc(60),
            content=ft.Stack([
                ft.Container(
                    width=esc(60), height=esc(60),
                    content=canvas.Canvas([
                        # Diamante blanco (borde)
                        canvas.Path([

                            # Flechas canvas personalizadas
                            def flecha_diamante_canvas():
                                return ft.Container(
                                    width=esc(60), height=esc(60),
                                    content=ft.Stack([
                                        ft.Container(
                                            width=esc(60), height=esc(60),
                                            content=canvas.Canvas([
                                                canvas.Path([
                                                    canvas.Path.MoveTo(esc(30), esc(5)),
                                                    canvas.Path.LineTo(esc(55), esc(30)),
                                                    canvas.Path.LineTo(esc(30), esc(55)),
                                                    canvas.Path.LineTo(esc(5), esc(30)),
                                                    canvas.Path.Close(),
                                                ]),
                                                canvas.Fill(ft.Colors.WHITE),
                                                canvas.Path([
                                                    canvas.Path.MoveTo(esc(30), esc(12)),
                                                    canvas.Path.LineTo(esc(48), esc(30)),
                                                    canvas.Path.LineTo(esc(30), esc(48)),
                                                    canvas.Path.LineTo(esc(12), esc(30)),
                                                    canvas.Path.Close(),
                                                ]),
                                                canvas.Fill(ft.Colors.BLACK),
                                                canvas.Line(esc(18), esc(30), esc(42), esc(30), paint=ft.Paint(stroke_width=2, color=ft.Colors.WHITE)),
                                                canvas.Path([
                                                    canvas.Path.MoveTo(esc(30), esc(18)),
                                                    canvas.Path.LineTo(esc(36), esc(28)),
                                                    canvas.Path.LineTo(esc(24), esc(28)),
                                                    canvas.Path.Close(),
                                                ]),
                                                canvas.Fill(ft.Colors.WHITE),
                                                canvas.Path([
                                                    canvas.Path.MoveTo(esc(30), esc(42)),
                                                    canvas.Path.LineTo(esc(36), esc(32)),
                                                    canvas.Path.LineTo(esc(24), esc(32)),
                                                    canvas.Path.Close(),
                                                ]),
                                                canvas.Fill(ft.Colors.WHITE),
                                            ], width=esc(60), height=esc(60)),
                                        ),
                                        ft.Column([
                                            ft.Container(
                                                expand=True,
                                                content=ft.GestureDetector(
                                                    on_tap=lambda e: cambiar_pokemon(1),
                                                    content=ft.Container(bgcolor="transparent")
                                                )
                                            ),
                                            ft.Container(
                                                expand=True,
                                                content=ft.GestureDetector(
                                                    on_tap=lambda e: cambiar_pokemon(-1),
                                                    content=ft.Container(bgcolor="transparent")
                                                )
                                            ),
                                        ], width=esc(60), height=esc(60)),
                                    ])
                                )

                            # Contenedor superior (Luces)
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
                                border=ft.Border.all(10, ft.Colors.GREY_300)
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
                                    inferior
                                ], horizontal_alignment="center", spacing=esc(20), scroll=ft.ScrollMode.AUTO)
                            )

                            actualizar_ui(obtener_datos_pokemon(1))

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