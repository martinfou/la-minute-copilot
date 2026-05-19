# Addendum — La minute Copilot PRD

_Détails techniques et opérationnels qui nourrissent architecture / epics mais ne appartiennent pas au corps du PRD._

## Chaîne de production OpenClaw

| Élément | Détail |
|---------|--------|
| **Runtime** | Machine locale (chez l’animateur) |
| **Interface** | Telegram |
| **Accès dépôt** | OpenClaw a accès au projet `la-minute-copilot` |
| **Entrée animateur** | Sujet (topic) + quelques cas d’usage jugés originaux |
| **Sortie** | Fichier JSON conforme au schéma `schema/la-minute-copilot.schema.json` |
| **Rendu** | `scripts/generate_pptx.py` (ou `./generate.sh`) → `.pptx` thème Desjardins |
| **Documentation agent** | `OPENCLAW.md` à la racine du dépôt (navigation, éditorial, checklist) |

**Non couvert par OpenClaw dans ce flux :** choix d’autres LLM que l’écosystème Copilot ; validation institutionnelle du contenu (reste humain — animateur).

## Piste optionnelle « rencontre dev »

GitHub Copilot pourrait faire l’objet d’épisodes ou d’une **rencontre dédiée développeurs**, distincte du format M365 hebdomadaire grand public TI. À trancher dans le PRD (FR ou hors scope v1).
