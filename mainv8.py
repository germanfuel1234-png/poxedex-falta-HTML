#creamos el entorno virtual,para ello vamos a la terminal y escribimos

#python -m venv venv
#.\venv\scripts\active
#pip install virtualenv

#virtualenv env
#cd env/Scripts
#en powershel de windes poner: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#activate
#exit
#pip install flet
#pip install aiohttp asyncio

import flet as ft
import aiohttp
import asyncio

pokemon_actual = 0



async def main(page: ft.Page):
    #espera un resultado
    #await page.add_async(ft.Text(value="hola mundo"))
    page.window_width =720
    page.window_height =1280
    page.window_resizable = False
    page.padding = 0
    page.fonts= {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.9/zpix.ttf",
    }
    page.theme= ft.Theme(font_family="zpix")

    
    async def peticion(url):
        async with aiohttp.ClientSession() as sesion:
            async with sesion.get(url) as response:
                return await response.json()
    
    async def evento_pokemon (e: ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual+=1
        else:
            pokemon_actual-=1

        numero =  (pokemon_actual%150)+1 
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")

        datos= f"name: {resultado['name']}\n\nAbilities:"
        for elemento in resultado['abilities']:
            habilidad = elemento ['abilities']['name']
            datos += f"\n{habilidad}"
        datos +=f"\n\nHeight: {resultado['height']}"
        texto.value = datos
        sprite_url=f"https://raw.githubusercontent.com/pokeapi/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src=sprite_url
        await page.update()

    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update()



    luz_azul=ft.Container(width =70,height =70,left=5,top=5,bgcolor=ft.colors.BLUE,border_radius=50)
    boton_azul = ft.Stack([
        ft.Container(width =80,height =80,bgcolor=ft.colors.WHITE,border_radius=50),
        luz_azul,
    ])
    items_superior = [
        ft.Container(boton_azul, width=80,height=80,),
        ft.Container(width=40,height=40,bgcolor=ft.colors.RED_200,border_radius=50),
        ft.Container(width=40,height=40,bgcolor=ft.colors.YELLOW,border_radius=50),
        ft.Container(width=40,height=40,bgcolor=ft.colors.GREEN,border_radius=50),
    ]

    sprite_url=f"https://raw.githubusercontent.com/pokeapi/sprites/master/sprites/pokemon/0.png"
    imagen= ft.Image(
       src= sprite_url,
       scale=10,
       width=30,
       height=30,
       top=350/2,
       right=550/2,
    )

    stack_central = ft.Stack([
        ft.Container(width =600,height =400,bgcolor=ft.colors.WHITE,border_radius=20),
        ft.Container(width =550,height =350,bgcolor=ft.colors.BLACK,top=25,left=25),
        imagen,    
    ])

    triangulo=ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(40,0),
            ft.canvas.Path.LineTo(0,50),
            ft.canvas.Path.LineTo(80,50),
        ],
        paint=ft.Paint(
                style=ft.PaintingStyle.FILL,
            ),
        ),
    ],
    width=80,
    height=50,
    )

    flecha_superior=ft.Container(triangulo,width=80,height=50,on_click=evento_pokemon)
    flechas= ft.Column(
        [
            flecha_superior,
            #radianes 180grados=1.1415
            ft.Container(triangulo,rotate=ft.Rotate(angle=3.14159) ,width=80,height=50,on_click=evento_pokemon),

        ]
    )
    texto=ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=22,
    )

    items_inferior = [
        ft.Container(width=50,),#margen izquierdo
        ft.Container(texto, padding=10, width=400, height=300, bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(width=30,),#margen derecho
        ft.Container(flechas,width=80,height=120),
    ]

    superior = ft.Container(content=ft.Row(items_superior), width =600,height =80, margin=ft.margin.only(top=40))
    centro = ft.Container(content=stack_central, width =600, height =400, margin=ft.margin.only(top=40), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior),width =600,height =400, margin=ft.margin.only(top=40),)

    col= ft.Column(spacing=0,controls=[
        superior,
        centro,
        inferior,
    ])
    contenedor = ft.Container(col,width =720,height =1280, bgcolor =ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await blink()

ft.app(target=main)

