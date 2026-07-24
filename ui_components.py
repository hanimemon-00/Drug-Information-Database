"""
ui_components.py

Small, reusable visual building blocks used across the app: pill tags,
expandable info cards, and a couple of styled buttons. Kept separate so
sidebar.py / profile.py stay focused on layout rather than widget details.
"""

import flet as ft

FONT_FAMILY = "Segoe UI"

# How long a section's text can be before it collapses into an
# expandable tile instead of always being fully shown.
LONG_TEXT_THRESHOLD = 220


def border_all(width: float, color: str) -> ft.Border:
    side = ft.BorderSide(width, color)
    return ft.Border(top=side, right=side, bottom=side, left=side)


def tag(text: str, color: str, bgcolor: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, size=11, weight=ft.FontWeight.W_600, color=color),
        bgcolor=bgcolor,
        padding=ft.Padding(10, 5, 10, 5),
        border_radius=999,
        border=border_all(1, color),
    )


def section_icon(key: str) -> str:
    icons = {
        "mechanism": ft.Icons.SETTINGS_SUGGEST_OUTLINED,
        "dosage": ft.Icons.MEDICATION_OUTLINED,
        "indications": ft.Icons.CHECK_CIRCLE_OUTLINE,
        "contraindications": ft.Icons.BLOCK,
        "warnings": ft.Icons.WARNING_AMBER_OUTLINED,
        "precautions": ft.Icons.SHIELD_OUTLINED,
        "drug_interactions": ft.Icons.SYNC_ALT,
        "food_interactions": ft.Icons.RESTAURANT_OUTLINED,
        "adverse_effects": ft.Icons.SICK_OUTLINED,
        "toxicity": ft.Icons.DANGEROUS_OUTLINED,
        "overdose": ft.Icons.EMERGENCY_OUTLINED,
        "monitoring": ft.Icons.MONITOR_HEART_OUTLINED,
        "storage": ft.Icons.INVENTORY_2_OUTLINED,
        "counseling": ft.Icons.CHAT_OUTLINED,
        "combination": ft.Icons.SCIENCE_OUTLINED,
        "pregnancy": ft.Icons.PREGNANT_WOMAN_OUTLINED,
        "breastfeeding": ft.Icons.CHILD_CARE_OUTLINED,
        "pediatric": ft.Icons.CHILD_FRIENDLY_OUTLINED,
        "geriatric": ft.Icons.ELDERLY_OUTLINED,
        "hepatic": ft.Icons.WATER_DROP_OUTLINED,
        "renal": ft.Icons.OPACITY_OUTLINED,
    }
    return icons.get(key, ft.Icons.INFO_OUTLINE)


def section_card(
    label: str,
    value: str,
    accent: str,
    soft_bg: str,
    surface: str,
    text_color: str,
    icon_key: str,
) -> ft.Control:
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(section_icon(icon_key), color=accent, size=18),
                ft.Text(
                    label.upper(),
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=accent,
                    font_family=FONT_FAMILY,
                ),
            ],
            spacing=8,
        ),
        bgcolor=soft_bg,
        padding=ft.Padding(16, 10, 16, 10),
        border_radius=ft.BorderRadius(top_left=12, top_right=12, bottom_left=0, bottom_right=0),
    )

    body_text = ft.Text(
        value,
        size=13,
        color=text_color,
        font_family=FONT_FAMILY,
        selectable=True,
    )
    body = ft.Container(
        content=body_text,
        padding=ft.Padding(16, 14, 16, 16),
    )

    if len(value) > LONG_TEXT_THRESHOLD:
        # Long content collapses by default into an expandable tile.
        tile = ft.ExpansionTile(
            title=ft.Row(
                [
                    ft.Icon(section_icon(icon_key), color=accent, size=18),
                    ft.Text(
                        label.upper(),
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=accent,
                        font_family=FONT_FAMILY,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=soft_bg,
            collapsed_bgcolor=soft_bg,
            controls=[
                ft.Container(
                    content=body_text,
                    padding=ft.Padding(16, 4, 16, 16),
                )
            ],
        )
        return ft.Container(
            content=tile,
            bgcolor=surface,
            border_radius=12,
            border=border_all(1, accent + "33"),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

    return ft.Container(
        content=ft.Column([header, body], spacing=0),
        bgcolor=surface,
        border_radius=12,
        border=border_all(1, accent + "33"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )


def empty_state(icon, title: str, subtitle: str, text_color: str, muted_color: str) -> ft.Control:
    return ft.Column(
        [
            ft.Icon(icon, size=64, color=muted_color),
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=text_color, font_family=FONT_FAMILY),
            ft.Text(subtitle, size=13, color=muted_color, font_family=FONT_FAMILY),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        expand=True,
    )