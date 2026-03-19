import flet as ft

from typing import Callable
from dataclasses import dataclass
from flet import (
    GestureDetector, DragUpdateEvent, Container
)

@dataclass
class AppState:
    is_presenting: bool = False
    current_slide: int = 0
    laser_active: bool = False
    laser_pos: tuple[float, float] | None = None 

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

        presentation_area = Container(
            width=800,
            height=500,
            bgcolor=ft.Colors.BLACK,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_800),
            border_radius=10,
            content=GestureDetector(
                mouse_cursor=ft.MouseCursor.CLICK if self.state.laser_active else ft.MouseCursor.BASIC,
                on_pan_update=self.on_laser_drag,
                drag_interval=5,
                content=Container(expand=True, bgcolor=ft.Colors.TRANSPARENT)
            ),
            visible=self.state.is_presenting
        )

        self.page.add(
            ft.Column(
                [   # List of things that will be added to the Colum, can be anything ?
                    header,
                    status_text,
                    start_btn,
                    laser_btn,
                    ft.Divider(height=40),
                    ft.Text("Features coming: Laser, Notes, Clicker..."),
                    presentation_area
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
            )
        )

        self.presentation_area = presentation_area

        self.status_text = status_text

    def toggle_laser(self, e: ft.ControlEvent):
        self.state.laser_active = not self.state.laser_active
        if not self.state.laser_active:
            self.state.laser_pos = None
        self.status_text.value = (
            f"Status: {'Presenting' if self.state.is_presenting else 'Idle'} | "
            f"Slide: {self.state.current_slide} | "
            f"Laser: {'ON' if self.state.laser_active else 'OFF'}"
        )
        self.presentation_area.visible = self.state.is_presenting
        self.presentation_area.content.mouse_cursor = (
            ft.MouseCursor.CLICK if self.state.laser_active else ft.MouseCursor.BASIC
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

    def on_laser_drag(self, e: DragUpdateEvent):
        print("Drag fired! global_pos:", e.global_position)
        print("local_delta:", e.local_delta)
        print("global_delta:", e.global_delta)
        if not self.state.laser_active:
            return
        
        if self.state.laser_pos is None:
            self.state.laser_pos = (e.global_position.x, e.global_position.y)
        else:
            delta = e.local_delta or e.global_delta
            if delta:
                self.state.laser_pos = (
                    self.state.laser_pos[0] + delta.x,
                    self.state.laser_pos[1] + delta.y
                )
        print(f"Laser at {self.state.laser_pos}")
        self.page.update()

def main(page: ft.Page):
    PresentationApp(page)

if __name__ == "__main__":
    ft.run(main)