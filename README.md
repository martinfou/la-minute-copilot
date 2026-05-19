# La minute Copilot

Votre session hebdomadaire de 5 minutes pour maîtriser Microsoft Copilot au quotidien.
À l'intention des employés TI et non-TI.

**Contenu dissocié du contenant.** Modifiez le JSON pour changer le texte ; le générateur produit le PowerPoint.

Ce dépôt inclut la **[méthode BMAD](https://github.com/bmad-code-org/BMAD-METHOD)** (Build More Architect Dreams) pour guider le développement assisté par IA dans Cursor : workflows, agents spécialisés et compétences (`bmad-help`, PRD, architecture, stories, etc.).

## Structure

```
la-minute-copilot/
├── presentations/              ← JSON (source de vérité) + .pptx générés
├── scripts/
│   ├── generate_pptx.py        ← Générateur PowerPoint (JSON → .pptx)
│   └── lucide_icons.py         ← Téléchargement et rasterisation des icônes Lucide
├── schema/
│   └── la-minute-copilot.schema.json
├── prompts/                    ← Archive des prompts Copilot
├── _bmad/                      ← BMAD : config, agents, workflows (v6.7.1)
├── _bmad-output/               ← Artefacts BMAD (PRD, planning, stories…) — gitignored
├── .agents/skills/             ← Compétences Cursor générées par BMAD (44 skills)
├── assets/icons/cache/         ← Cache PNG des icônes (généré, ignoré par git)
├── pyproject.toml
├── generate.sh                 ← Détecte uv ou pip, lance le générateur
└── README.md
```

## Prérequis

| Outil | Rôle |
|-------|------|
| **Python 3.11+** | Exécuter le générateur |
| **python-pptx** | Création des fichiers `.pptx` (installé via `uv sync` ou `pip install -e .`) |
| **rsvg-convert** | Rasteriser les icônes SVG Lucide en PNG (`brew install librsvg` sur macOS) |
| **Node.js 20+** | Installer ou mettre à jour BMAD (`npx bmad-method`) |
| **Python 3.10+** et **uv** | Recommandés par BMAD pour certains workflows |

Sans `rsvg-convert`, les présentations se génèrent quand même, mais **sans icônes** sur les cartes.

## BMAD Method (Cursor)

Installation déjà effectuée dans ce projet :

- **Module** : `bmm` (BMad Method) + `core`
- **IDE** : Cursor → compétences dans `.agents/skills/`
- **Langue** : français (`communication_language`, `document_output_language`)
- **Connaissance projet** : racine du dépôt (`project_knowledge = .`)

### Démarrer dans Cursor

1. Ouvrir ce dossier dans Cursor.
2. Dans le chat, invoquer la compétence **`bmad-help`** (ex. « Que dois-je faire ensuite? »).
3. Les artefacts produits (PRD, architecture, stories…) vont dans `_bmad-output/`.

### Réinstaller ou mettre à jour BMAD

```bash
npx bmad-method install --yes \
  --directory "$(pwd)" \
  --modules bmm \
  --tools cursor \
  --set core.communication_language=French \
  --set core.document_output_language=French
```

Documentation : [docs.bmad-method.org](https://docs.bmad-method.org) · Dépôt : [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)

> Utiliser `--directory "$(pwd)"` (et `CI=true` si besoin) pour éviter le mode interactif bloqué sur le choix du dossier.

## Thème graphique (Desjardins)

Le rendu s'inspire de la charte Desjardins : vert corporatif, fond menthe pour le contenu, typographie sobre (pas d'émojis dans les diapositives).

| Élément | Couleur / style |
|---------|-----------------|
| Vert corporatif | `#00874E` — titres, accents, slide de synthèse |
| Fond menthe | `#E6F0EA` — slides de contenu |
| Cartes | Fond blanc, bordure grise, titre en couleur d'accent |
| Pied de page | Trait vert + « La minute Copilot » + numéro de page |
| Encadré bonus (synthèse) | Blanc, liseré vert à gauche, texte vert foncé |

Les icônes des cartes proviennent de **[Lucide](https://lucide.dev/icons)** (glyphes vectoriels monochromes, teintés selon la couleur d'accent de la carte).

## Schéma JSON

Fichier : `schema/la-minute-copilot.schema.json` (JSON Schema draft 2020-12).
Validé automatiquement par VS Code, GitHub Copilot et des outils comme `check-jsonschema`.

Référence en tête de chaque épisode :

```jsonc
{
  "$schema": "https://github.com/martinfou/la-minute-copilot/schema/la-minute-copilot.schema.json",
  "title": "La minute Copilot",
  "subtitle": "Copilot dans Outlook",
  "author": "Martin Fournier",
  "date": "2026-05-17",
  "slides": [ /* ... */ ]
}
```

### Types de diapositives (`slides[].type`)

| Type | Usage | Visuel |
|------|-------|--------|
| `title` | 1ère slide | Panneau vert à gauche (titre, sous-titre, auteur, date), fond menthe à droite |
| `tips` | Contenu principal | Fond menthe, titre vert foncé, puces, cartes blanches, pied de page |
| `bonus` | Astuce supplémentaire | Fond menthe, cartes ou puces |
| `summary` | Dernière slide | Fond vert, cartes récap blanches, encadré bonus blanc |

### Propriétés des cartes (`slides[].cards[]`)

| Champ | Requis | Description |
|-------|--------|-------------|
| `title` | ✅ | Titre en gras (couleur d'accent) |
| `icon` | ❌ | Nom Lucide en kebab-case (`message-square`, `users`, `inbox`…) |
| `color` | ❌ | `green` / `amber` / `blue` / `red` — `blue` est remappé vers le vert Desjardins |
| `lines` | ⚠️ | Lignes de texte (slides `tips` / `bonus`) |
| `desc` | ⚠️ | Texte court (slide `summary`) |

Chaque slide peut aussi inclure `speaker_notes`, `bullets`, `subtitle`, `footer` et `bonus` selon le type.

## Épisodes

| # | Sujet | JSON | PPTX | Slides |
|---|-------|------|------|--------|
| 1 | Outlook — 5 astuces + sauvegarder ses prompts | `outlook.json` | `La_Minute_Copilot_Outlook.pptx` | 8 |
| 2 | Personas — L'importance des personas dans les prompts | `personas.json` | `La_Minute_Copilot_Personas.pptx` | 6 |
| 3 | Modèles — Les modèles Copilot Web | `modeles.json` | `La_Minute_Copilot_Modeles.pptx` | 6 |
| 4 | SharePoint et OneDrive — Copilot et vos fichiers | `sharepoint-onedrive.json` | `La_Minute_Copilot_SharePoint.pptx` | 6 |
| 5 | Prompts avancés — CoT, ToT, Red/Blue Team | `prompts-avances.json` | `La_Minute_Copilot_PromptsAvances.pptx` | 6 |
| 6 | Architecture — Le voyage du prompt en entreprise | `architecture-prompt.json` | `La_Minute_Copilot_Architecture.pptx` | 6 |

Les fichiers `.pptx` sont générés localement (ignorés par git sauf si versionnés explicitement). Le **JSON est la source de vérité**.

### Épisode Outlook (aperçu)

| Astuce | Sujet |
|--------|--------|
| 1 | Résumer un fil de discussion |
| 2 | Rédiger une réponse en 2 clics |
| 3 | Prioriser sa boîte de réception |
| 4 | Statut d'un projet (actions à prendre, éléments en attente) |
| 5 | Planifier sa journée et sa semaine (fin de journée, lundi, vendredi) |
| Bonus | Sauvegarder ses prompts (QuickPart, OneNote, Copilot Lab) |

Contenu entièrement en **français** (y compris les exemples de prompts).

## Générer une présentation

### Installation (une fois)

**Avec uv (recommandé)**

```bash
uv venv --python 3.11
uv sync
brew install librsvg   # macOS — icônes Lucide
```

**Avec pip**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
brew install librsvg
```

### Un épisode

```bash
./generate.sh presentations/outlook.json
./generate.sh presentations/outlook.json -o presentations/La_Minute_Copilot_Outlook.pptx
```

Le script `generate.sh` active le venv (`uv` ou `pip`) puis appelle `scripts/generate_pptx.py`.

### Tous les épisodes

```bash
for j in outlook personas modeles sharepoint-onedrive prompts-avances architecture-prompt; do
  case $j in
    outlook) o=La_Minute_Copilot_Outlook ;;
    personas) o=La_Minute_Copilot_Personas ;;
    modeles) o=La_Minute_Copilot_Modeles ;;
    sharepoint-onedrive) o=La_Minute_Copilot_SharePoint ;;
    prompts-avances) o=La_Minute_Copilot_PromptsAvances ;;
    architecture-prompt) o=La_Minute_Copilot_Architecture ;;
  esac
  ./generate.sh "presentations/${j}.json" -o "presentations/${o}.pptx"
done
```

### Créer un nouvel épisode

1. Copier `presentations/outlook.json` → `presentations/mon-sujet.json`
2. Éditer le JSON (titres, cartes, `icon` Lucide, notes du présentateur)
3. `./generate.sh presentations/mon-sujet.json`
4. Présenter

Vérifier les noms d'icônes sur [lucide.dev/icons](https://lucide.dev/icons) — le CDN utilisé est `lucide-static@0.469.0`.

## Validation JSON (CI)

```yaml
name: Validate JSON
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install check-jsonschema
      - run: check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/*.json
```
