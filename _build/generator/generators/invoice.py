"""Générateur de factures PDF."""
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from faker import Faker
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

from companies import Company, random_company
from generators.base import BaseGenerator

_fake = Faker("fr_FR")

PRODUCT_CATALOG = [
    ("Prestation de conseil", 150.00),
    ("Développement logiciel (j/h)", 650.00),
    ("Formation (demi-journée)", 480.00),
    ("Licence logicielle annuelle", 290.00),
    ("Maintenance corrective", 120.00),
    ("Audit technique", 800.00),
    ("Hébergement serveur (mois)", 75.00),
    ("Rédaction documentation", 200.00),
    ("Intégration API tierce", 350.00),
    ("Support prioritaire (mois)", 180.00),
]


class InvoiceGenerator(BaseGenerator):
    """Génère des factures PDF au format A4."""

    LABEL = "facture"

    def generate(self, company: Company, seed: Optional[int] = None) -> Path:
        rng = random.Random(seed)
        if seed is not None:
            Faker.seed(seed)

        invoice_number = f"FA-{rng.randint(2020, 2026)}-{rng.randint(1000, 9999)}"
        invoice_date = date.today() - timedelta(days=rng.randint(0, 365))
        due_date = invoice_date + timedelta(days=rng.choice([30, 45, 60]))

        client = random_company(seed=rng.randint(0, 9999) if seed else None)

        # Lignes de la facture
        n_lines = rng.randint(2, 7)
        lines = []
        for _ in range(n_lines):
            product, unit_price = rng.choice(PRODUCT_CATALOG)
            qty = rng.randint(1, 10)
            unit_price *= rng.uniform(0.8, 1.2)
            total = qty * unit_price
            lines.append((product, qty, unit_price, total))

        subtotal = sum(l[3] for l in lines)
        tva_rate = rng.choice([0.20, 0.10, 0.055])
        tva = subtotal * tva_rate
        grand_total = subtotal + tva

        filepath = self.output_dir / f"{invoice_number}.pdf"
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        r, g, b = company.primary_color
        primary = colors.Color(r, g, b)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "title", parent=styles["Title"],
            textColor=primary, fontSize=18, spaceAfter=6
        )
        normal = styles["Normal"]
        small = ParagraphStyle("small", parent=normal, fontSize=8)

        story = []

        # En-tête émetteur
        story.append(Paragraph(company.name.upper(), title_style))
        story.append(Paragraph(
            f"{company.address} — {company.zip_code} {company.city}", small
        ))
        story.append(Paragraph(
            f"Tél : {company.phone} | {company.email}", small
        ))
        story.append(Paragraph(
            f"SIRET : {company.siret} | TVA : {company.tva_number}", small
        ))
        story.append(Spacer(1, 0.5 * cm))

        # Titre document
        doc_title = ParagraphStyle(
            "doc_title", parent=styles["Heading1"],
            textColor=primary, fontSize=22
        )
        story.append(Paragraph("FACTURE", doc_title))
        story.append(Spacer(1, 0.3 * cm))

        # Méta facture + client
        meta_data = [
            [Paragraph("<b>N° Facture :</b>", normal), invoice_number,
             Paragraph("<b>Client :</b>", normal), client.name],
            [Paragraph("<b>Date :</b>", normal), invoice_date.strftime("%d/%m/%Y"),
             "", f"{client.address}"],
            [Paragraph("<b>Échéance :</b>", normal), due_date.strftime("%d/%m/%Y"),
             "", f"{client.zip_code} {client.city}"],
        ]
        meta_table = Table(meta_data, colWidths=[3 * cm, 4 * cm, 2.5 * cm, 7 * cm])
        meta_table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.6 * cm))

        # Tableau des lignes
        header = ["Désignation", "Qté", "P.U. HT (€)", "Total HT (€)"]
        table_data = [header] + [
            [desc, str(qty), f"{pu:,.2f}", f"{tot:,.2f}"]
            for desc, qty, pu, tot in lines
        ]
        col_widths = [9 * cm, 2 * cm, 3 * cm, 3 * cm]
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4 * cm))

        # Totaux
        totals = [
            ["", "", "Sous-total HT :", f"{subtotal:,.2f} €"],
            ["", "", f"TVA ({tva_rate*100:.0f}%) :", f"{tva:,.2f} €"],
            ["", "", Paragraph("<b>TOTAL TTC :</b>", normal), Paragraph(f"<b>{grand_total:,.2f} €</b>", normal)],
        ]
        totals_table = Table(totals, colWidths=[9 * cm, 2 * cm, 3 * cm, 3 * cm])
        totals_table.setStyle(TableStyle([
            ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LINEABOVE", (2, 2), (-1, 2), 1, primary),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.8 * cm))

        # Pied de page
        footer_style = ParagraphStyle("footer", parent=small, textColor=colors.grey)
        story.append(Paragraph(
            "Règlement par virement bancaire. Tout retard de paiement entraîne des pénalités "
            "de 3 fois le taux d'intérêt légal en vigueur.",
            footer_style
        ))

        doc.build(story)
        return filepath
