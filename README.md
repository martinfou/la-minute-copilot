# La minute Copilot

Votre session hebdomadaire de 5 minutes pour maîtriser Microsoft Copilot au quotidien.
À l'intention des employés IT et non-IT.

## Structure

```
la-minute-copilot/
├── presentations/          ← JSON (contenu) + .pptx (présentation générée)
├── scripts/
│   └── generate_pptx.py     ← Générateur PowerPoint (lit le JSON, produit le .pptx)
├── schema/
│   └── la-minute-copilot.schema.json  ← Schéma JSON (partageable avec d'autres outils)
├── prompts/                ← Archive des prompts Copilot
├── .venv/                  ← Environnement virtuel Python
├── pyproject.toml          ← Métadonnées et dépendances (moderne, remplace requirements.txt)
├── generate.sh             ← Script de convenience (détecte uv ou pip)
└── README.md
```

**Contenu dissocié du contenant.** Modifiez le JSON pour changer le texte, le parseur s'occupe du reste.

## 📐 Schéma JSON (`schema/la-minute-copilot.schema.json`)

Un schéma JSON Schema (draft 2020-12) documentant la structure des fichiers de présentation.
Validé automatiquement par VS Code, Copilot, et la plupart des éditeurs de code.

### Utilisation

Les fichiers JSON d'épisodes contiennent une référence `$schema` en tête :

```jsonc
{
  "$schema": "https://github.com/martinfou/la-minute-copilot/schema/la-minute-copilot.schema.json",
  "title": "La minute Copilot",
  "subtitle": "Copilot dans Outlook",
  // ...
}
```

### Types de diapositives (`slides[].type`)

Le thème graphique s'inspire de la charte **Desjardins** : vert corporatif et fond vert menthe pour le contenu.

Les cartes utilisent des icônes monochromes **[Lucide](https://lucide.dev)** (glyphes vectoriels plats, cohérents avec une charte corporative). Dans le JSON, renseignez `"icon": "message-square"` (nom kebab-case du catalogue Lucide). Prérequis : `rsvg-convert` (`brew install librsvg` sur macOS).

| Type | Usage | Visuel |
|------|-------|--------|
| `title` | 1ère slide | Panneau vert plein à gauche, titre/sous-titre en blanc, fond menthe à droite |
| `tips` | Contenu principal | Fond vert menthe, titre vert foncé, puces et cartes blanches, pied de page avec logo |
| `bonus` | Astuce supplémentaire | Fond vert menthe, cartes ou puces |
| `summary` | Dernière slide | Fond vert Desjardins, cartes récap blanches, encadré bonus blanc à accent vert |

### Propriétés des cartes (`slides[].cards[]`)

| Champ | Requis | Description |
|-------|--------|-------------|
| `title` | ✅ | Titre en gras avec couleur d'accent |
| `icon` | ❌ | Nom d'icône [Lucide](https://lucide.dev/icons) (kebab-case, ex. `message-square`) |
| `color` | ❌ | `green` / `amber` / `blue` / `red` (défaut: bleu) |
| `lines` | ⚠️ | Lignes de texte (ou `desc` pour summary) |
| `desc` | ⚠️ | Texte court pour les cartes de résumé |

### Validation avec d'autres outils

Le schéma est auto-suffisant pour être utilisé par :

- **VS Code** — IntelliSense automatique sur les fichiers `.json`
- **GitHub Copilot** — Meilleure compréhension du contexte du fichier
- **GitHub Actions** — Validation automatique des PRs avec `ajv` ou `check-jsonschema`
- **Python** — Validation avec `jsonschema` library
- **Node.js** — Validation avec `ajv`

**Exemple de workflow GitHub Actions :**

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

## Épisodes

| # | Sujet | JSON | PPTX |
|---|-------|------|------|
| 1 | Outlook — 5 astuces + sauvegarder ses prompts | `outlook.json` | `La_Minute_Copilot_Outlook.pptx` |
| 2 | Personas — L'importance des personas dans les prompts | `personas.json` | `La_Minute_Copilot_Personas.pptx` |
| 3 | Modèles — Les modèles de langage expliqués | `modeles.json` | `La_Minute_Copilot_Modeles.pptx` |
| 4 | SharePoint & OneDrive — Copilot et vos fichiers | `sharepoint-onedrive.json` | `La_Minute_Copilot_SharePoint.pptx` |
| 5 | Prompts avancés — CoT, ToT, Red/Blue Team | `prompts-avances.json` | `La_Minute_Copilot_PromptsAvances.pptx` |
| 6 | Architecture — Le voyage du prompt en entreprise | `architecture-prompt.json` | `La_Minute_Copilot_Architecture.pptx` |

## Générer une présentation

### Avec uv (recommandé — plus rapide, Rust)
```bash
# Installation unique
uv venv --python 3.11
uv sync

# Générer
./generate.sh presentations/outlook.json
```

### Avec pip
```bash
# Installation unique
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Générer
./generate.sh presentations/outlook.json
```

### Avec le script automatique (détecte uv → pip)
```bash
./generate.sh presentations/outlook.json
./generate.sh presentations/outlook.json -o mon_fichier.pptx
```

### Créer un nouvel épisode
1. Copier `presentations/outlook.json` en `presentations/sujet.json`
2. Éditer le JSON (titres, cartes, contenu)
3. `./generate.sh presentations/sujet.json`
4. Présenter!
