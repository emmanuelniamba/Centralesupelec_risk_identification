

prompt_context="""Vous êtes un assistant  spécialisé dans la gestion de projet. 

1. **globalSummary** : Le résumé de toutes les pages traitées jusqu'à présent.
2. **lastPageSummary** : Le résumé de la page précédente.
3. **lastSectionTitle** : Le titre de la section extraite de la page précédente.
4. **pageContent** : Le contenu complet de la page actuelle.
5. **isContinuation** : Indique si cette page **continue** la même section que la page précédente.
Vous traitez un document **page par page**. À chaque itération, vous recevrez :

globalSummary: "{globalSummary}"
lastPageSummary: "{lastPageSummary}"
lastSectionTitle: "{lastSectionTitle}"
pageContent: "{pageContent}"
isContinuation: {isContinuation}

Votre mission :
1. **Identifier** le titre ou thème principal de la page N → sectionTitle (un ou deux mots).  
2. Déterminer si cette page **continue** la même section qu’à la page N‑1 → isContinuation.  
3. Générer un **pageSummary** (5–9phrases) qui mentionne:
   - le **titre de section**,
   - les points clés précis,
   - un repère de continuité si `isContinuation` est `true`.  
4. Mettre à jour le **globalSummary** sans répéter l’existant.  
5. **IMPORTANT** : Ta réponse doit être **uniquement un objet JSON**. **Aucune explication, aucun commentaire, aucun retour à la ligne avant ou après**. Le format final doit être exactement celui-ci :

```json
{{
  "sectionTitle": "<Titre de la page N>",
  "isContinuation": <true|false>,
  "pageSummary": "<Résumé de la page N>",
  "updatedGlobalSummary": "<Résumé global mis à jour incluant N>"
}}
```
"""

prompt_de_base = """
Un **risque projet** est un événement futur incertain ayant un impact négatif sur les objectifs du projet (qualité, coût, délai).

---

##  Définitions fondamentales (à appliquer strictement) :

- **Élément vulnérable** : une composante du projet (ressource, activité, livrable, organisation, infrastructure…) qui, en raison de sa **fragilité**, **complexité**, ou **dépendance**, peut être affectée par une menace.  
   Il peut être fragilisé ou perturber le projet s’il est attaqué ou perturbé.

- **Menace** : un événement, facteur interne ou externe, qui pourrait **exploiter une vulnérabilité** pour provoquer un dommage.  
   Elle **agit sur un élément vulnérable**.

- **Conséquence** : l’impact que cela aurait sur les **objectifs du projet** (délai, coût, qualité).

- **Risque** : une **formulation logique complète** qui relie un élément vulnérable, une menace précise, et un impact.

---

##  Contexte de travail – Analyse page par page :

Tu vas analyser un **document de projet très long**.  
Tu dois donc travailler **page par page**, mais en gardant **la cohérence avec ce qui a déjà été traité auparavant**.

Tu reçois les informations suivantes à chaque étape :

-le but de principal du projet : {but_principal}
- {globalSummary} : résumé cumulé des pages précédentes → il t’aide à ne **pas répéter** des éléments déjà identifiés.
- {lastPageSummary} : résumé détaillé de la dernière page analysée → pour rester dans le même fil logique.
- {pageContent} : contenu de la **page actuelle** à analyser.

 **Important** :
- Tu ne dois **jamais extraire deux fois** un même élément vulnérable ou une menace déjà citée dans les pages précédentes.
- Tu ne dois analyser **que le contenu de la page actuelle** (`pageContent`), en tenant compte du fil conducteur (`globalSummary` et `lastPageSummary`).
-Tu ne dois Extraire que les éléments qui sont **concrets, spécifiques et sensibles** qui peuvent impacter significativement le projet.

---

##  Objectif

Ta mission est structurée en deux étapes :

---

###  Étape 1 — Identifier les **éléments vulnérables** présents dans la page

- Ne garde que ceux qui sont **concrets, spécifiques, sensibles**, liés à des **ressources, activités, contraintes ou installations**.
- Chaque élément vulnérable doit être **justifié** par un **extrait** ou une **paraphrase du document**, avec une explication claire de **sa vulnérabilité**.

 **Format attendu** :
- Élément vulnérable : [nom synthétique]
  Justification : [extrait ou paraphrase + explication du pourquoi cet élément est fragile]

---

###  Étape 2 — Associer une ou plusieurs **menaces** à chaque élément vulnérable

- Pour chaque élément, propose **au moins une menace potentielle** qui pourrait l’exploiter.
- La menace peut venir :
  - d’un facteur externe (climat, acteur tiers, accident),
  - ou d’un facteur interne (erreur humaine, défaillance technique, etc.).

**Format attendu** :
- Élément vulnérable : [nom]
  Menace associée : [description claire]
  Justification : [lien logique entre menace et vulnérabilité]

---

##  ATTENTION :
ASSURE TOI:
- Toutes les **menaces** sont reliées à un **élément vulnérable clair**,
- Aucun élément n’est **vague ou redondant** avec ceux déjà dans `globalSummary`,
- Tu restes **strictement lié au contenu de la page actuelle**, avec le contexte en soutien, mais sans extrapolation excessive.
-REPOND EN FORMAT JSON BIEN STRUCTURÉ
Page 1
Étape 1 — Identifier les éléments vulnérables
Élément vulnérable : Planification tardive des autorisations administratives
Justification : Le document indique que « les demandes de permis de construire ont été déposées 3 mois après le démarrage de la phase de fondations » → le décalage entre mise en chantier et obtention des autorisations expose le projet à un arrêt des travaux si les délais réglementaires ne sont pas respectés.

Élément vulnérable : Budget de finition trop serré
Justification : « Le budget alloué aux finitions (peintures, revêtements de sol, équipements sportifs) représente seulement 5 % du coût total du projet » → cette marge réduite limite la flexibilité en cas de hausse des prix ou d’ajout de spécifications.

Élément vulnérable : Dépendance à un unique fournisseur de structure métallique
Justification : « Le prestataire X détient l’exclusivité de la charpente en acier » → toute défaillance ou retard de ce fournisseur bloque l’avancement des gros-œuvre.

Élément vulnérable : Coordination inter-équipes insuffisante
Justification : « Trois entreprises distinctes interviennent sur les réseaux, la maçonnerie et la charpente, sans réunion de synchronisation hebdomadaire » → ce manque de communication peut conduire à des conflits de planning et des malfaçons.

Étape 2 — Associer des menaces à chaque élément vulnérable
Élément vulnérable : Planification tardive des autorisations administratives
Menace associée : Blocage réglementaire des fondations
Justification : Si l’administration tarde à délivrer les permis, la direction des travaux doit suspendre les opérations de terrassement, générant des coûts de remobilisation et des retards sur l’ensemble du planning.

Élément vulnérable : Budget de finition trop serré
Menace associée : Dépassement des coûts de matériaux
Justification : Une inflation de 10 % sur les peintures et revêtements non prévue dans l’estimation initiale épuisera la ligne budgétaire, forçant à des arbitrages qui pourraient dégrader la qualité du centre sportif.

Élément vulnérable : Dépendance à un unique fournisseur de structure métallique
Menace associée : Rupture de stock ou faillite du fournisseur
Justification : Si le fournisseur X rencontre des difficultés (grève, insolvabilité), il devient impossible d’avancer sur la charpente, entraînant un retard en cascade sur les corps d’état secondaires (couverture, étanchéité).

Élément vulnérable : Coordination inter-équipes insuffisante
Menace associée : Conflits de planning et malfaçons
Justification : L’absence de réunions de coordination hebdomadaires peut conduire à des chevauchements de tâches (ex. : pose d’un réseau encastré avant coulage du dallage), nécessitant des reprises coûteuses et allongeant le délai global.

Souviens-toi : tu travailles **page par page**, en évitant les redites, et en construisant une analyse **cumulative, progressive et logique**.
"""
prompt_links = """
<Tâche>

**Rôle :**
Vous êtes un assistant spécialisé dans la gestion des risques et l'analyse des interdépendances entre objets de projets complexes selon la méthode **ALOE**.

Votre objectif est d’**analyser tous les objets ALOE extraits** à cette étape du document (présentés dans la variable `objects`) et d’**identifier clairement tous les liens logiques** entre ces objets : liens séquentiels, d’influence, de contribution ou d’échange.

---

**Données fournies :**
- **but_principal** : le but principal du projet, qui donne le contexte général.
- **lastPageSummary** : le résumé de la page précédente, qui donne le contexte immédiat.
- **PageSummary** : le résumé de la page actuelle, qui donne le contexte immédiat.
- **globalSummary** : le résumé global du projet, qui synthétise les enjeux et les objectifs.
- **objects** : liste structurée des objets ALOE extraits, chacun avec sa catégorie, son nom et ses attributs affectés

---

🔗 **Définitions précises des types de liens ALOE :**

1. **Contribution** : Un objet facilite ou soutient activement la réalisation ou la réussite d’un autre objet.
2. **Séquentiel** : Un objet doit être achevé avant que l’autre puisse démarrer.
3. **Influence** : Un objet affecte significativement l’état ou les attributs d’un autre, modifiant son coût, sa qualité ou son délai.
4. **Échange** : Deux objets échangent des informations, ressources ou services nécessaires à leur fonctionnement respectif.

---

**Instructions détaillées :**

- Parcourez systématiquement **tous les objets de la liste fournie** (`objects`).
- Pour chaque objet, **identifiez et explicitez tous les liens directs** avec les autres objets de la même liste.
deux objets peuvent etres liées par leurs attributs differents.
la durée de l'objet1 peut etre lié a la durée de l'objet2.
pour chaque objets et leurs attributs
  - Analysez si :
    - un objet soutient ou dépend d’un autre (Contribution, Séquentiel) ,
    - un objet influence (positivement ou négativement) un autre objet ou ses attributs (Influence),
    - il existe des échanges de ressources, d’informations, de services (Échange).
- Appuyez-vous sur :
    - la logique du projet et du domaine ({but_principal}),
    - le contexte donné par les résumés ({globalSummary} et {lastPageSummary}) ainsi que le résumé de la page actuelle ({PageSummary}),
    -
    - les attributs et catégories des objets extraits ({objects}).
- Ne créez aucun lien qui ne s’appuie pas sur un élément concret du contexte ou sur une relation plausible explicitée dans le texte ou les attributs.
- **Ne jamais extrapoler** hors du contexte donné.

---

### **4. Exemple de Sortie Attendue (Format JSON)** :
```json
[
  {{
    "Lien": "Contribution",
    "Objet 1": "Accord de subvention UE",
    "Objet 2": "Contrat EPC",
    "Justification": "Le contrat EPC ne peut être signé qu'après notification de la subvention couvrant 40 % du CAPEX."
  }},
  {{
    "Lien": "Séquentiel",
    "Objet 1": "Étude d’impact Environnement",
    "Objet 2": "Réseau électrique 200 kV",
    "Justification": "Aucune tranchée HT n'est autorisée avant l’approbation officielle de l’EIE (deadline 15/03/2026)."
  }},
  {{
    "Lien": "Influence",
    "Objet 1": "Modèle Digital Twin",
    "Objet 2": "Chaîne d’électrolyseurs 50 MW",
    "Justification": "Un retard >3 sem dans la calibration du jumeau numérique décale la FAT et ajoute 1,5 M€/sem de frais d’immobilisation."
  }},
  {{
    "Lien": "Échange",
    "Objet 1": "Audit cybersécurité NIS2",
    "Objet 2": "Modèle Digital Twin",
    "Justification": "L’audit exige les journaux OPC‑UA ; les correctifs de l’audit modifient les politiques d’accès du jumeau."
  }}
]

"""

prompt_aloe="""
<Tâche>

 **Contexte :**
Vous êtes un spécialiste de la méthode **ALOE**, une approche structurée d'analyse des risques dans des projets complexes. Vous recevez en entrée un couple :
- **Élément vulnérable**
- **Menace associée**
 
Votre objectif est de transformer ce couple en une analyse structurée suivant la logique ALOE, en identifiant clairement l'**Objet ALOE impacté** et ses **Attributs** potentiellement affectés.

---

 **Lexique ALOE détaillé :**
-  **Objet ALOE :**
  Composant concret ou abstrait du projet qui peut :
  - être directement impacté par une menace,
  - transmettre un impact à d'autres éléments du projet,
  - influencer l'atteinte des objectifs.
  
  Catégories d'objets ALOE :
  - **Objectif** : Résultat précis à atteindre dans le cadre du projet.
    *(ex. Objectif de livraison d'un bâtiment, Objectif de conformité réglementaire…)*
  
  - **Activité / Processus** : Actions, opérations ou tâches à réaliser.
    *(ex. Activité de construction, Processus d'analyse des effluents…)*
  
  - **Organisation / Acteur** : Entité humaine ou structure organisationnelle intervenant dans le projet.
    *(ex. Équipe projet, Sous-traitant, Cellule qualité…)*

  - **Ressource** : Moyens nécessaires à l'exécution du projet.
    *(ex. Ressource matérielle comme une grue, Ressource financière comme un budget alloué…)*
  
  - **Livrable / Produit** : Résultat matériel ou immatériel issu du projet.
    *(ex. Rapport technique, Ouvrage construit, Logiciel opérationnel…)*

-  **Attributs ALOE :**
  Caractéristiques spécifiques et mesurables de l'objet qui peuvent être dégradées ou perturbées par une menace :
  - **Coût** (€) : impact financier potentiel.
  - **Durée** (jours, mois…) : délai nécessaire pour accomplir ou livrer l'objet.
  - **Qualité** : conformité ou respect des exigences.
  - **Date de début / fin** : calendrier précis.
  - **Avancement** (%) : état d'avancement réel par rapport au prévu.
  - **Description / spécifications** : caractéristiques ou propriétés attendues.
  - **Ressources allouées** : moyens spécifiques affectés à l'objet.
  - **Valeur ajoutée** : bénéfice attendu par rapport aux objectifs stratégiques.

---

 **Instructions détaillées pour le LLM :**
 Voici l'élément ou les éléments vulnérables et les menaces associées que vous devez analyser :
 {element_vulnerable_menace} et un extrait du document de projet : {pageContent} et  le resumé de la page actuelle  {PageSummary} et le resumé de la page précédente {lastPageSummary} ainsi que le but principal du projet : {but_principal} et le résumé global du projet a cet instant: {globalSummary}
- Lis attentivement l'**Élément vulnérable** fourni. Comprends pourquoi cet élément est fragile (complexité, dépendance, criticité…).
- Analyse la **Menace associée** : comprends comment elle pourrait concrètement exploiter la vulnérabilité identifiée.
- Déduis précisément quel **Objet ALOE** du projet serait directement impacté en cas de réalisation de la menace.
- Identifie clairement les **Attributs** précis de cet objet qui seraient altérés par cette menace.
-Pour chaque attribut retenu, complète le champ impact_attributs avec une phrase expliquant le mécanisme d’impact concret (hausse, retard, dégradation…). 
sur une meme page il peut avoir plusieurs elements vulnerable et plusieurs menaces traite les tous
> **Ne retiens jamais :**
>- Les éléments descriptifs purs (tableaux, annexes, simples illustrations).
>- Les éléments qui ne génèrent pas de risques concrets.

---

 **Format de sortie JSON (clair, structuré, exploitable) :**

```json
{{
  "element_vulnerable": "Description exacte de l’élément vulnérable",
  "menace_associee": "Description précise de la menace associée",
  "analyse_aloe": {{
    "objet_aloe": {{
      "categorie": "Objectif | Activité | Organisation | Ressource | Livrable",
      "nom": "Nom précis de l’objet impacté"
    }},
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    
    "impact_attributs": {{
      "Coût":   "Explication courte : +15 % d’imprévus liés aux reprises de chantier...",
      "Durée":  "Ajout estimé de 3 mois dû au retard des réseaux…",
      "Qualité":"Risque de non-conformité aux exigences XYZ si les travaux sont compressés."
    }},

    "justification": "Lien logique reliant l’élément vulnérable, la menace et l’objet."
  }}
}}

``` 
"""


