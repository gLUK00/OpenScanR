"""Générateur de lettres manuscrites simulées."""
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from faker import Faker
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from config import FONTS_DIR

_fake = Faker("fr_FR")

# Polices manuscrites candidates (présentes dans assets/fonts/)
# Si absentes, repli sur Helvetica-Oblique
HANDWRITTEN_FONTS = [
    "DancingScript",
    "Caveat",
    "PatrickHand",
]

LETTER_SUBJECTS = [
    "Demande d'information",
    "Réclamation",
    "Remerciements",
    "Candidature spontanée",
    "Demande de rendez-vous",
    "Suivi de dossier",
    "Signalement d'anomalie",
    "Retour d'expérience",
]

LETTER_PARAGRAPHS = [
    "Je me permets de vous écrire afin de vous faire part de ma situation.",
    "Suite à notre entretien téléphonique du mois dernier, je souhaitais revenir vers vous.",
    "Je tiens tout d'abord à vous remercier pour la qualité de votre accueil.",
    "Dans l'attente de votre réponse, je reste disponible pour tout complément d'information.",
    "Je vous prie de bien vouloir excuser le délai dans lequel je vous adresse ce courrier.",
    "Pourriez-vous m'indiquer les démarches à suivre pour résoudre cette situation ?",
    "Je souhaite attirer votre attention sur un point qui me semble important.",
    "Je reste à votre disposition pour convenir d'un rendez-vous à votre convenance.",
    "Veuillez trouver ci-joint les documents que vous m'avez demandés.",
    "Je vous confirme ma disponibilité pour la date que vous m'avez proposée.",
]


def _register_font(font_name: str) -> Optional[str]:
    """Tente d'enregistrer une police TTF depuis assets/fonts/. Retourne le nom si ok."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    ttf_path = FONTS_DIR / f"{font_name}-Regular.ttf"
    if ttf_path.exists():
        try:
            pdfmetrics.registerFont(TTFont(font_name, str(ttf_path)))
            return font_name
        except Exception:
            pass
    return None


class HandwrittenLetterGenerator:
    """Génère des lettres à l'aspect manuscrit (texte + police TTF ou oblique)."""

    LABEL = "lettre_manuscrite"

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, seed: Optional[int] = None) -> Path:
        rng = random.Random(seed)
        if seed is not None:
            Faker.seed(seed)

        # Choisir la police
        font_name = "Helvetica-Oblique"
        for candidate in rng.sample(HANDWRITTEN_FONTS, len(HANDWRITTEN_FONTS)):
            registered = _register_font(candidate)
            if registered:
                font_name = registered
                break

        letter_id = f"LM-{rng.randint(1000, 9999)}"
        letter_date = date.today() - timedelta(days=rng.randint(0, 730))
        sender = _fake.name()
        sender_address = _fake.address().replace("\n", ", ")
        recipient = _fake.name()
        recipient_company = _fake.company()
        subject = rng.choice(LETTER_SUBJECTS)

        # Corps : 3 à 6 paragraphes aléatoires
        n_para = rng.randint(3, 6)
        paragraphs = rng.choices(LETTER_PARAGRAPHS, k=n_para)

        filepath = self.output_dir / f"{letter_id}.pdf"
        w, h = A4
        c = canvas.Canvas(str(filepath), pagesize=A4)

        # Fond légèrement beige pour simuler papier
        c.setFillColorRGB(0.99, 0.97, 0.92)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # Légère texture de lignes
        c.setStrokeColorRGB(0.88, 0.86, 0.80)
        c.setLineWidth(0.3)
        y_line = h - 3 * cm
        while y_line > 2 * cm:
            c.line(1.5 * cm, y_line, w - 1.5 * cm, y_line)
            y_line -= 0.75 * cm

        margin_x = 2.5 * cm
        y = h - 3 * cm

        # En-tête expéditeur (haut gauche)
        c.setFillColorRGB(0.15, 0.15, 0.15)
        c.setFont(font_name, 11)
        c.drawString(margin_x, y, sender)
        y -= 0.75 * cm
        c.setFont(font_name, 9)
        c.drawString(margin_x, y, sender_address)
        y -= 1.2 * cm

        # Date (haut droit)
        date_str = f"Le {letter_date.strftime('%d %B %Y')}"
        c.setFont(font_name, 10)
        c.drawRightString(w - margin_x, h - 3 * cm, date_str)

        # Destinataire
        c.setFont(font_name, 10)
        c.drawString(w * 0.55, h - 4.5 * cm, recipient)
        c.setFont(font_name, 9)
        c.drawString(w * 0.55, h - 4.5 * cm - 0.6 * cm, recipient_company)
        y = h - 6.5 * cm

        # Objet
        c.setFont(font_name, 10)
        c.drawString(margin_x, y, f"Objet : {subject}")
        y -= 1.0 * cm

        # Corps de la lettre
        line_height = 0.75 * cm
        for para in paragraphs:
            # Découpe simple des lignes (wrap manuel ~80 chars)
            words = para.split()
            current_line = ""
            for word in words:
                test = f"{current_line} {word}".strip()
                # estimation : 1 char ≈ 0.22 cm à 10pt
                if len(test) * 0.22 * cm > (w - 2 * margin_x):
                    c.setFont(font_name, 10)
                    c.drawString(margin_x, y, current_line)
                    y -= line_height
                    current_line = word
                    if y < 3 * cm:
                        c.showPage()
                        c.setFillColorRGB(0.99, 0.97, 0.92)
                        c.rect(0, 0, w, h, fill=1, stroke=0)
                        y = h - 2.5 * cm
                else:
                    current_line = test
            if current_line:
                c.setFont(font_name, 10)
                c.drawString(margin_x, y, current_line)
                y -= line_height
            y -= 0.3 * cm  # espace entre paragraphes

        # Formule de politesse
        y -= 0.5 * cm
        politesse = "Dans l'attente de votre réponse, veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
        c.setFont(font_name, 10)
        c.drawString(margin_x, y, politesse[:70])
        y -= line_height
        c.drawString(margin_x, y, politesse[70:])
        y -= 1.5 * cm

        # Signature
        c.setFont(font_name, 13)
        c.drawString(margin_x + 8 * cm, y, sender)

        c.save()
        return filepath
