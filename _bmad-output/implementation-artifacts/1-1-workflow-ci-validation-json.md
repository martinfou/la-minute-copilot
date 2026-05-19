# Story 1.1: Workflow CI validation JSON

Status: ready-for-dev

<!-- Validation optionnelle : bmad-create-story:validate avant dev-story -->

## Story

As a **développeur / animateur**,
I want **une validation automatique des JSON d’épisodes à chaque pull request**,
so that **aucun épisode invalide n’atteigne la branche principale**.

## Acceptance Criteria

1. **Given** le dépôt `la-minute-copilot` sur GitHub  
   **When** une pull request modifie des fichiers sous `presentations/*.json`  
   **Then** un workflow GitHub Actions valide tous les JSON contre le schéma.

2. **Given** le workflow CI  
   **When** il s’exécute  
   **Then** il utilise `check-jsonschema --schemafile schema/la-minute-copilot.schema.json` sur **chaque** fichier `presentations/*.json` (6 fichiers actuels).

3. **Given** un JSON qui ne respecte pas le schéma  
   **When** la CI s’exécute  
   **Then** le job **échoue** (exit code non nul) et la PR ne peut pas merger sans correction.

4. **Given** le README  
   **When** un contributeur lit la section « Validation JSON (CI) »  
   **Then** le workflow documenté correspond au fichier réel (nom, déclencheur, commande).

5. **Given** les six JSON existants  
   **When** la CI tourne sur la branche actuelle **sans modification invalide**  
   **Then** le job **passe** (baseline verte).

## Tasks / Subtasks

- [ ] Créer `.github/workflows/validate-json.yml` (AC: 1, 2, 3)
  - [ ] Déclencheur : `pull_request` (branches `main` / `master` selon le dépôt — vérifier branche par défaut)
  - [ ] Optionnel : `push` sur `main` pour validation continue
  - [ ] `actions/checkout@v4`
  - [ ] Python 3.11+ (`actions/setup-python@v5` avec `python-version: '3.11'`)
  - [ ] `pip install check-jsonschema` (pin version raisonnable ex. `check-jsonschema>=0.28` si souhaité)
  - [ ] Commande : `check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/*.json`
  - [ ] Ne pas valider les `.pptx` — uniquement JSON
- [ ] Vérifier localement avant PR (AC: 5)
  - [ ] `pip install check-jsonschema` (ou `uv pip install check-jsonschema`)
  - [ ] Exécuter la même commande que la CI — doit sortir 0
- [ ] Aligner README si le workflow diffère du snippet existant (AC: 4)
  - [ ] Mettre à jour section « Validation JSON (CI) » si chemins, version Python ou déclencheurs changent
  - [ ] Ne pas dupliquer toute la doc dans OPENCLAW.md (Story 1.2) — une ligne « voir README » suffit pour l’instant
- [ ] Test de régression manuelle (AC: 3)
  - [ ] Introduire temporairement une clé invalide dans un JSON de test / branche locale → CI doit échouer
  - [ ] Revenir au JSON valide

## Dev Notes

### Contexte produit

- **FR-6** : structure JSON standardisée — la CI enforce le schéma avant merge.
- **NFR-1** : reproductibilité — empêche les régressions de format dans `presentations/`.
- Gap architecture : pas de `.github/workflows/` aujourd’hui — cette story le comble.

### Fichiers à créer / modifier

| Fichier | Action |
|---------|--------|
| `.github/workflows/validate-json.yml` | **CREATE** |
| `README.md` | **UPDATE** section Validation JSON (si nécessaire) |

**Ne pas modifier** : `scripts/generate_pptx.py`, `schema/` (sauf bug schéma découvert — hors scope), fichiers JSON épisodes (sauf test local).

### Schéma et épisodes existants

- Schéma : `schema/la-minute-copilot.schema.json` (JSON Schema draft 2020-12)
- JSON à valider (6) :
  - `presentations/outlook.json`
  - `presentations/personas.json`
  - `presentations/modeles.json`
  - `presentations/sharepoint-onedrive.json`
  - `presentations/prompts-avances.json`
  - `presentations/architecture-prompt.json`

### Workflow YAML recommandé (base)

```yaml
name: Validate JSON

on:
  pull_request:
    paths:
      - 'presentations/**.json'
      - 'schema/**'
  push:
    branches: [main]
    paths:
      - 'presentations/**.json'
      - 'schema/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install check-jsonschema
        run: pip install 'check-jsonschema>=0.28'
      - name: Validate presentation JSON files
        run: check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/*.json
```

**Notes d’implémentation :**

- Si `paths` sur `pull_request` est utilisé, une PR qui ne touche que Python ne déclenchera pas la CI JSON — acceptable ; alternative : toujours lancer sur toute PR (plus lent mais plus sûr).
- Sur macOS local, la glob `presentations/*.json` est développée par le shell — en CI Ubuntu bash, idem.
- Pas besoin d’installer `python-pptx` ni `rsvg` pour cette story.

### Architecture compliance

- [Source: `_bmad-output/planning-artifacts/architecture.md`] Décision #4 — validation CI `check-jsonschema`
- [Source: `_bmad-output/project-context.md`] JSON = source de vérité ; schéma obligatoire
- [Source: `README.md` lignes 209-221] Snippet CI existant — **aligner le fichier réel sur ce contrat**

### Testing requirements

- Pas de tests pytest requis pour v1.
- **Preuve de done** : workflow vert sur PR ; test négatif documenté dans Completion Notes (JSON invalide → rouge).

### Previous story intelligence

_Première story du sprint — aucune story précédente._

### Project structure notes

- `_bmad-output/` est gitignored — ne pas y mettre le workflow.
- `implementation-artifacts/` contient les stories, pas le code produit.

### References

- [Source: `_bmad-output/planning-artifacts/epics.md` — Story 1.1]
- [Source: `_bmad-output/planning-artifacts/prds/prd-la-minute-copilot-2026-05-18/prd.md` — FR-6]
- [Source: `_bmad-output/planning-artifacts/architecture.md` — Gap CI, Epic 1]
- [Source: `README.md` — Validation JSON (CI)]

## Dev Agent Record

### Agent Model Used

_(à remplir par l’agent dev)_

### Debug Log References

### Completion Notes List

### File List
