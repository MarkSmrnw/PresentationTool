import flet as ft

from typing import Callable
from dataclasses import dataclass

@dataclass
class AppState: # Nicer way of storing values?
    is_presenting: bool = False
    current_slide: int = 0
    laser_active: bool = False

class PresentationApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = AppState()

        page.title = "Presentation Tool" # very CSS like. Mayor likeage
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 20
        page.theme_mode = ft.ThemeMode.DARK

        self.build_ui()

    def build_ui(self):
        header = ft.Text(
            "Presentation Tool",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        status_text = ft.Text(
            f"Status: {'Presenting' if self.state.is_presenting else 'Idle'} | Slide: {self.state.current_slide}",
            size=16
        )

        start_btn = ft.Button(
            "Start Presentation",
            on_click=self.toggle_presentation,
        )

        laser_btn = ft.Button(
            "Toggle Laser Pointer",
            on_click=self.toggle_laser,
            width=300,
            height=50,
        )

        self.page.add(
            ft.Column(
                [   # List of things that will be added to the Colum, can be anything ?
                    header,
                    status_text,
                    start_btn,
                    laser_btn,
                    ft.Divider(height=40),
                    ft.Text("Features coming: Laser, Notes, Clicker...")
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
            )
        )

        self.status_text = status_text

    def toggle_laser(self, e: ft.ControlEvent):
        self.state.laser_active = not self.state.laser_active
        self.status_text.value = (
            f"Status: {'Presenting' if self.state.is_presenting else 'Idle'} | "
            f"Slide: {self.state.current_slide} | "
            f"Laser: {'ON' if self.state.laser_active else 'OFF'}"
        )

        self.page.update()

    def toggle_presentation(self, e: ft.ControlEvent):
        self.state.is_presenting = not self.state.is_presenting
        self.status_text.value = (
            f"Status: {'Presenting' if self.state.is_presenting else 'Idle'} | "
            f"Slide: {self.state.current_slide} | "
            f"Laser: {'ON' if self.state.laser_active else 'OFF'}"
        )

        self.page.update()

def main(page: ft.Page):
    PresentationApp(page)

if __name__ == "__main__":
    ft.run(main)