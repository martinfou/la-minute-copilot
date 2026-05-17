# 🎤 La minute Copilot

Votre session hebdomadaire de 5 minutes pour maîtriser Microsoft Copilot au quotidien.
À l'intention des employés IT et non-IT.

## Structure

```
la-minute-copilot/
├── presentations/      ← JSON (contenu) + .pptx (présentation générée)
├── scripts/
│   └── parse.py        ← Générateur PowerPoint (lit le JSON, produit le .pptx)
├── prompts/            ← Archive des prompts Copilot
├── .venv/              ← Dépendances Python
├── requirements.txt
├── generate.sh         ← Script de convenience
└── README.md
```

**Contenu dissocié du contenant.** Modifiez le JSON pour changer le texte, le parseur s'occupe du reste.

## Épisodes

| # | Sujet | JSON | PPTX |
|---|-------|------|------|
| 1 | Outlook — 3 astuces + sauvegarder ses prompts | `ep01-outlook.json` | `La_Minute_Copilot_Outlook.pptx` |

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
