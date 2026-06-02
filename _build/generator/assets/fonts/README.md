# Ressources — Polices manuscrites

Placer ici les fichiers `.ttf` des polices manuscrites.

## Polices reconnues automatiquement
Le générateur cherche ces fichiers dans cet ordre :

| Fichier | Police |
|---|---|
| `DancingScript-Regular.ttf` | Dancing Script (Google Fonts) |
| `Caveat-Regular.ttf` | Caveat (Google Fonts) |
| `PatrickHand-Regular.ttf` | Patrick Hand (Google Fonts) |

Si aucune police n'est trouvée, le générateur replie sur **Helvetica-Oblique** (intégrée à ReportLab).

## Téléchargement rapide (exemple avec curl)
```bash
# Depuis Google Fonts (URLs directes des releases GitHub)
curl -L "https://github.com/google/fonts/raw/main/ofl/caveat/Caveat-Regular.ttf" \
     -o Caveat-Regular.ttf
```
