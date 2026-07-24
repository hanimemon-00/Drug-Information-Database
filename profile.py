"""
profile.py

Builds the main-content views: the welcome screen (nothing selected), the
"no results" state, and the full drug profile (header + section cards).

SECTIONS maps each display card to one or more possible dict keys, so the
app works whether Research_Data.py uses the original tkinter-prototype
schema (Drug_Action, Side_effects, ...) or the fuller schema described in
the app spec (Mechanism_of_Action, Adverse_Effects, ...). The first key
found with a non-empty value wins; a card is skipped entirely if none of
its keys have data.
"""

import flet as ft

from ui_components import tag, section_card, empty_state

FONT_FAMILY = "Segoe UI"

# (icon_key, display label, list of possible source keys, palette color key, palette soft-bg key)
SECTIONS = [
    ("mechanism", "Mechanism of Action", ["Drug_Action", "Mechanism_of_Action"], "accent", "accent_soft"),
    ("dosage", "Dosage", ["Dose", "Dosage"], "accent", "accent_soft"),
    ("indications", "Indications", ["Indications"], "success", "success_soft"),
    ("contraindications", "Contraindications", ["Contraindications"], "danger", "danger_soft"),
    ("warnings", "Warnings", ["Warnings", "Cautions"], "warn", "warn_soft"),
    ("precautions", "Precautions", ["Precautions"], "warn", "warn_soft"),
    ("drug_interactions", "Drug Interactions", ["Drug_Drug_interaction", "Drug_Interactions"], "danger", "danger_soft"),
    ("food_interactions", "Food Interactions", ["Food_Interactions"], "warn", "warn_soft"),
    ("adverse_effects", "Adverse Effects", ["Side_effects", "Adverse_Effects"], "warn", "warn_soft"),
    ("toxicity", "Toxicity", ["Toxicity"], "danger", "danger_soft"),
    ("overdose", "Overdose Management", ["Overdose_Management"], "danger", "danger_soft"),
    ("monitoring", "Monitoring Parameters", ["Monitoring_Parameters"], "teal", "teal_soft"),
    ("storage", "Storage Conditions", ["Storage_Conditions"], "teal", "teal_soft"),
    ("counseling", "Patient Counseling", ["Patient_Counseling"], "success", "success_soft"),
    ("combination", "Combination Therapy", ["Combination_Therapy"], "success", "success_soft"),
    ("pregnancy", "Pregnancy", ["Pregnancy"], "purple", "purple_soft"),
    ("breastfeeding", "Breastfeeding", ["Breast_Feeding", "Breastfeeding"], "purple", "purple_soft"),
    ("pediatric", "Pediatric Use", ["Pediatric_Use"], "purple", "purple_soft"),
    ("geriatric", "Geriatric / Elderly Use", ["Elderly", "Geriatric_Use"], "purple", "purple_soft"),
    ("hepatic", "Hepatic Impairment", ["Hepatic_Impairment"], "teal", "teal_soft"),
    ("renal", "Renal Impairment", ["Renal_Impairment"], "teal", "teal_soft"),
]


def _first_value(drug: dict, keys: list) -> str:
    for k in keys:
        v = drug.get(k)
        if v:
            return str(v)
    return ""


def build_welcome(colors: dict) -> ft.Control:
    return ft.Container(
        content=empty_state(
            ft.Icons.LOCAL_HOSPITAL,
            "Drug Information Database",
            "Search for a drug to begin.",
            colors["text_primary"],
            colors["text_secondary"],
        ),
        expand=True,
        alignment=ft.alignment.Alignment(0, 0),
    )


def build_no_results(colors: dict) -> ft.Control:
    return ft.Container(
        content=empty_state(
            ft.Icons.SEARCH_OFF,
            "No matching drugs",
            "Try a different search term or filter.",
            colors["text_primary"],
            colors["text_secondary"],
        ),
        expand=True,
        alignment=ft.alignment.Alignment(0, 0),
    )


def build_profile(
    drug: dict,
    colors: dict,
    is_favorite: bool,
    on_toggle_favorite,
) -> ft.Control:
    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    drug.get("Generic_Name", ""),
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=colors["text_on_dark"],
                                    font_family=FONT_FAMILY,
                                ),
                                ft.Text(
                                    drug.get("Brand_Name", ""),
                                    size=13,
                                    color=colors["text_muted_on_dark"],
                                    font_family=FONT_FAMILY,
                                )
                                if drug.get("Brand_Name")
                                else ft.Container(),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.STAR if is_favorite else ft.Icons.STAR_BORDER,
                            icon_color="#FBBF24" if is_favorite else colors["text_muted_on_dark"],
                            tooltip="Toggle favorite",
                            on_click=on_toggle_favorite,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Row(
                    [
                        tag(t, colors["text_on_dark"], "#00000030")
                        for t in [
                            drug.get("Disease"),
                            drug.get("System"),
                            drug.get("Affected_Organ"),
                        ]
                        if t
                    ],
                    spacing=8,
                    wrap=True,
                ),
                ft.Text(
                    " | ".join(
                        p
                        for p in [
                            drug.get("Therapeutic_Class"),
                            drug.get("Pharmacological_Class"),
                        ]
                        if p
                    ),
                    size=12,
                    italic=True,
                    color=colors["text_muted_on_dark"],
                    font_family=FONT_FAMILY,
                )
                if drug.get("Therapeutic_Class") or drug.get("Pharmacological_Class")
                else ft.Container(),
            ],
            spacing=12,
        ),
        bgcolor=colors["header_bg"],
        border_radius=14,
        padding=ft.Padding(24, 22, 24, 22),
    )

    cards = []
    for icon_key, label, keys, color_key, soft_key in SECTIONS:
        value = _first_value(drug, keys)
        if not value:
            continue
        cards.append(
            section_card(
                label,
                value,
                colors[color_key],
                colors[soft_key],
                colors["surface"],
                colors["text_primary"],
                icon_key,
            )
        )

    return ft.Column(
        [header, ft.Column(cards, spacing=10)],
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )