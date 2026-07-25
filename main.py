"""
main.py

Entry point for the Drug Information Database desktop app (Flet).

Run with:
    pip install flet
    python main.py

Swap in your real dataset by replacing Research_Data.py (same `drug_data`
variable name) -- see the docstring there for the expected schema.
"""

import flet as ft

from Research_Data import drug_data
from drug_data_manager import DrugDataManager
from theme import get_palette
import top_nav
import sidebar
import profile

FONT_FAMILY = "Segoe UI"


class AppState:
    def __init__(self):
        self.dark_mode = False
        self.search = ""
        self.system = "All Systems"
        self.sort_desc = False
        self.favorites_only = False
        self.selected_name = None


def main(page: ft.Page):
    page.title = "Drug Information Database"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {}
    page.padding = 0
    page.window.width = 1280
    page.window.height = 800
    page.window.min_width = 980
    page.window.min_height = 620

    dm = DrugDataManager(drug_data)
    state = AppState()

    body_container = ft.Container(expand=True)
    root_row = ft.Row([], spacing=0, expand=True)
    top_bar_holder = ft.Container()
    page.add(ft.Column([top_bar_holder, root_row], spacing=0, expand=True))

    def current_colors():
        return get_palette(state.dark_mode)

    def current_drug():
        if not state.selected_name:
            return None
        for d in dm.entries:
            if d["Generic_Name"] == state.selected_name:
                return d
        return None

    def select_drug(name: str):
        state.selected_name = name
        dm.mark_viewed(name)
        render()

    def on_search_change(e):
        state.search = e.control.value
        render()

    def on_system_change(e):
        state.system = e.control.value
        render()

    def on_sort_toggle(e):
        state.sort_desc = not state.sort_desc
        render()

    def on_favorites_toggle(e):
        state.favorites_only = not state.favorites_only
        render()

    def on_toggle_favorite(e):
        if state.selected_name:
            dm.toggle_favorite(state.selected_name)
            render()

    def on_theme_toggle(e):
        state.dark_mode = not state.dark_mode
        page.theme_mode = ft.ThemeMode.DARK if state.dark_mode else ft.ThemeMode.LIGHT
        render()

    def on_settings_click(e):
        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Settings"),
                content=ft.Text(
                    "This offline prototype currently exposes appearance "
                    "(light/dark) as its only setting. Extend this dialog "
                    "for additional preferences as needed."
                ),
            )
        )

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "/" and not e.ctrl and not e.alt and not e.meta:
            # focus search — handled via rebuilding with autofocus is heavy,
            # so we just no-op here; left as an extension point.
            pass
        elif e.key == "Escape":
            if state.search:
                state.search = ""
                render()

    page.on_keyboard_event = on_keyboard

    def render():
        colors = current_colors()
        page.bgcolor = colors["bg"]

        results = dm.search(
            query=state.search,
            system=state.system,
            favorites_only=state.favorites_only,
            sort_desc=state.sort_desc,
        )

        # Keep selection valid; auto-select first result if nothing/invalid selected.
        names_in_results = [d["Generic_Name"] for d in results]
        if state.selected_name not in names_in_results:
            state.selected_name = names_in_results[0] if names_in_results else None
            if state.selected_name:
                dm.mark_viewed(state.selected_name)

        drug = current_drug()

        if drug:
            main_content = profile.build_profile(
                drug,
                colors,
                dm.is_favorite(drug["Generic_Name"]),
                on_toggle_favorite,
            )
        elif dm.total_count() == 0:
            main_content = profile.build_welcome(colors)
        else:
            main_content = profile.build_no_results(colors)

        content_area = ft.Container(
            content=main_content,
            expand=True,
            padding=ft.Padding(28, 24, 28, 24),
            bgcolor=colors["bg"],
        )

        sb = sidebar.build_sidebar(
            colors=colors,
            systems=dm.systems(),
            total_count=dm.total_count(),
            filtered_count=len(results),
            drugs=results,
            selected_name=state.selected_name,
            favorites=dm.favorite_drugs(),
            recently_viewed=dm.recently_viewed_drugs(),
            search_value=state.search,
            system_value=state.system,
            sort_desc=state.sort_desc,
            favorites_only=state.favorites_only,
            on_search_change=on_search_change,
            on_system_change=on_system_change,
            on_sort_toggle=on_sort_toggle,
            on_favorites_toggle=on_favorites_toggle,
            on_select_drug=select_drug,
        )

        top_bar_holder.content = top_nav.build_top_nav(
            colors, state.dark_mode, on_theme_toggle, on_settings_click
        )

        root_row.controls = [sb, content_area]
        page.update()

    render()


if __name__ == "__main__":
    ft.run(main)

