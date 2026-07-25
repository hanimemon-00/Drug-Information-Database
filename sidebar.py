"""
sidebar.py

Builds the left sidebar: search field, system filter, sort toggle,
favorites shortcut list, recently-viewed shortcut list, the scrollable
drug list itself, and the total drug count footer.
"""

import flet as ft

FONT_FAMILY = "Segoe UI"


def build_sidebar(
    colors: dict,
    systems: list,
    total_count: int,
    filtered_count: int,
    drugs: list,
    selected_name: str,
    favorites: list,
    recently_viewed: list,
    search_value: str,
    system_value: str,
    sort_desc: bool,
    favorites_only: bool,
    on_search_change,
    on_system_change,
    on_sort_toggle,
    on_favorites_toggle,
    on_select_drug,
) -> ft.Control:
    search_field = ft.TextField(
        value=search_value,
        hint_text="Enter Generic Name",
        prefix_icon=ft.Icons.SEARCH,
        border_color=colors["border"],
        focused_border_color=colors["accent"],
        bgcolor=colors["sidebar_soft"],
        color=colors["text_on_dark"],
        hint_style=ft.TextStyle(color=colors["text_muted_on_dark"]),
        border_radius=10,
        content_padding=ft.Padding(12, 10, 12, 10),
        on_change=on_search_change,
        dense=True,
        autofocus=True if search_value else False,  # 👈 ADD THIS LINE
    )

    system_dropdown = ft.Dropdown(
        value=system_value,
        options=[ft.dropdown.Option("All Systems")]
        + [ft.dropdown.Option(s) for s in systems],
        border_color=colors["border"],
        bgcolor=colors["sidebar_soft"],
        color=colors["text_on_dark"],
        border_radius=10,
        content_padding=ft.Padding(12, 8, 12, 8),
        text_size=13,
        on_change=on_system_change,
        dense=True,
    )

    sort_button = ft.IconButton(
        icon=ft.Icons.SORT_BY_ALPHA,
        icon_color=colors["accent"] if sort_desc else colors["text_muted_on_dark"],
        tooltip="Toggle A-Z / Z-A sort",
        on_click=on_sort_toggle,
    )

    favorites_button = ft.IconButton(
        icon=ft.Icons.FAVORITE if favorites_only else ft.Icons.FAVORITE_BORDER,
        icon_color="#F87171" if favorites_only else colors["text_muted_on_dark"],
        tooltip="Show favorites only",
        on_click=on_favorites_toggle,
    )

    def section_label(text):
        return ft.Text(
            text.upper(),
            size=10,
            weight=ft.FontWeight.BOLD,
            color=colors["text_muted_on_dark"],
            font_family=FONT_FAMILY,
        )

    quick_lists = []
    if favorites:
        quick_lists.append(section_label("Favorites"))
        quick_lists += [
            ft.ListTile(
                title=ft.Text(d["Generic_Name"], size=12, color=colors["text_on_dark"], font_family=FONT_FAMILY, max_lines=1),
                leading=ft.Icon(ft.Icons.STAR, size=16, color="#FBBF24"),
                dense=True,
                content_padding=ft.Padding(4, 0, 4, 0),
                on_click=lambda e, n=d["Generic_Name"]: on_select_drug(n),
            )
            for d in favorites[:5]
        ]

    if recently_viewed:
        quick_lists.append(section_label("Recently Viewed"))
        quick_lists += [
            ft.ListTile(
                title=ft.Text(d["Generic_Name"], size=12, color=colors["text_on_dark"], font_family=FONT_FAMILY, max_lines=1),
                leading=ft.Icon(ft.Icons.HISTORY, size=16, color=colors["text_muted_on_dark"]),
                dense=True,
                content_padding=ft.Padding(4, 0, 4, 0),
                on_click=lambda e, n=d["Generic_Name"]: on_select_drug(n),
            )
            for d in recently_viewed[:5]
        ]

    drug_list_items = []
    for d in drugs:
        selected = d["Generic_Name"] == selected_name
        drug_list_items.append(
            ft.ListTile(
                title=ft.Text(
                    d["Generic_Name"],
                    size=13,
                    color=colors["text_on_dark"] if not selected else "#FFFFFF",
                    weight=ft.FontWeight.W_600 if selected else ft.FontWeight.NORMAL,
                    font_family=FONT_FAMILY,
                ),
                subtitle=ft.Text(
                    d.get("Disease", ""),
                    size=11,
                    color=colors["text_muted_on_dark"],
                    max_lines=1,
                ),
                selected=selected,
                selected_tile_color=colors["selected"],
                bgcolor=colors["sidebar_bg"] if not selected else None,
                dense=True,
                on_click=lambda e, n=d["Generic_Name"]: on_select_drug(n),
            )
        )

    if not drug_list_items:
        drug_list_items = [
            ft.Container(
                content=ft.Text(
                    "No drugs match your filters.",
                    size=12,
                    color=colors["text_muted_on_dark"],
                    font_family=FONT_FAMILY,
                ),
                padding=16,
            )
        ]

    return ft.Container(
        width=320,
        bgcolor=colors["sidebar_bg"],
        padding=ft.Padding(0, 0, 0, 0),
        content=ft.Column(
            [
                ft.Container(
                    padding=ft.Padding(20, 24, 20, 4),
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=colors["accent"], size=22),
                                    ft.Text(
                                        "MedInfo",
                                        size=19,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF",
                                        font_family=FONT_FAMILY,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Text(
                                "PHARMACOLOGY REFERENCE DATABASE",
                                size=9,
                                color=colors["accent"],
                                font_family=FONT_FAMILY,
                            ),
                        ],
                        spacing=4,
                    ),
                ),
                ft.Container(
                    padding=ft.Padding(20, 14, 20, 0),
                    content=search_field,
                ),
                ft.Container(
                    padding=ft.Padding(20, 10, 20, 0),
                    content=ft.Column(
                        [
                            section_label("Filter by System"),
                            ft.Row(
                                [
                                    ft.Container(content=system_dropdown, expand=True),
                                    sort_button,
                                    favorites_button,
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=6,
                    ),
                ),
                ft.Container(
                    content=ft.Divider(color=colors["border"], height=1),
                    padding=ft.Padding(20, 12, 20, 0),
                )
                if quick_lists
                else ft.Container(),
                ft.Container(
                    padding=ft.Padding(12, 0, 12, 0),
                    content=ft.Column(quick_lists, spacing=0),
                )
                if quick_lists
                else ft.Container(),
                ft.Container(
                    content=ft.Divider(color=colors["border"], height=1),
                    padding=ft.Padding(20, 8, 20, 0),
                ),
                ft.Container(
                    padding=ft.Padding(8, 4, 8, 0),
                    content=ft.Column(
                        drug_list_items,
                        spacing=0,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                ),
                ft.Container(
                    padding=ft.Padding(20, 8, 20, 14),
                    content=ft.Text(
                        f"{filtered_count} of {total_count} drugs",
                        size=11,
                        color=colors["text_muted_on_dark"],
                        font_family=FONT_FAMILY,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )