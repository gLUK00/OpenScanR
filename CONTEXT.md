# OpenScanR — Contexte du projet

## Description
OpenScanR est un logiciel de **reconnaissance et de classification de documents numérisés**.
Il vise à identifier automatiquement le type d'un document (facture, devis, lettre, etc.) à partir de son image ou de son contenu extrait.

## Objectifs principaux
- Ingestion de documents numérisés (images, PDF scannés)
- Extraction du contenu texte (OCR)
- Classification du type de document (facture, devis, lettre manuscrite, etc.)
- Export des métadonnées structurées

## Architecture (à affiner)
- `_build/generator/` : génération de documents PDF synthétiques pour l'entraînement et les tests

## Scripts utilitaires
| Script | Emplacement | Description |
|---|---|---|
| `download_fonts.sh` | `_build/generator/assets/fonts/` | Télécharge les 11 polices manuscrites TTF depuis Google Fonts (Caveat, DancingScript, PatrickHand, Sacramento, Pacifico, Satisfy, IndieFlower, Handlee, GloriaHallelujah, CoveredByYourGrace, SedgwickAve). Idempotent : ignore les fichiers déjà présents. |

```bash
# Usage
cd _build/generator/assets/fonts
bash download_fonts.sh
```

## État d'avancement
| Composant | Statut |
|---|---|
| Générateur de documents synthétiques | 🔧 En cours |
| Pipeline OCR | ⏳ À faire |
| Modèle de classification | ⏳ À faire |
| API / Interface utilisateur | ⏳ À faire |

## Décisions techniques
- Langage principal : Python
- Format de données synthétiques : PDF
- Bibliothèques de génération PDF : `reportlab`, `fpdf2`, `Pillow`

## Notes de session
<!-- Ajouter ici les notes et décisions prises lors de chaque session de travail -->
- **2026-06-02** : Initialisation du projet. Création du CONTEXT.md, du .gitignore et du générateur de documents synthétiques (`_build/generator`).
