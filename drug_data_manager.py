"""
drug_data_manager.py

All non-visual logic for the app: loading and normalizing the local
drug_data list, instant search/filtering, system de-duplication, favorites,
and recently-viewed tracking. Kept free of any Flet/UI imports so it can be
tested and reused independently of the interface.
"""

from typing import Optional

# Short medical abbreviations that should stay upper-case rather than
# being title-cased (e.g. "cns" -> "CNS", not "Cns").
KNOWN_ACRONYMS = {
    "cns": "CNS",
    "gi": "GI",
    "gu": "GU",
    "ent": "ENT",
    "cvs": "CVS",
}


class DrugDataManager:
    def __init__(self, raw_data: list):
        # Only keep records that actually represent a drug (has a name)
        self.entries = [d for d in raw_data if d.get("Generic_Name")]

        # Build a case/whitespace-insensitive map of System -> canonical
        # display label, using the first-seen casing as the display form.
        self._system_display = {}
        for d in self.entries:
            raw_system = (d.get("System") or "").strip()
            if not raw_system:
                continue
            key = raw_system.lower()
            if key not in self._system_display:
                self._system_display[key] = KNOWN_ACRONYMS.get(key, raw_system.title())

        self.favorites: set[str] = set()
        self.recently_viewed: list[str] = []  # generic names, most recent first
        self._max_recent = 8

    # ------------------------------------------------------------------
    # Systems
    # ------------------------------------------------------------------
    def systems(self) -> list[str]:
        """Sorted, de-duplicated (case/whitespace-insensitive) system list."""
        return sorted(self._system_display.values())

    def _system_key(self, drug: dict) -> str:
        return (drug.get("System") or "").strip().lower()

    # ------------------------------------------------------------------
    # Search & filter
    # ------------------------------------------------------------------
    def search(
        self,
        query: str = "",
        system: Optional[str] = None,
        favorites_only: bool = False,
        sort_desc: bool = False,
    ) -> list[dict]:
        query = (query or "").strip().lower()
        system_key = None
        if system and system != "All Systems":
            system_key = system.strip().lower()

        results = []
        for d in self.entries:
            if system_key and self._system_key(d) != system_key:
                continue
            if favorites_only and d["Generic_Name"] not in self.favorites:
                continue
            if query:
                haystack = " ".join(
                    str(d.get(field, ""))
                    for field in (
                        "Generic_Name",
                        "Brand_Name",
                        "Disease",
                        "Therapeutic_Class",
                        "Pharmacological_Class",
                        "Affected_Organ",
                        "System",
                    )
                ).lower()
                if query not in haystack:
                    continue
            results.append(d)

        results.sort(key=lambda d: d["Generic_Name"].lower(), reverse=sort_desc)
        return results

    # ------------------------------------------------------------------
    # Favorites
    # ------------------------------------------------------------------
    def is_favorite(self, generic_name: str) -> bool:
        return generic_name in self.favorites

    def toggle_favorite(self, generic_name: str) -> bool:
        """Returns the new favorite state."""
        if generic_name in self.favorites:
            self.favorites.remove(generic_name)
            return False
        self.favorites.add(generic_name)
        return True

    def favorite_drugs(self) -> list[dict]:
        by_name = {d["Generic_Name"]: d for d in self.entries}
        return [by_name[name] for name in sorted(self.favorites) if name in by_name]

    # ------------------------------------------------------------------
    # Recently viewed
    # ------------------------------------------------------------------
    def mark_viewed(self, generic_name: str) -> None:
        if generic_name in self.recently_viewed:
            self.recently_viewed.remove(generic_name)
        self.recently_viewed.insert(0, generic_name)
        self.recently_viewed = self.recently_viewed[: self._max_recent]

    def recently_viewed_drugs(self) -> list[dict]:
        by_name = {d["Generic_Name"]: d for d in self.entries}
        return [by_name[name] for name in self.recently_viewed if name in by_name]

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------
    def total_count(self) -> int:
        return len(self.entries)