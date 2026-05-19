---
project_name: 'la-minute-copilot'
user_name: 'Martinfou'
date: '2026-05-18'
sections_completed:
  - technology_stack
  - language_rules
  - framework_rules
  - testing_rules
  - quality_rules
  - workflow_rules
  - anti_patterns
status: 'complete'
rule_count: 42
optimized_for_llm: true
---

# Project Context for AI Agents

_Règles et motifs critiques pour implémenter du code dans ce dépôt. Priorité aux détails non évidents — le README couvre le reste._

---

## Technology Stack & Versions

| Composant | Version / contrainte |
|-----------|----------------------|
| Python | ≥ 3.11 (`pyproject.toml`, venv 3.11 via `generate.sh`) |
| python-pptx | ≥ 1.0 |
| Lucide (CDN) | `lucide-static@0.469.0` — constante `LUCIDE_VERSION` dans `scripts/lucide_icons.py` |
| rsvg-convert | librsvg (requis pour icônes ; optionnel pour PPTX sans icônes) |
| JSON Schema | draft 2020-12 — `schema/la-minute-copilot.schema.json` |
| Slide format | 13.33" × 7.5" (16:9) |
| BMAD | 6.7.1 — artefacts planification dans `_bmad-output/` (versionné Git) |

**Pas dans ce dépôt :** Node/React (sauf `npx bmad-method`), base de données, API serveur.

---

## Critical Implementation Rules

### Language-Specific Rules (Python)

- **Style existant :** fonctions module-level (`add_*`, `render_*`), pas de classes ; imports groupés en tête dans `generate_pptx.py`, `from __future__ import annotations` dans `lucide_icons.py`.
- **Chemins :** `Path(__file__).resolve().parent` pour ancres locales ; `sys.path.insert(0, …)` uniquement pour importer `lucide_icons` depuis `scripts/`.
- **Encodage :** toujours `encoding='utf-8'` pour lire/écrire JSON.
- **Texte affiché :** passer par `clean_text()` avant insertion dans PPTX (retire émojis et normalise espaces).
- **Couleurs pptx :** utiliser les constantes `RGBColor` du haut de `generate_pptx.py` — ne pas inventer de hex hors palette sans mise à jour coordonnée du thème.
- **Erreurs icônes :** `add_lucide_icon` échoue silencieusement après un seul avertissement stderr ; ne pas faire échouer la génération entière.

### Framework-Specific Rules (python-pptx + JSON)

**Source de vérité = JSON, jamais le PPTX**
- Modifier `presentations/*.json`, regénérer avec `./generate.sh` ou `python3 scripts/generate_pptx.py`.
- Ne pas éditer manuellement les `.pptx` versionnés sauf urgence ; les changements seront écrasés.

**Contrat JSON**
- Référence `$schema` en tête de chaque épisode (voir README).
- Types de slide : `title` | `tips` | `bonus` | `summary` — enregistrés dans `RENDERERS` ; type inconnu = slide **ignorée** (pas d'exception).
- `title` : requiert `subtitle` (schéma + rendu panneau gauche).
- `summary` : requiert `cards` avec `desc` (pas `lines`).
- `tips` / `bonus` : cartes utilisent `lines` ; max 4 cartes par slide (schéma).
- `speaker_notes` : style oral direct en français (« Accueil: … », « Démo: … »).

**Cartes**
- `icon` : kebab-case Lucide (`message-square`), validé par regex `[a-z0-9-]+`.
- `color` : `green` | `amber` | `blue` | `red` — **`blue` est remappé vers vert Desjardins** dans `PALETTE` (rétrocompat).
- Chaînes vides dans `lines` = espacement vertical intentionnel.

**Thème Desjardins (ne pas dévier)**
- Vert `#00874E`, fond menthe `#E6F0EA`, vert foncé titres `#006B3F`.
- Police `Calibri` ; **pas d'émojis** sur les diapositives (même si présents dans JSON source).
- Pied de page contenu : trait + « La minute Copilot » + numéro ; slide `summary` = fond vert plein, cartes blanches.

**Nouveau type de slide**
1. Ajouter au schéma (`enum` + `enumDescriptions` + règles `allOf` si champs requis).
2. Implémenter `render_<type>(slide, sd, idx)` dans `generate_pptx.py`.
3. Enregistrer dans `RENDERERS`.
4. Mettre à jour README (table types) si comportement public.

**Nouvelle icône / version Lucide**
- Vérifier existence sur https://lucide.dev/icons
- Mettre à jour `LUCIDE_VERSION` et `LUCIDE_CDN` dans `lucide_icons.py` si bump.
- Cache : `assets/icons/cache/` (gitignored) — pas besoin de committer les PNG.

### Testing Rules

- **Pas de suite de tests projet** à ce jour — ne pas ajouter de framework de test lourd sans demande explicite.
- **Validation manuelle :** `./generate.sh presentations/<épisode>.json` puis ouvrir le PPTX.
- **Validation CI (recommandée) :** `check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/*.json` (voir README).
- Tests BMAD dans `.agents/skills/*/scripts/tests/` — hors périmètre des épisodes Copilot.

### Code Quality & Style Rules

- **Fichiers :** JSON kebab-case (`prompts-avances.json`) ; PPTX sortie `La_Minute_Copilot_<Sujet>.pptx` (PascalCase avec underscores).
- **Contenu :** français québécois/canadien professionnel ; public TI + non-TI, contexte institution financière.
- **Commentaires code :** français pour logique métier/visuelle ; docstrings courtes sur fonctions publiques `lucide_icons`.
- **Portée des changements :** minimal — une épisode = un JSON ; changement générateur = impact sur **tous** les épisodes → regénérer la boucle README.
- **Secrets :** aucune clé API dans le dépôt (génération 100 % locale).

### Development Workflow Rules

- **Environnement :** préférer `uv sync` + `./generate.sh` ; sinon `pip install -e .` dans `.venv`.
- **Commits :** uniquement sur demande utilisateur ; pas de `git config` ; pas de force push.
- **BMAD :** lire ce fichier avant implémentation ; artefacts BMAD dans `_bmad-output/` (versionné Git).
- **Nouvel épisode :** copier `presentations/outlook.json` → éditer → générer → optionnellement ajouter ligne au tableau README « Épisodes ».

### Critical Don't-Miss Rules

| Ne pas faire | Faire à la place |
|--------------|------------------|
| Éditer le `.pptx` pour le texte | Éditer le `.json` + regénérer |
| Ajouter émojis dans le rendu slide | OK dans JSON notes seulement si utile ; `clean_text` les retire à l'affichage |
| Nouvelle couleur `color` sans `PALETTE` | Étendre `PALETTE` + schéma `enum` |
| Icône inventée ou snake_case | Nom exact Lucide kebab-case |
| Oublier `rsvg-convert` en doc | Mentionner `brew install librsvg` si icônes requises |
| Slide type sans entrée `RENDERERS` | Ajouter renderer ou retirer du JSON |
| Hardcoder texte d'épisode dans Python | Tout contenu pédagogique reste dans JSON |
| Bump Lucide sans tester un épisode | Générer au moins un JSON avec icônes variées |

**Layout slide 6 :** `prs.slide_layouts[6]` = blank — ne pas changer sans recalibrer toutes les positions `Inches()`.

**Sortie par défaut :** même répertoire que le JSON, basename `.pptx` — utiliser `-o` pour noms `La_Minute_Copilot_*` cohérents avec les épisodes existants.

---

## Usage Guidelines

**Pour les agents IA**

- Lire ce fichier avant toute modification de `scripts/`, `schema/` ou `presentations/`.
- En cas de doute : JSON + schéma > README > ce fichier > improvisation.
- Préférer la règle la plus restrictive (thème Desjardins, pas d'émojis slides, JSON source de vérité).

**Pour les humains**

- Garder ce fichier **court** (< ~150 lignes utiles) ; retirer les règles devenues évidentes.
- Mettre à jour quand : nouveau type de slide, bump Lucide, changement palette, nouveau workflow CI.
- Révision trimestrielle recommandée.

_Dernière mise à jour : 2026-05-18_
