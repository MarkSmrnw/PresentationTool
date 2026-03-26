import flet as ft

def main(page:ft.Page):

    page.title = "Desktop Frontend"
    page.bgcolor = ft.Colors.WHITE

    icBTN = ft.IconButton(
        icon=ft.Icons.CAMERA,
    )

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            controls=[
                ft.Text("Temp frontend for Desktop.", color=ft.Colors.BLACK, size=20),
            ]
        )
    )

ft.run(main)