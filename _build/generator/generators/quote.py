"""Générateur de devis PDF."""
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
from generators.invoice import PRODUCT_CATALOG

_fake = Faker("fr_FR")


class QuoteGenerator:
    """Génère des devis PDF au format A4 (structure proche de la facture)."""

    LABEL = "devis"

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, company: Company, seed: Optional[int] = None) -> Path:
        rng = random.Random(seed)
        if seed is not None:
            Faker.seed(seed)

        quote_number = f"DV-{rng.randint(2020, 2026)}-{rng.randint(1000, 9999)}"
        quote_date = date.today() - timedelta(days=rng.randint(0, 365))
        validity_date = quote_date + timedelta(days=rng.choice([30, 60, 90]))

        client = random_company(seed=rng.randint(0, 9999) if seed else None)

        n_lines = rng.randint(2, 8)
        lines = []
        for _ in range(n_lines):
            product, unit_price = rng.choice(PRODUCT_CATALOG)
            qty = rng.randint(1, 10)
            unit_price *= rng.uniform(0.8, 1.2)
            total = qty * unit_price
            lines.append((product, qty, unit_price, total))

        subtotal = sum(l[3] for l in lines)
        discount_pct = rng.choice([0, 0, 0, 5, 10])  # rabais éventuel
        discount = subtotal * discount_pct / 100
        subtotal_after = subtotal - discount
        tva_rate = rng.choice([0.20, 0.10])
        tva = subtotal_after * tva_rate
        grand_total = subtotal_after + tva

        filepath = self.output_dir / f"{quote_number}.pdf"
        r, g, b = company.primary_color
        primary = colors.Color(r, g, b)

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

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
        story.append(Paragraph("DEVIS", doc_title))
        story.append(Spacer(1, 0.3 * cm))

        # Informations
        meta_data = [
            [Paragraph("<b>N° Devis :</b>", normal), quote_number,
             Paragraph("<b>Client :</b>", normal), client.name],
            [Paragraph("<b>Date :</b>", normal), quote_date.strftime("%d/%m/%Y"),
             "", f"{client.address}"],
            [Paragraph("<b>Validité :</b>", normal), validity_date.strftime("%d/%m/%Y"),
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

        # Tableau lignes
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
        ]
        if discount_pct > 0:
            totals.append(["", "", f"Remise ({discount_pct}%) :", f"-{discount:,.2f} €"])
        totals += [
            ["", "", f"TVA ({tva_rate*100:.0f}%) :", f"{tva:,.2f} €"],
            ["", "", Paragraph("<b>TOTAL TTC :</b>", normal), Paragraph(f"<b>{grand_total:,.2f} €</b>", normal)],
        ]
        totals_table = Table(totals, colWidths=[9 * cm, 2 * cm, 3 * cm, 3 * cm])
        totals_table.setStyle(TableStyle([
            ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LINEABOVE", (2, -1), (-1, -1), 1, primary),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.8 * cm))

        # Zone signature
        sig_data = [
            [Paragraph("<i>Bon pour accord — Date et signature du client :</i>", small), ""],
            ["", ""],
            ["", ""],
        ]
        sig_table = Table(sig_data, colWidths=[10 * cm, 7 * cm])
        sig_table.setStyle(TableStyle([
            ("BOX", (1, 0), (1, -1), 1, colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("MINROWHEIGHT", (0, 1), (-1, -1), 30),
        ]))
        story.append(sig_table)
        story.append(Spacer(1, 0.4 * cm))

        footer_style = ParagraphStyle("footer", parent=small, textColor=colors.grey)
        story.append(Paragraph(
            f"Ce devis est valable jusqu'au {validity_date.strftime('%d/%m/%Y')}. "
            "La commande sera confirmée à réception du bon pour accord signé.",
            footer_style
        ))

        doc.build(story)
        return filepath
