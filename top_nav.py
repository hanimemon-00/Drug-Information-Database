"""
top_nav.py

Top navigation bar. The primary search box lives in the sidebar (per the
spec's layout); this bar carries the app title, a theme toggle, and a
settings button (placeholder dialog, since no settings are specified
beyond appearance).
"""

import flet as ft

FONT_FAMILY = "Segoe UI"


def build_top_nav(colors: dict, dark_mode: bool, on_theme_toggle, on_settings_click) -> ft.Control:
    return ft.Container(
        bgcolor=colors["surface"],
        border=ft.Border(bottom=ft.BorderSide(1, colors["border"])),
        padding=ft.Padding(24, 12, 20, 12),
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=colors["accent"], size=20),
                        ft.Text(
                            "Drug Information Database",
                            size=15,
                            weight=ft.FontWeight.W_600,
                            color=colors["text_primary"],
                            font_family=FONT_FAMILY,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.DARK_MODE if not dark_mode else ft.Icons.LIGHT_MODE,
                            icon_color=colors["text_secondary"],
                            tooltip="Toggle dark / light mode",
                            on_click=on_theme_toggle,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.SETTINGS_OUTLINED,
                            icon_color=colors["text_secondary"],
                            tooltip="Settings",
                            on_click=on_settings_click,
                        ),
                    ],
                    spacing=4,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )