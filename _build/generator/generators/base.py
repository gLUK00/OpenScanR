"""Classe de base pour tous les générateurs de documents."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from companies import Company


class BaseGenerator(ABC):
    """Génère un document PDF dans output_dir."""

    PAGE_SIZE = A4

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def generate(self, company: Company, seed: Optional[int] = None) -> Path:
        """Génère un fichier PDF et retourne son chemin."""

    def _new_canvas(self, filepath: Path) -> canvas.Canvas:
        return canvas.Canvas(str(filepath), pagesize=self.PAGE_SIZE)

    def _draw_company_header(
        self,
        c: canvas.Canvas,
        company: Company,
        margin: int = 50,
    ) -> float:
        """
        Dessine l'en-tête société (nom + coordonnées + bandeau couleur).
        Retourne la position Y courante après l'en-tête.
        """
        w, h = self.PAGE_SIZE
        r, g, b = company.primary_color

        # Bandeau coloré en haut
        c.setFillColorRGB(r, g, b)
        c.rect(0, h - 80, w, 80, fill=1, stroke=0)

        # Nom de la société
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(margin, h - 52, company.name.upper())

        # Coordonnées sur fond blanc
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 8)
        y = h - 95
        for line in (
            f"{company.address}",
            f"{company.zip_code} {company.city}",
            f"Tél : {company.phone}  |  {company.email}",
            f"SIRET : {company.siret}  |  TVA : {company.tva_number}",
        ):
            c.drawString(margin, y, line)
            y -= 12

        return y - 10  # espace supplémentaire avant le contenu
