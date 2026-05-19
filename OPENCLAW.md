# Instructions OpenClaw — La minute Copilot

**Lis ce fichier en premier** quand tu travailles dans ce dépôt. Il décrit le **but du projet**, comment le naviguer et comment **produire un épisode** (fichier JSON).

Compléments utiles :
- `README.md` — vue d’ensemble humaine, thème visuel, commandes
- `schema/la-minute-copilot.schema.json` — contrat JSON (référence obligatoire)
- `_bmad-output/project-context.md` — règles techniques pour le code et la génération PPTX
- `_bmad-output/planning-artifacts/prds/prd-la-minute-copilot-2026-05-18/prd.md` — vision produit, personas, exigences éditoriales
- `_bmad-output/planning-artifacts/architecture.md` — décisions techniques et limites du dépôt

---

## 1. But de La minute Copilot

**La minute Copilot** est une **série de présentations PowerPoint hebdomadaires** (~5 minutes) pour le **département informatique** d’une institution financière québécoise (~100 personnes : gestion, Scrum Masters, QA, analystes, PO proxy, adjoints admin, développeurs, etc.).

**Problème adressé :** Copilot (M365) a été déployé **sans formation** ; les niveaux de compétence sont très inégaux. Beaucoup traitent Copilot comme **Google** ; d’autres craignent que l’IA **vole leur emploi** ; les devs utilisent surtout **GitHub Copilot** et ignorent le reste de l’offre Microsoft.

**Promesse de chaque épisode :** des **trucs et astuces concrets** pour être plus performant avec **Copilot** (écosystème M365 : Outlook, Teams, Word, Copilot Web, SharePoint/OneDrive, etc.) — **pas** d’autres LLM (ChatGPT, Claude, etc.).

**Objectif sur ~6 mois :** ~25 épisodes ; l’audience devient plus à l’aise et plus efficace avec Copilot (mesuré par des sondages avant/après, gérés par l’animateur).

**Chaîne de production :**

```
Martin (sujet + use cases)  →  OpenClaw (JSON)  →  generate_pptx.py  →  .pptx
         Telegram                    ce dépôt              ./generate.sh
```

Tu es responsable du **JSON** dans `presentations/`. Martin valide, lance la génération et présente en séance.

---

## 2. Carte du dépôt

| Chemin | Rôle pour toi |
|--------|----------------|
| `presentations/*.json` | **Source de vérité** du contenu — c’est ici que tu écris ou modifies un épisode |
| `presentations/*.pptx` | Fichiers **générés** — ne pas éditer à la main |
| `schema/la-minute-copilot.schema.json` | Schéma à respecter (types de slides, cartes, champs) |
| `scripts/generate_pptx.py` | Moteur de rendu (thème Desjardins) — lire si tu dois comprendre les types de slides |
| `scripts/lucide_icons.py` | Icônes Lucide → PNG (noms en kebab-case) |
| `generate.sh` | Commande que Martin utilise pour produire le PPTX |
| `OPENCLAW.md` | Ce guide |
| `_bmad/`, `.agents/` | Workflows BMAD / Cursor — **hors scope** création d’épisodes |
| `_bmad-output/` | PRD, project-context — contexte produit, pas le JSON des slides |
| `prompts/` | Archive de prompts — inspiration seulement |

**Épisodes existants (modèles à imiter) :**

| Fichier JSON | Sujet |
|--------------|--------|
| `outlook.json` | Copilot dans Outlook |
| `personas.json` | Personas dans les prompts |
| `modeles.json` | Modèles Copilot Web (Auto, rapide, Think Deeper) |
| `sharepoint-onedrive.json` | SharePoint / OneDrive |
| `prompts-avances.json` | Prompts avancés |
| `architecture-prompt.json` | Cycle de vie d’un prompt en entreprise |

---

## 3. Ta mission (OpenClaw)

Quand Martin t’envoie un **topic** et quelques **cas d’usage originaux** (Telegram) :

1. **Clarifier** si besoin (outil M365 visé, persona visé : débutant / anxieux / dev).
2. **Choisir un fichier** : `presentations/<sujet-kebab>.json` (nouveau ou mise à jour).
3. **Rédiger le JSON complet** conforme au schéma (voir §4).
4. **Valider** mentalement : français, pas de données sensibles, 5 min de présentation, astuce actionnable.
5. **Signaler à Martin** le chemin du fichier et la commande :  
   `./generate.sh presentations/<fichier>.json`

Tu **ne génères pas** le PPTX toi-même sauf si ton environnement peut exécuter `./generate.sh` ; le JSON est ta livraison principale.

---

## 4. Contrat JSON (résumé)

En tête de fichier, inclure si possible :

```json
{
  "$schema": "https://github.com/martinfou/la-minute-copilot/schema/la-minute-copilot.schema.json",
  "title": "La minute Copilot",
  "subtitle": "Sujet de l'épisode",
  "author": "Martin Fournier",
  "date": "YYYY-MM-DD",
  "slides": [ ... ]
}
```

### Types de slides (`slides[].type`)

| Type | Usage |
|------|--------|
| `title` | **1ère slide** — couverture (requiert `subtitle`, souvent `footer`) |
| `tips` | Contenu principal — astuces, puces, cartes |
| `bonus` | Astuce supplémentaire |
| `summary` | **Dernière slide** — récap (`cards` avec `desc`, souvent `bonus` + `footer`) |

Ordre typique : `title` → plusieurs `tips` / `bonus` → `summary`.

### Cartes (`cards[]`)

- `title` (requis), `lines` **ou** `desc` (summary)
- `icon` : nom [Lucide](https://lucide.dev/icons) en **kebab-case** (`message-square`, `sparkles`, `zap`)
- `color` : `green` | `amber` | `blue` | `red` (`blue` est affiché en vert Desjardins)

### Notes présentateur (`speaker_notes`)

- Style **oral**, direct, comme Martin à l’animateur : « Accueil : … », « Démo : … »
- Doit tenir ~**5 minutes** au total pour l’épisode

### Règles éditoriales

- **Français** (Québec), ton professionnel, institution financière.
- **Une ou deux astuces** vraiment testables dans la semaine.
- Pour l’audience **anxieuse** : Copilot = **assistant**, pas remplacement du métier.
- Pour les **débutants** : éviter le jargon ; montrer où cliquer.
- Pour les **devs** : pousser vers **M365 / Copilot Web**, pas seulement GitHub Copilot.
- **Exemples de prompts** génériques — jamais de vrais clients, courriels réels ou données confidentielles.
- Les émojis peuvent apparaître dans le JSON source ; le générateur les **retire des slides** (charte sobre).

---

## 5. Format du brief Martin (entrée)

Attendu typiquement :

- **Topic** : ex. « Copilot dans Teams », « Sécurité des prompts »
- **2–4 use cases originaux** : situations concrètes du TI
- Optionnel : persona cible (débutant / peur emploi / dev), ordre dans la saison

Si le brief est vague, propose **un titre d’épisode** et **3 astuces** avant d’écrire tout le JSON.

---

## 6. Checklist avant de rendre la main

- [ ] JSON valide selon `schema/la-minute-copilot.schema.json`
- [ ] Premier slide `type: "title"` avec `subtitle`
- [ ] Dernier slide `type: "summary"` avec `cards` + `desc`
- [ ] Chaque slide de contenu a `speaker_notes`
- [ ] Icônes Lucide existent (vérifier sur lucide.dev)
- [ ] Durée présentable en ~5 min
- [ ] Sujet 100 % **Copilot / M365** (pas autre LLM)
- [ ] Fichier enregistré sous `presentations/<nom>.json`

Validation locale (si `check-jsonschema` installé) :

```bash
check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/ton-episode.json
```

---

## 7. Après ta livraison

Martin exécute :

```bash
./generate.sh presentations/ton-episode.json
# ou avec nom PPTX explicite :
./generate.sh presentations/ton-episode.json -o presentations/La_Minute_Copilot_MonSujet.pptx
```

Le PPTX apparaît avec le thème **Desjardins** (vert `#00874E`, fond menthe, cartes blanches).

**Icônes :** nécessitent `rsvg-convert` sur la machine de génération (`brew install librsvg`). Sans ça, le PPTX se génère sans icônes.

---

## 8. Ce qu’il ne faut pas faire

- Modifier les `.pptx` comme source de vérité
- Inventer des champs hors schéma ou des `type` de slide non supportés
- Promouvoir ChatGPT, Claude ou autre hors Copilot
- Mettre des données réelles d’employés ou de clients dans les exemples
- Produire un « cours » de 30 slides — rester **court et actionnable**
- Ignorer les épisodes existants : **copier la structure** de `outlook.json` ou `modeles.json` avant d’inventer un nouveau format

---

## 9. File de sujets (saison)

Sujets déjà couverts ou planifiés dans le dépôt :

1. Cycle de vie d’un prompt en entreprise  
2. Modèles Copilot Web  
3. Outlook  
4. Personas  
5. Prompts avancés  
6. SharePoint / OneDrive  

~19 autres sujets possibles (Teams, Word, Excel, Quick Parts, etc.) — en discuter avec Martin pour éviter les doublons.

---

## 10. Questions

En cas de doute sur le **produit** (personas, ton, périmètre) : lire le PRD dans `_bmad-output/planning-artifacts/prds/prd-la-minute-copilot-2026-05-18/prd.md`.

En cas de doute sur le **format technique** : `schema/la-minute-copilot.schema.json` et `_bmad-output/project-context.md`.

Demander à Martin sur Telegram pour validation éditoriale ou sujet de la semaine.
