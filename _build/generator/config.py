"""Configuration globale du générateur."""
from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
LOGOS_DIR = ASSETS_DIR / "logos"
FONTS_DIR = ASSETS_DIR / "fonts"
OUTPUT_DIR = BASE_DIR / "output"

# Crée les répertoires s'ils n'existent pas
for _dir in (LOGOS_DIR, FONTS_DIR, OUTPUT_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# Locale Faker
FAKER_LOCALE = "fr_FR"

# Marges (en points, 1pt = 1/72 inch)
PAGE_MARGIN = 50
