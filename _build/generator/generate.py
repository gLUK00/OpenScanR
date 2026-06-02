#!/usr/bin/env python3
"""Point d'entrée CLI du générateur de documents synthétiques OpenScanR."""
import random
import sys
from pathlib import Path

import click

# Ajoute le répertoire courant au path pour les imports relatifs
sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR
from companies import random_company
from generators import InvoiceGenerator, QuoteGenerator, HandwrittenLetterGenerator


@click.command()
@click.option("--invoices", default=0, help="Nombre de factures à générer.")
@click.option("--quotes", default=0, help="Nombre de devis à générer.")
@click.option("--handwritten", default=0, help="Nombre de lettres manuscrites à générer.")
@click.option("--all", "generate_all", is_flag=True, help="Génère tous les types.")
@click.option("--count", default=5, show_default=True, help="Quantité par type (avec --all).")
@click.option("--seed", default=None, type=int, help="Graine aléatoire pour la reproductibilité.")
@click.option("--output", default=str(OUTPUT_DIR), show_default=True, help="Répertoire de sortie.")
def main(invoices, quotes, handwritten, generate_all, count, seed, output):
    """Génère des documents PDF synthétiques pour OpenScanR."""
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)

    if generate_all:
        invoices = quotes = handwritten = count

    if invoices == 0 and quotes == 0 and handwritten == 0:
        click.echo("Aucun document à générer. Utilisez --help pour voir les options.")
        return

    rng = random.Random(seed)

    def next_seed():
        return rng.randint(0, 999_999) if seed is not None else None

    total = 0

    # Factures
    if invoices > 0:
        inv_dir = out / "invoices"
        gen = InvoiceGenerator(inv_dir)
        click.echo(f"Génération de {invoices} facture(s)...")
        for i in range(invoices):
            company = random_company(seed=next_seed())
            path = gen.generate(company, seed=next_seed())
            click.echo(f"  [{i+1}/{invoices}] {path.name}")
            total += 1

    # Devis
    if quotes > 0:
        qt_dir = out / "quotes"
        gen = QuoteGenerator(qt_dir)
        click.echo(f"Génération de {quotes} devis...")
        for i in range(quotes):
            company = random_company(seed=next_seed())
            path = gen.generate(company, seed=next_seed())
            click.echo(f"  [{i+1}/{quotes}] {path.name}")
            total += 1

    # Lettres manuscrites
    if handwritten > 0:
        hw_dir = out / "handwritten"
        gen = HandwrittenLetterGenerator(hw_dir)
        click.echo(f"Génération de {handwritten} lettre(s) manuscrite(s)...")
        for i in range(handwritten):
            path = gen.generate(seed=next_seed())
            click.echo(f"  [{i+1}/{handwritten}] {path.name}")
            total += 1

    click.echo(f"\n✓ {total} document(s) généré(s) dans : {out}")


if __name__ == "__main__":
    main()
