# 🎤 La minute Copilot

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
├── .venv/                  ← Dépendances Python
├── requirements.txt
├── generate.sh             ← Script de convenience
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

| Type | Usage | Visuel |
|------|-------|--------|
| `title` | 1ère slide | Fond bleu, titre + sous-titre + footer centrés |
| `tips` | Contenu principal | Fond blanc, puces + cartes côte à côte |
| `bonus` | Astuce supplémentaire | Fond gris clair, cartes ou puces |
| `summary` | Dernière slide | Fond bleu, cartes récap + bannière jaune bonus |

### Propriétés des cartes (`slides[].cards[]`)

| Champ | Requis | Description |
|-------|--------|-------------|
| `icon` | ✅ | Émoji identifiant la carte |
| `title` | ✅ | Titre en gras avec couleur d'accent |
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
      - run: check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/ep*.json
```

## Épisodes

| # | Sujet | JSON | PPTX |
|---|-------|------|------|
| 1 | Outlook — 3 astuces + sauvegarder ses prompts | `ep01-outlook.json` | `La_Minute_Copilot_Outlook.pptx` |
| 2 | Personas — L'importance des personas dans les prompts | `ep02-personas.json` | `La_Minute_Copilot_Personas.pptx` |
| 3 | Modèles — Les modèles de langage expliqués | `ep03-modeles.json` | `La_Minute_Copilot_Modeles.pptx` |
| 4 | SharePoint & OneDrive — Copilot et vos fichiers | `ep04-sharepoint-onedrive.json` | `La_Minute_Copilot_SharePoint.pptx` |
| 5 | Prompts avancés — CoT, ToT, Red/Blue Team | `ep05-prompts-avances.json` | `La_Minute_Copilot_PromptsAvances.pptx` |
| 6 | Architecture — Le voyage du prompt en entreprise | `ep06-architecture-prompt.json` | `La_Minute_Copilot_Architecture.pptx` |

## Générer une présentation

### Première fois
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ensuite
```bash
# Générer la dernière présentation
./generate.sh presentations/ep01-outlook.json

# Ou vers un fichier spécifique
./generate.sh presentations/ep01-outlook.json -o mon_fichier.pptx
```

### Créer un nouvel épisode
1. Copier `presentations/ep01-outlook.json` en `presentations/ep02-sujet.json`
2. Éditer le JSON (titres, cartes, contenu)
3. `./generate.sh presentations/ep02-sujet.json`
4. Présenter!
