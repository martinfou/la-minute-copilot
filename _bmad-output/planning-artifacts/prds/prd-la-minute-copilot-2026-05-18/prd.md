---
title: La minute Copilot
status: final
created: 2026-05-18
updated: 2026-05-19
---

# PRD: La minute Copilot

## 0. Document Purpose

Ce PRD décrit la **série hebdomadaire** « La minute Copilot » et les exigences pour **produire et maintenir** ses épisodes au sein du département TI d’une institution financière québécoise (~100 contributeurs). Il s’adresse à l’animateur/propriétaire du produit, aux workflows BMAD en aval (UX si pertinent, architecture de la chaîne de production, epics/stories) et aux parties prenantes qui valident le périmètre.

**Entrées existantes :** dépôt `la-minute-copilot` (6 épisodes JSON/PPTX, schéma, générateur Python), `_bmad-output/project-context.md`, `OPENCLAW.md` (guide agent). Détails techniques OpenClaw : `addendum.md`.

**Structure :** glossaire ancré, fonctionnalités groupées avec FR numérotés globalement, hypothèses en `[ASSUMPTION]`.

---

## 1. Vision

Le département a reçu les outils **Microsoft Copilot** (écosystème M365) **sans formation structurée**. Le niveau de connaissance et les compétences sont **très inégaux** : certains collègues n’osent pas commencer, d’autres bricolent des prompts sans méthode, et les gestionnaires comme les adjoints administratifs n’ont pas les mêmes besoins qu’un développeur ou un QA.

**La minute Copilot** comble ce vide par une **présentation hebdomadaire de cinq minutes** : trucs et astuces **concrets** pour être **plus performant avec Copilot** au quotidien — pas un cours magistral, pas une démo produit complète. Chaque épisode laisse l’audience avec **une ou deux actions applicables** la semaine suivante (ex. résumer un fil Outlook, structurer un persona dans un prompt, choisir le bon mode Copilot Web).

Sur **environ six mois** (~**25 épisodes**), l’objectif est que le département **monte en maîtrise** : moins de friction, des prompts plus utiles, et une culture où Copilot est un **levier d’efficacité** partagé — mesuré par **deux sondages** (référence avant la série, bilan à six mois) et la livraison de la saison (voir §5).

La **production** s’appuie sur une chaîne reproductible : l’animateur fournit un **sujet** et des **cas d’usage originaux** ; **OpenClaw** (agent local, contact Telegram, accès au dépôt) génère le **JSON** de l’épisode ; le **générateur Python** produit le **PowerPoint** aligné sur la charte visuelle institutionnelle (thème Desjardins dans le dépôt actuel). L’animateur reste seul responsable de la **présentation en séance** et du **choix éditorial**.

**Hors vision / hors scope produit :** autres LLM que Copilot (ChatGPT standalone, Claude, etc.) ; formation certifiante longue ; enregistrement vidéo ou portail e-learning comme produit principal `[ASSUMPTION: enregistrements ad hoc possibles sans être dans le scope v1]`.

**Piste éditoriale v1 :** les **développeurs et profils techniques** restent dans la **minute hebdo** — beaucoup utilisent surtout **GitHub Copilot** et **n’explorent pas** le reste de l’offre IA Microsoft (M365, Copilot Web, etc.). Des épisodes M365 leur sont donc **explicitement destinés**, en complément d’éventuelles astuces GitHub dans certains numéros `[ASSUMPTION: pas de série parallèle obligatoire en v1]`.

---

## 2. Target User

L’**audience primaire** est le **département TI** (~100 personnes). Le produit sert trois archétypes d’audience + l’animateur. Les épisodes alternent des sujets **grand public TI** et des sujets qui **ramènent les profils techniques** vers M365.

### 2.1 Personas (audience)

#### P1 — Débutant prudent *(persona primaire pour le ton éditorial)*

**Qui :** adjoints administratifs, gestionnaires peu techniques, contributeurs qui n’ont presque jamais ouvert Copilot.

**Contexte :** manque d’**inspiration** — ne savent pas quoi faire au-delà de traiter Copilot **comme Google** (question-réponse générique, pas de scénario métier).

**Besoin émotionnel :** se sentir capable sans passer pour « nul » devant les pairs.

#### P2 — Utilisateur anxieux

**Qui :** Scrum Masters, PO proxy, analystes d’affaires, QA, rôles « métier-agile » exposés au changement IA.

**Contexte :** **peur que Copilot vole leur emploi** ou dévalue leur expertise ; usage timide ou évitement.

**Besoin émotionnel :** voir Copilot comme **assistant** (gain de temps sur le répétitif), pas comme remplacement — avec preuves concrètes en 5 minutes.

#### P3 — Power user technique (angle M365)

**Qui :** développeurs, QA technique, profils qui vivent dans **GitHub Copilot** au quotidien.

**Contexte :** **sous-explorent** Outlook, Teams, Word, Excel, **Copilot Web**, SharePoint/OneDrive avec Copilot.

**Besoin fonctionnel :** astuces **actionnables** sur l’écosystème Microsoft qu’ils ignorent — **dans la série hebdo**, pas relégués à un autre canal.

#### P4 — Animateur (propriétaire du produit)

**Qui :** Martin Fournier (v1) — seul auteur, validateur et présentateur.

**Contexte :** cadence hebdo, ~25 épisodes sur 6 mois, production assistée par OpenClaw.

### 2.2 Jobs To Be Done

**P1 — Débutant prudent**
- Quand j’ai cinq minutes après la présentation, je veux **savoir quoi faire concrètement** dans un outil que j’utilise déjà (souvent Outlook ou courriel), afin de **essayer une astuce** sans lire de documentation.
- Quand je formule une question à Copilot, je veux **un modèle de prompt** simple (persona, contexte), afin d’obtenir quelque chose d’utile au lieu d’une réponse générique « Google ».

**P2 — Utilisateur anxieux**
- Quand j’entends parler d’IA au travail, je veux **voir un cas où Copilot augmente ma marge de manœuvre** (résumer, brouillon, tri), afin de **réduire la peur** de remplacement.
- Quand je reprends le travail la semaine suivante, je veux **réutiliser une astuce à faible risque** (pas de données sensibles en démo), afin de **tester sans engagement long**.

**P3 — Power user technique**
- Quand je suis déjà à l’aise avec GitHub Copilot, je veux **découvrir un levier M365** pertinent pour mon travail (réunion, spec, courriel), afin d’**élargir** mon usage sans changer d’outil principal pour le code.
- Quand un épisode porte sur Copilot Web ou le cycle de vie d’un prompt en entreprise, je veux **comprendre les modes et limites** (rapide vs raisonnement), afin de **choisir le bon mode** pour la tâche.

**P4 — Animateur**
- Quand la session hebdo approche, je veux **transformer un sujet + des cas d’usage originaux** en diapositives **prêtes à présenter** (JSON + PPTX conformes à la charte), afin de **tenir la cadence** sans construire manuellement chaque slide.
- Quand je briefe OpenClaw sur Telegram, je veux **itérer sur le contenu** (titres, cartes, notes présentateur) dans le dépôt, afin de **présenter un épisode fiable** en cinq minutes devant ~100 personnes.
- Quand je planifie la saison (~25 épisodes), je veux **une file de sujets** qui couvre le spectre P1–P3, afin que **personne ne reste sur « Copilot = Google »** ni sur « Copilot = menace » ni sur « seul GitHub compte ».

### 2.3 Non-Users (v1)

- Collaborateurs hors **département TI** (sauf invités ponctuels en audience).
- Utilisateurs cherchant une formation **non-Copilot** ou un autre fournisseur LLM.
- Équipes sans accès/licence M365 Copilot `[ASSUMPTION: accès Copilot déjà déployé pour l’audience cible]`.
- Personnes attendant une **formation diplômante** ou un parcours e-learning complet (hors format 5 min).

### 2.4 Key User Journeys

- **UJ-1. Sophie (adjointe admin) essaie sa première astuce Outlook après l’épisode.**
  - **Persona + contexte :** P1 ; utilise Outlook toute la journée, n’a jamais cliqué sur Copilot.
  - **Entry state :** assise à la session hebdo (présentiel ou Teams) ; authentifiée M365.
  - **Path :** écoute 5 min → note « Résumer ce fil » → le lendemain ouvre un long fil → Copilot → Summarize → lit le résumé.
  - **Climax :** comprend qu’elle a **gagné du temps** sans « poser une question Google ».
  - **Resolution :** répète sur un autre fil ; éventuellement partage l’astuce à un collègue.
  - **Edge case :** fil vide ou Copilot indisponible → retente avec un fil plus long ou signale au support interne `[ASSUMPTION]`.

- **UJ-2. Marc (Scrum Master) reprend confiance après un épisode « persona ».**
  - **Persona + contexte :** P2 ; craint que l’IA remplace la facilitation.
  - **Entry state :** sceptique en début de session.
  - **Path :** voit une démo où Copilot **structure** un compte-rendu à partir de notes brutes → reçoit un **modèle de prompt avec persona « facilitateur agile »** → teste sur un vrai compte-rendu (données non sensibles).
  - **Climax :** le brouillon lui fait **gagner 20 minutes** ; il voit son rôle comme **celui qui valide et affine**, pas remplacé.
  - **Resolution :** réutilise le persona la semaine suivante pour un autre rituel.

- **UJ-3. Léa (développeuse) découvre Copilot Web en session.**
  - **Persona + contexte :** P3 ; vit dans VS Code + GitHub Copilot.
  - **Entry state :** assiste à l’épisode « modèles Copilot Web » par obligation ou curiosité.
  - **Path :** comprend Auto vs Quick vs Think Deeper → choisit **Think Deeper** pour décortiquer un spike technique → compare avec ce qu’elle aurait fait dans l’IDE.
  - **Climax :** identifie **un cas où M365 Copilot Web** bat GitHub Copilot (ex. synthèse multi-doc non-code).
  - **Resolution :** ouvre Copilot Web au moins une fois dans la semaine pour une tâche non-code.

- **UJ-4. Martin prépare l’épisode de la semaine avec OpenClaw.**
  - **Persona + contexte :** P4 ; sujet choisi dans la file éditoriale (ex. SharePoint).
  - **Entry state :** idée + 2–3 use cases originaux notés.
  - **Path :** message Telegram à OpenClaw → JSON généré dans `presentations/` → relecture (ton FR, pas de données réelles sensibles) → `./generate.sh` → test PPTX → ajustements JSON si besoin → présentation vendredi.
  - **Climax :** diapo **conforme charte** + notes présentateur utilisables en 5 min.
  - **Resolution :** épisode archivé dans le dépôt ; sujet suivant planifié.
  - **Edge case :** JSON invalide au schéma → correction manuelle ou re-prompt OpenClaw avant génération.

---

## 3. Glossary

| Terme | Définition |
|-------|------------|
| **Épisode** | Une présentation hebdomadaire : un fichier JSON source + PPTX généré. |
| **Animateur** | Personne qui choisit le sujet, pilote OpenClaw, valide le JSON, présente en séance (P4, v1). |
| **OpenClaw** | Agent IA local joignable par Telegram ; produit le JSON à partir du brief animateur. |
| **Chaîne de production** | Brief → JSON (schéma) → `generate_pptx.py` → PPTX. |
| **Audience TI** | ~100 contributeurs du département informatique. |
| **Débutant prudent** | Persona P1 — manque d’inspiration, usage type moteur de recherche. |
| **Utilisateur anxieux** | Persona P2 — crainte de remplacement par l’IA. |
| **Power user technique** | Persona P3 — fort sur GitHub Copilot, faible sur M365 Copilot. |
| **Astuce** | Action ou prompt reproductible en ≤5 min de démo + essai personnel. |
| **Persona (prompt)** | Rôle + contexte + ton donnés à Copilot pour cadrer la réponse — distinct des personas PRD P1–P4. |

---

## 4. Features

### 4.0 File éditoriale (sujets identifiés)

Priorité initiale alignée sur le dépôt existant et la liste animateur. Les **6 premiers** ont un JSON dans `presentations/` ; ~**19 épisodes** additionnels à planifier pour atteindre ~25.

| Priorité | Sujet | Personas ciblés | JSON existant |
|----------|-------|-------------------|---------------|
| 1 | Cycle de vie d’un prompt — de l’usage à Copilot en entreprise | P2, P3 | `architecture-prompt.json` |
| 2 | Modèles Copilot Web (Auto, rapide, Think Deeper) | P1, P3 | `modeles.json` |
| 3 | Copilot dans Outlook | P1, P2 | `outlook.json` |
| 4 | Personas dans les prompts | P1, P2 | `personas.json` |
| 5 | Prompts avancés (CoT, ToT, Red/Blue Team, etc.) | P2, P3 | `prompts-avances.json` |
| 6 | SharePoint / OneDrive + Copilot | P1, P3 | `sharepoint-onedrive.json` |
| — | *~19 sujets à définir* (Teams, Word, Excel, Planner, sécurité des prompts, Quick Parts, etc.) | P1–P3 | — |

_Règle éditoriale :_ chaque nouvel épisode indique en interne quels **personas P1–P3** il sert principalement.

### 4.1 Format et expérience de la série *(must-have v1 — bloc A)*

**Description :** Chaque session hebdomadaire respecte un format court et prévisible pour ~100 personnes du TI. L’expérience privilégie l’**action** sur la théorie. Réalise UJ-1, UJ-2, UJ-3.

#### FR-1: Session de cinq minutes

L’**Animateur** peut présenter un **Épisode** en **cinq minutes** (± une minute de marge) devant l’**Audience TI**. Réalise UJ-1, UJ-2, UJ-3.

**Consequences (testable):**
- Le script présentateur (`speaker_notes`) tient en **≤6 minutes** à voix normale lors d’une répétition.
- La diapositive de type `summary` clôt l’épisode avec récap et bonus actionnable.

#### FR-2: Astuce actionnable par épisode

L’**Audience TI** peut identifier **au moins une astuce** applicable dans la semaine suivant l’**Épisode**. Réalise UJ-1, UJ-2.

**Consequences (testable):**
- Chaque épisode inclut au moins une **Astuce** démontrable (outil M365 nommé + geste utilisateur).
- Les notes présentateur décrivent une **démo** ou un **essai personnel** en une phrase.

#### FR-3: Ton rassurant pour l’utilisateur anxieux

L’**Animateur** peut présenter le contenu de façon à positionner Copilot comme **assistant** (gain de temps, validation humaine), sans narratif de remplacement du métier. Réalise UJ-2.

**Consequences (testable):**
- Aucune diapositive ne contient de formulation du type « Copilot fait votre travail à votre place » sans nuance de contrôle humain.
- Au moins un épisode sur la file §4.0 cible explicitement **P2** (ex. personas, cycle de vie du prompt).

#### FR-4: Ciblage persona par épisode

L’**Animateur** peut documenter, pour chaque **Épisode**, quels personas **P1**, **P2** et/ou **P3** sont principalement servis. Réalise UJ-4.

**Consequences (testable):**
- La file éditoriale §4.0 (ou métadonnée interne) indique **≥1 persona** par épisode planifié.
- Sur ~25 épisodes, la file couvre **P1, P2 et P3** au moins une fois chacun.

#### FR-5: Alternance des niveaux de difficulté

L’**Animateur** peut enchaîner des sujets **accessibles** (P1) et des sujets **élargissant M365** pour P3, sans série parallèle. Réalise UJ-3.

**Consequences (testable):**
- Parmi les 6 premiers sujets §4.0, au moins **deux** sont classés « débutant » et **deux** « technique M365 » dans la file.
- Les épisodes restants planifiés maintiennent cette alternance `[ASSUMPTION: pas plus de deux épisodes « avancés » consécutifs]`.

#### FR-6: Structure visuelle standardisée

L’**Épisode** respecte les types de diapositives du schéma (`title`, `tips`, `bonus`, `summary`) et la charte visuelle du dépôt. Réalise UJ-4.

**Consequences (testable):**
- Le JSON valide contre `schema/la-minute-copilot.schema.json`.
- Le PPTX généré utilise le thème Desjardins (pas d’émojis sur les slides — voir `project-context.md`).

#### FR-7: Contenu en français institutionnel

L’**Audience TI** reçoit un contenu entièrement en **français** adapté au contexte québécois et à une institution financière. Réalise UJ-1, UJ-2, UJ-3.

**Consequences (testable):**
- Titres, cartes, puces et `speaker_notes` sont en français.
- Les exemples de prompts n’incluent pas de données client réelles ni d’informations confidentielles.

### 4.2 Livraison de la saison *(must-have v1)*

**Description :** La série couvre environ six mois de sessions hebdomadaires avec une progression éditoriale cohérente.

#### FR-8: Saison d’environ vingt-cinq épisodes

L’**Animateur** peut livrer **environ 25 Épisodes** sur **six mois** (une session par semaine, hors congés `[ASSUMPTION: reports documentés dans la file]`). Réalise UJ-4.

**Consequences (testable):**
- **≥22 Épisodes** présentés sur la période (marge pour absences).
- Les **6** sujets §4.0 sont présentés au plus tard avant la fin du **2e mois** `[ASSUMPTION: ordre ajustable]`.

#### FR-9: Périmètre Copilot exclusif

L’**Épisode** ne promeut ni ne forme sur des LLM **hors écosystème Copilot** (ChatGPT, Claude, etc.). Réalise la vision §1.

**Consequences (testable):**
- Aucune diapositive ne présente un concurrent non-Copilot comme alternative recommandée.
- GitHub Copilot n’apparaît que comme complément ponctuel, pas comme sujet principal de plus de **2** épisodes sur 25.

### 4.3 Mesure d’impact *(must-have v1 — sondages)*

**Description :** L’efficacité perçue et l’évolution des compétences sont mesurées par **deux sondages** : référence avant le lancement de la série, puis bilan à six mois.

#### FR-10: Sondage de référence (avant La minute Copilot)

L’**Animateur** (ou le département) peut administrer un **sondage de référence** à l’**Audience TI** **avant** le premier **Épisode** de la série.

**Consequences (testable):**
- Les résultats sont **conservés** (export ou copie) avec une date antérieure au premier épisode.
- Le sondage couvre au minimum : niveau de confiance avec Copilot, fréquence d’usage, perception du risque emploi `[ASSUMPTION: questions exactes définies hors PRD]`.

#### FR-11: Sondage de bilan (six mois)

L’**Animateur** (ou le département) peut administrer un **second sondage** à l’**Audience TI** **vers six mois** après le début de la série, sur une base **comparable** au sondage FR-10.

**Consequences (testable):**
- Les mêmes dimensions que FR-10 sont mesurées pour permettre une **comparaison avant/après**.
- Le bilan est produit **après ≥20 Épisodes** présentés ou à l’échéance calendaire de six mois (le plus tard des deux).

### 4.4 Chaîne de production *(existante — hors extension must-have v1)*

**Description :** La production d’**Épisodes** s’appuie sur la **Chaîne de production** déjà en place (OpenClaw → JSON → PPTX). Le PRD v1 **n’exige pas** de nouvelles capacités sur ce bloc (pas de CI obligatoire, pas de portail self-service) — seulement son **usage** pour satisfaire les FR §4.1–4.3.

**Capacités existantes réputées suffisantes pour v1 :**
- Brief Telegram → JSON dans `presentations/`
- `./generate.sh` → PPTX charte Desjardins
- Schéma JSON, `OPENCLAW.md`, `project-context.md` pour guider OpenClaw

`[ASSUMPTION: améliorations post-v1 — validation CI (`check-jsonschema`), checklist brief — sauf besoin urgent.]`

---

## 5. Success Metrics

| Métrique | Cible v1 | Source |
|----------|----------|--------|
| **Sondage référence** | Complété avant épisode 1 | Sondage pré-série (FR-10) |
| **Sondage bilan 6 mois** | Complété vers M6 ; comparable au référence | Sondage post-série (FR-11) |
| **Épisodes livrés** | ≥22 / ~25 planifiés | Calendrier animateur |
| **Couverture file §4.0** | 6 sujets initiaux présentés | Inventaire dépôt |
| **Couverture personas** | P1, P2, P3 chacun servis ≥1 fois dans la saison | File éditoriale §4.0 |
| **Efficacité perçue** | Amélioration mesurable sur les items communs des deux sondages (ex. confiance, fréquence d’usage) | Comparaison FR-10 vs FR-11 |
| **Anxiété emploi (P2)** | Baisse des réponses indiquant peur de remplacement `[ASSUMPTION: item présent dans les deux sondages]` | Comparaison FR-10 vs FR-11 |

**Contre-métrique :** la série ne doit pas augmenter l’usage de LLM **non-Copilot** au département (pas de métrique formelle v1 — vigilance qualitative).

---

## 6. Open Questions

| ID | Question | Bloquant ? |
|----|----------|------------|
| OQ-1 | ~~Mesure à 6 mois ?~~ → **Résolu :** sondage référence + sondage à 6 mois (FR-10, FR-11) | — |
| OQ-2 | ~~GitHub Copilot : série hebdo ou rencontre séparée ?~~ → **Résolu** | — |
| OQ-3 | Validation compliance/contenu avant présentation (relecteur, checklist) ? | Non |
| OQ-4 | ~~JTBD animateur P4 ?~~ → **Validé** | — |
| OQ-5 | Liste des ~19 épisodes restants : brainstorm dédié ou file au fil de l’eau ? | Non |
| OQ-6 | Questions exactes des deux sondages (à documenter hors PRD ou en annexe) ? | Non |

---

## 7. Usage & prochaines étapes BMad

**Pour l’animateur :** ce PRD fixe le *quoi* et le *pour qui* ; `OPENCLAW.md` et le schéma JSON fixent le *comment* produire chaque épisode.

**Workflows recommandés (nouvelle conversation chacun) :**

| Priorité | Code | Skill | Pourquoi |
|----------|------|-------|----------|
| 1 | **[CA]** | `bmad-create-architecture` | Documenter la chaîne OpenClaw → JSON → PPTX si vous ajoutez CI, validation ou évolutions outils |
| 2 | **[CE]** | `bmad-create-epics-and-stories` | Découper la saison (~25 épisodes), sondages, améliorations pipeline |
| 3 | **[IR]** | `bmad-check-implementation-readiness` | Avant de lancer un sprint d’implémentation sur le dépôt |
| — | **[QQ]** | `bmad-quick-dev` | Nouvel épisode, `check-jsonschema`, petits changements générateur |
| — | **[BH]** | `bmad-help` | Réorientation |

**Questions ouvertes reportées (non bloquantes) :** OQ-3 (compliance), OQ-5 (file des 19 sujets), OQ-6 (libellés sondages) — propriétaire : Animateur ; réviser en cours de saison.
