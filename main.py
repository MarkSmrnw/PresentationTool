import flet as ft

def main(page: ft.Page):
    page.title = "Presentation Tool"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Text("Hello World!", size=40, weight=ft.FontWeight.BOLD),
        ft.Button("Start", on_click=lambda e: print("Click")),
    )

ft.run(main)