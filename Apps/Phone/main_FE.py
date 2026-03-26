import asyncio
import datetime
import requests
import threading

import flet as ft

from scripts.webrtc import init_webrtc_connection

def flet_main(page:ft.Page):

    page.title = "Phone Frontend"
    page.bgcolor = ft.Colors.BROWN_100

    input=ft.TextField(value="192.168.178.15", text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK)

    notif_banner = ft.Row(
        height=100,
        controls=[
            ft.Text("Temp!")
        ],
    )

    def test(e:any):
        print(input.value)
        print(f"Triggered at {datetime.datetime.now()}")
        print(f"Parsed args: {e}\n")

        request = requests.get(f"http://{input.value}:8000/ping")

        threading.Thread(target=lambda: asyncio.run(init_webrtc_connection(input.value))).start()

    page.add(
        ft.Container(
            height=200,
            content=notif_banner
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Temp frontend for Mobile.", color=ft.Colors.BLACK, size=20),
            ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                input
            ]
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    margin=30,
                    content=ft.Button(
                        "Connect", 
                        icon=ft.Icons.WIFI,
                        on_click=test,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        tooltip="Sigma"
                    )
                )
            ]
        )
    )

ft.run(flet_main)