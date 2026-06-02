# Générateur de documents synthétiques — OpenScanR

Génère des documents PDF artificiels variés pour alimenter le pipeline d'entraînement et de test d'OpenScanR.

## Types de documents générés
- **Factures** (`invoice`) : numéro, date, lignes articles, TVA, total
- **Devis** (`quote`) : structure similaire à la facture avec mention "DEVIS"
- **Lettres manuscrites** (`handwritten_letter`) : simulation de texte manuscrit via polices TTF

## Structure
```
generator/
├── README.md
├── requirements.txt
├── generate.py           # Point d'entrée CLI
├── config.py             # Configuration globale (chemins, graines, etc.)
├── assets/
│   ├── logos/            # Logos SVG/PNG des sociétés fictives
│   └── fonts/            # Polices manuscrites TTF
├── companies.py          # Données des sociétés fictives
├── generators/
│   ├── __init__.py
│   ├── base.py           # Classe abstraite BaseGenerator
│   ├── invoice.py        # Générateur de factures
│   ├── quote.py          # Générateur de devis
│   └── handwritten.py    # Générateur de lettres manuscrites
└── output/               # Répertoire de sortie des PDF (ignoré par git via _build/)
```

## Utilisation
```bash
# Installer les dépendances
pip install -r requirements.txt

# Générer 10 factures, 10 devis et 5 lettres manuscrites
python generate.py --invoices 10 --quotes 10 --handwritten 5

# Tout générer avec seed reproductible
python generate.py --all --count 20 --seed 42
```
