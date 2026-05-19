---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-la-minute-copilot-2026-05-18/prd.md
  - _bmad-output/planning-artifacts/prds/prd-la-minute-copilot-2026-05-18/addendum.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/project-context.md
  - OPENCLAW.md
  - README.md
workflowType: epics-and-stories
project_name: la-minute-copilot
user_name: Martinfou
date: 2026-05-19
status: complete
---

# la-minute-copilot — Epic Breakdown

## Overview

Découpage des exigences du PRD final et de l’architecture en epics et stories implémentables. Le produit couvre la **série hebdomadaire** La minute Copilot, la **chaîne JSON → PPTX** et la **mesure** par sondages (hors repo).

**Pas de document UX** — format slide fixé par le schéma et `generate_pptx.py`.

---

## Requirements Inventory

### Functional Requirements

- **FR-1:** Session de cinq minutes devant l’Audience TI.
- **FR-2:** Au moins une astuce actionnable par épisode.
- **FR-3:** Ton rassurant pour P2 (Copilot = assistant).
- **FR-4:** Ciblage persona P1/P2/P3 documenté par épisode.
- **FR-5:** Alternance sujets accessibles vs technique M365.
- **FR-6:** Structure visuelle standardisée (schéma + thème Desjardins).
- **FR-7:** Contenu en français institutionnel, sans données sensibles.
- **FR-8:** Saison ~25 épisodes sur six mois (≥22 livrés).
- **FR-9:** Périmètre Copilot exclusif (pas d’autres LLM).
- **FR-10:** Sondage de référence avant le premier épisode.
- **FR-11:** Sondage de bilan à six mois (comparable au référence).

### NonFunctional Requirements

- **NFR-1:** Reproductibilité — JSON versionné, PPTX régénérable (`architecture.md`).
- **NFR-2:** Simplicité — CLI locale, pas de serveur ni base de données.
- **NFR-3:** Cohérence visuelle — palette Desjardins centralisée dans `generate_pptx.py`.
- **NFR-4:** Guidage agents — `project-context.md`, `OPENCLAW.md`, schéma JSON.
- **NFR-5:** Sécurité contenu — pas de PII dans les exemples d’épisodes.
- **NFR-6:** Encodage UTF-8 pour tous les JSON.
- **NFR-7:** Icônes Lucide optionnelles via `rsvg-convert` (dégradation gracieuse).
- **NFR-8:** Artefacts BMAD dans `_bmad-output/` (gitignored).

### Additional Requirements

- Brownfield : **pas de nouveau starter** — dépôt actuel = fondation (`architecture.md`).
- Validation JSON recommandée : `check-jsonschema` sur `presentations/*.json` (gap CI).
- OpenClaw : brief Telegram → JSON ; lire `OPENCLAW.md` avant production.
- Un épisode = `presentations/<slug>.json` + génération `./generate.sh`.
- Sondages FR-10/11 : **hors dépôt** (Teams / outil département).
- PPTX : ne pas éditer manuellement ; régénérer depuis JSON.

### UX Design Requirements

_N/A — pas d’application UI. Le « design » est le contrat JSON + moteur PPTX._

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR-1 | Epic 2, 4 | Format 5 min — contenu `speaker_notes` + structure slides |
| FR-2 | Epic 2, 4 | Astuce actionnable dans chaque JSON |
| FR-3 | Epic 2, 4 | Ton P2 dans rédaction épisodes |
| FR-4 | Epic 2, 4, 5 | Personas documentés (file §4.0 / ROADMAP) |
| FR-5 | Epic 2, 5 | Alternance dans planification saison |
| FR-6 | Epic 1, 2, 4 | Schéma + CI + génération PPTX |
| FR-7 | Epic 2, 4 | Revue contenu FR / conformité |
| FR-8 | Epic 2, 4, 5 | Saison et calendrier |
| FR-9 | Epic 2, 4 | Périmètre éditorial Copilot only |
| FR-10 | Epic 3 | Sondage référence |
| FR-11 | Epic 3 | Sondage bilan 6 mois |

---

## Epic List

### Epic 1: Pipeline fiable JSON → PPTX

L’**Animateur** et **OpenClaw** peuvent produire des épisodes **validés** et **régénérés** sans surprise de format.

**FRs couverts :** FR-6 (support outillage)

### Epic 2: Lancer la saison — six épisodes fondation

L’**Audience TI** reçoit les **six premiers sujets** prêts à présenter ; l’**Animateur** tient la cadence initiale avec fichiers du dépôt.

**FRs couverts :** FR-1 à FR-7, FR-8 (partiel), FR-9

### Epic 3: Mesurer la montée en compétence Copilot

L’**Animateur** peut prouver l’évolution de l’audience avec **deux sondages** comparables.

**FRs couverts :** FR-10, FR-11

### Epic 4: Produire les épisodes hebdomadaires suivants

L’**Animateur** peut ajouter des épisodes **7+** via OpenClaw en suivant un processus reproductible.

**FRs couverts :** FR-1 à FR-7, FR-8 (partiel), FR-9

### Epic 5: Compléter la file éditoriale (~19 sujets)

La **saison complète (~25 épisodes)** couvre P1, P2 et P3 avec alternance des niveaux.

**FRs couverts :** FR-4, FR-5, FR-8 (complément)

---

## Epic 1: Pipeline fiable JSON → PPTX

Garantir que tout JSON d’épisode est valide avant génération PPTX et que le dépôt documente le flux.

### Story 1.1: Workflow CI validation JSON

As a **développeur / animateur**,
I want **une validation automatique des JSON d’épisodes à chaque PR**,
So that **aucun épisode invalide n’atteigne la branche principale**.

**Acceptance Criteria:**

**Given** le dépôt `la-minute-copilot` sur GitHub  
**When** une pull request modifie `presentations/*.json`  
**Then** un workflow `.github/workflows/validate-json.yml` exécute `check-jsonschema --schemafile schema/la-minute-copilot.schema.json presentations/*.json`  
**And** la PR échoue si un JSON est invalide  
**And** le README référence ce workflow (section Validation JSON)

**Implements:** FR-6, NFR-1, architecture gap CI

### Story 1.2: Script local de validation (optionnel)

As an **animateur**,
I want **valider un épisode en local avant présentation**,
So that **je détecte les erreurs sans attendre la CI**.

**Acceptance Criteria:**

**Given** `pip install check-jsonschema` (ou via `uv`)  
**When** j’exécute la commande documentée dans README ou `OPENCLAW.md` sur `presentations/<fichier>.json`  
**Then** le schéma est appliqué et les erreurs sont affichées clairement  
**And** la commande est identique à celle de la CI

**Implements:** FR-6, NFR-4

### Story 1.3: Régénération batch des six PPTX existants

As an **animateur**,
I want **régénérer tous les PPTX des six épisodes fondation**,
So that **les fichiers reflètent le JSON et le générateur actuels**.

**Acceptance Criteria:**

**Given** les six JSON listés dans le README (outlook, personas, modeles, sharepoint-onedrive, prompts-avances, architecture-prompt)  
**When** j’exécute la boucle `./generate.sh` documentée dans le README  
**Then** chaque `La_Minute_Copilot_*.pptx` est produit sans erreur  
**And** chaque PPTX s’ouvre avec le thème Desjardins (fond menthe / vert selon type de slide)  
**And** les `speaker_notes` sont présentes pour chaque slide de contenu

**Implements:** FR-6, NFR-1, NFR-3

---

## Epic 2: Lancer la saison — six épisodes fondation

Présenter les six sujets initiaux en respectant le format 5 minutes et les personas.

### Story 2.1: Checklist animateur pré-session (5 min)

As an **animateur**,
I want **une checklist courte avant chaque présentation**,
So that **je respecte FR-1 à FR-3 sans dépasser le temps**.

**Acceptance Criteria:**

**Given** un PPTX généré pour l’épisode de la semaine  
**When** je suis la checklist (nouveau fichier `presentations/CHECKLIST-ANIMATEUR.md` ou section README)  
**Then** elle inclut : répétition chronométrée ≤6 min, une astuce démo + une astuce « essai cette semaine », message rassurant P2, aucune promo LLM hors Copilot  
**And** la checklist référence les personas ciblés pour l’épisode (table PRD §4.0)

**Implements:** FR-1, FR-2, FR-3, FR-9

### Story 2.2: Revue éditoriale des six JSON existants

As an **animateur**,
I want **revoir les six JSON pour conformité FR-7 et personas**,
So that **le contenu est prêt pour l’institution financière québécoise**.

**Acceptance Criteria:**

**Given** les six fichiers JSON du dépôt  
**When** je passe la revue (manuelle ou assistée)  
**Then** aucun exemple ne contient de données client réelles ou PII  
**And** le texte est en français  
**And** chaque épisode a au moins une astuce testable (FR-2)  
**And** les épisodes « personas » et « architecture-prompt » ciblent P2 explicitement

**Implements:** FR-2, FR-3, FR-7, FR-4 (partiel)

### Story 2.3: Planifier l’ordre de présentation des six épisodes

As an **animateur**,
I want **un ordre de diffusion des six premiers sujets avec alternance débutant/technique**,
So that **j’honore FR-5 sur le 2e mois de la saison**.

**Acceptance Criteria:**

**Given** la file PRD §4.0  
**When** je documente l’ordre dans `presentations/SAISON-ORDRE.md` (ou tableau README)  
**Then** au moins deux épisodes « débutant » (ex. outlook, personas) et deux « technique M365 » (ex. modeles, architecture-prompt) sont planifiés  
**And** aucun plus de deux épisodes « avancés » consécutifs  
**And** chaque ligne indique les personas P1–P3 principaux

**Implements:** FR-4, FR-5, FR-8 (partiel)

### Story 2.4: Présenter le premier épisode de la saison

As an **animateur**,
I want **présenter le premier épisode selon le plan**,
So that **la série démarre officiellement pour l’Audience TI**.

**Acceptance Criteria:**

**Given** FR-10 complété (sondage référence — Epic 3)  
**And** Story 2.3 ordre défini  
**When** je présente l’épisode 1 devant ~100 personnes  
**Then** la session dure ~5 minutes  
**And** j’enregistre la date et le sujet dans `SAISON-ORDRE.md` (statut : présenté)

**Implements:** FR-1, FR-8 (démarrage saison)

---

## Epic 3: Mesurer la montée en compétence Copilot

Documenter et exécuter les deux sondages — hors code applicatif.

### Story 3.1: Sondage de référence (avant épisode 1)

As an **animateur**,
I want **administrer et archiver le sondage de référence**,
So that **FR-10 soit satisfait avant le lancement**.

**Acceptance Criteria:**

**Given** un sondage existant ou à créer (Teams Forms, etc.)  
**When** je le diffuse à l’Audience TI **avant** le premier épisode  
**Then** les résultats sont exportés/archivés avec date  
**And** le sondage couvre au minimum : confiance Copilot, fréquence d’usage, perception risque emploi  
**And** une note dans `presentations/SONDAGES.md` documente l’emplacement de l’export

**Implements:** FR-10, métrique PRD §5

### Story 3.2: Gabarit sondage bilan (6 mois)

As an **animateur**,
I want **un sondage bilan aux mêmes dimensions que le référence**,
So that **FR-11 permet une comparaison avant/après**.

**Acceptance Criteria:**

**Given** le sondage référence (Story 3.1)  
**When** je prépare le sondage M6 (copie ou même formulaire avec nouvelle campagne)  
**Then** les questions comparables sont listées dans `SONDAGES.md`  
**And** la date cible (≥20 épisodes ou 6 mois calendaires) est notée

**Implements:** FR-11

### Story 3.3: Administrer le sondage bilan et synthétiser

As an **animateur**,
I want **collecter le sondage M6 et une synthèse courte**,
So that **je démontre l’efficacité perçue de la série**.

**Acceptance Criteria:**

**Given** ≥20 épisodes présentés ou échéance 6 mois  
**When** le sondage bilan est complété  
**Then** une synthèse (1–2 pages) compare confiance, usage et anxiété emploi vs référence  
**And** le fichier est référencé dans `SONDAGES.md`

**Implements:** FR-11, métriques PRD §5

---

## Epic 4: Produire les épisodes hebdomadaires suivants

Processus reproductible pour épisodes 7+ via OpenClaw.

### Story 4.1: Brief type Telegram pour OpenClaw

As an **animateur**,
I want **un modèle de message brief**,
So that **OpenClaw reçoive topic + use cases de façon constante**.

**Acceptance Criteria:**

**Given** `OPENCLAW.md`  
**When** j’ajoute un exemple de brief dans `OPENCLAW.md` ou `presentations/BRIEF-TEMPLATE.md`  
**Then** le modèle inclut : sujet, 2–4 use cases, personas cibles (P1/P2/P3), outil M365, contraintes (pas de PII, FR uniquement)  
**And** il renvoie à la checklist §6 d’OPENCLAW

**Implements:** NFR-4, UJ-4, architecture process pattern

### Story 4.2: Créer l’épisode 7 (premier hors lot initial)

As an **animateur**,
I want **produire et présenter le septième épisode**,
So that **la chaîne OpenClaw → JSON → PPTX est prouvée hors des six JSON initiaux**.

**Acceptance Criteria:**

**Given** un sujet choisi (ex. Teams, Word — hors des six existants)  
**When** OpenClaw produit `presentations/<slug>.json` et je valide + `./generate.sh`  
**Then** le JSON passe `check-jsonschema`  
**And** la présentation respecte FR-1, FR-2, FR-7, FR-9  
**And** `SAISON-ORDRE.md` est mis à jour (épisode 7, présenté)

**Implements:** FR-1, FR-2, FR-6, FR-7, FR-8, FR-9

### Story 4.3: Story répétable — épisode hebdo N

As an **animateur**,
I want **une story gabarit pour chaque nouvelle semaine**,
So that **les epics suivants du sprint puvent cloner le pattern**.

**Acceptance Criteria:**

**Given** Stories 4.1 et 4.2 comme référence  
**When** je crée l’épisode N de la semaine  
**Then** le flux est : brief → JSON OpenClaw → relecture → validation schéma → generate.sh → présentation → mise à jour SAISON-ORDRE  
**And** chaque épisode documente personas servis (FR-4)

**Implements:** FR-1 à FR-7, FR-9, FR-8 (incrémental)

_Note : dupliquer Story 4.3 comme tickets « Épisode 8 », « Épisode 9 », … jusqu’à ≥22 épisodes — ou utiliser `bmad-create-story` par numéro._

---

## Epic 5: Compléter la file éditoriale (~19 sujets)

Atteindre ~25 épisodes avec couverture P1–P3.

### Story 5.1: Brainstorm et ROADMAP des sujets restants

As an **animateur**,
I want **une liste priorisée des ~19 sujets restants**,
So that **OQ-5 PRD soit résolue et FR-8 planifiable**.

**Acceptance Criteria:**

**Given** les six sujets déjà dans le dépôt  
**When** je crée `presentations/ROADMAP.md`  
**Then** la liste contient ≥15 sujets additionnels (Teams, Word, Excel, Quick Parts, sécurité prompts, etc.)  
**And** chaque ligne a : titre, personas (P1/P2/P3), niveau (débutant/technique), statut (à faire / en cours / fait)  
**And** la somme faites + à faire vise ≥25 épisodes saison

**Implements:** FR-4, FR-5, FR-8, OQ-5

### Story 5.2: Vérifier couverture personas fin de saison

As an **animateur**,
I want **auditer la ROADMAP + épisodes présentés**,
So that **P1, P2 et P3 ont chacun ≥1 épisode dédié sur la saison**.

**Acceptance Criteria:**

**Given** `ROADMAP.md` et `SAISON-ORDRE.md`  
**When** j’exécute l’audit (tableau personas × épisodes)  
**Then** chaque persona P1, P2, P3 a au moins un épisode marqué « principal »  
**And** les lacunes ont un sujet assigné dans ROADMAP avec date cible

**Implements:** FR-4, métrique couverture personas §5 PRD

---

## Final Validation Summary

| Check | Résultat |
|-------|----------|
| Tous les FR couverts | ✅ FR-1 à FR-11 mappés |
| Pas de dépendance avant vers l’avant (epics) | ✅ Epic 3.1 avant 2.4 ; Epic 1 avant 4 |
| Stories taille agent unique | ✅ |
| Brownfield starter | ✅ Pas de story « greenfield » — Epic 1 = CI + batch |
| UX-DR | N/A |
| File churn | ✅ Epics séparés par valeur (outil / lancement / mesure / production / planification) |

**Statut :** prêt pour `bmad-sprint-planning` ou `bmad-create-story` sur Story 1.1.

**Prochaine étape BMad :** **[SP]** `bmad-sprint-planning` ou **[IR]** `bmad-check-implementation-readiness`
