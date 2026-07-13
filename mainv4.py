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

import flet as ft
async def main(page: ft.Page):
    #espera un resultado
    #await page.add_async(ft.Text(value="hola mundo"))
    page.window_width =720
    page.window_height =1280
    page.window_resizable = False
    page.padding = 0
    boton_azul = ft.Stack([
        ft.Container(width =80,height =80,bgcolor=ft.colors.WHITE,border_radius=50),
        ft.Container(width =70,height =70,left=5,top=5,bgcolor=ft.colors.BLUE,border_radius=50)
    ])
    items_superior = [
        ft.Container(boton_azul, width=80,height=80,),
        ft.Container(width=40,height=40,bgcolor=ft.colors.RED_200,border_radius=50),
        ft.Container(width=40,height=40,bgcolor=ft.colors.YELLOW,border_radius=50),
        ft.Container(width=40,height=40,bgcolor=ft.colors.GREEN,border_radius=50),
    ]
    stack_central = ft.Stack([
        ft.Container(width =600,height =400,bgcolor=ft.colors.WHITE),
        ft.Container(width =550,height =350,bgcolor=ft.colors.BLACK,top=25,left=25),
        ft.Image(
            src= "https://raw.githubusercontent.com/pokeapi/sprites/master/sprites/pokemon/132.png",
            scale=10,
            width=50,
            height=50,
            top=350/2,
            right=550/2,
        )
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

    flechas= ft.Column(
        [
            ft.Container(triangulo,width=50,height=80,border=ft.border.all()),
            #radianes 180grados=1.1415
            ft.Container(triangulo,rotate=ft.Rotate(angle=3.14159) ,width=50,height=80,border=ft.border.all()),
        ]
    )
    items_inferior =[
        ft.Container(width=50,border=ft.border.all()),#margen izquierdo
        ft.Container(width=400,height=300,bgcolor=ft.colors.GREEN,border_radius=20),
        ft.Container(flechas,width=80,height=120,border=ft.border.all()),
        ft.Container(width=50,height=120,border=ft.border.all()),#margen derecho
    ]

    superior = ft.Container(content=ft.Row(items_superior), width =600,height =80, margin=ft.margin.only(top=40))
    centro = ft.Container(content=stack_central,width =600,height =400, margin=ft.margin.only(top=40),alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior),width =600,height =400, margin=ft.margin.only(top=40),border=ft.border.all())

    col= ft.Column(spacing=0,controls=[
        superior,
        centro,
        inferior,
    ])
    contenedor = ft.Container(col,width =720,height =1280, bgcolor =ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(contenedor)

ft.app(target=main)

