"""
theme.py

Central color palette and typography for the Drug Information Database app.
Two palettes are provided (light / dark); `get_palette(dark)` returns the
active one as a plain dict so the rest of the app never has to branch on
mode itself.
"""

FONT_FAMILY = "Segoe UI"

LIGHT = {
    "bg": "#F8FAFC",             # main content background
    "surface": "#FFFFFF",        # cards / panels
    "sidebar_bg": "#1F2937",     # dark sidebar even in light mode (per spec)
    "sidebar_soft": "#374151",
    "header_bg": "#1F2937",      # drug profile header banner

    "accent": "#2563EB",         # muted / professional blue
    "accent_soft": "#EFF6FF",

    "text_primary": "#1E293B",
    "text_secondary": "#64748B",
    "text_on_dark": "#F8FAFC",
    "text_muted_on_dark": "#9CA3AF",

    "border": "#E2E8F0",
    "selected": "#334155",

    "success": "#059669",
    "success_soft": "#ECFDF5",
    "warn": "#D97706",
    "warn_soft": "#FFFBEB",
    "danger": "#DC2626",
    "danger_soft": "#FEF2F2",
    "purple": "#7C3AED",
    "purple_soft": "#F3E8FF",
    "teal": "#0D9488",
    "teal_soft": "#CCFBF1",
}

DARK = {
    "bg": "#111827",
    "surface": "#1F2937",
    "sidebar_bg": "#0B1220",
    "sidebar_soft": "#1F2937",
    "header_bg": "#1F2937",

    "accent": "#2563EB",
    "accent_soft": "#1E3A8A",

    "text_primary": "#F9FAFB",
    "text_secondary": "#9CA3AF",
    "text_on_dark": "#F9FAFB",
    "text_muted_on_dark": "#9CA3AF",

    "border": "#2D3748",
    "selected": "#334155",

    "success": "#10B981",
    "success_soft": "#064E3B",
    "warn": "#F59E0B",
    "warn_soft": "#451A03",
    "danger": "#EF4444",
    "danger_soft": "#450A0A",
    "purple": "#A78BFA",
    "purple_soft": "#3B0764",
    "teal": "#2DD4BF",
    "teal_soft": "#134E4A",
}


def get_palette(dark: bool) -> dict:
    return DARK if dark else LIGHT