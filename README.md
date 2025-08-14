# Pipeline d'Analyse de Risques - CENTRALESUPELEC-LGI

## Description

Ce projet implémente un pipeline automatisé d'analyse de documents PDF pour identifier et analyser les interactions entre risques en utilisant l'intelligence artificielle générative. Le système traite des documents techniques et génère des analyses structurées sur les vulnérabilités, les éléments à risque et leurs interconnexions.

## Architecture du Projet

```
CENTRALESUPELEC-LGI/
├── src/
│   ├── Analyse/                    # Scripts de traitement
│   │   ├── Summarizer.py          # 1. Génération du contexte
│   │   ├── Element_vulnerable.py  # 2. Analyse des vulnérabilités
│   │   ├── Aloe_analysis.py       # 3. Analyse ALOE
│   │   ├── Link_analysis.py       # 4. Analyse des liens
│   │   └── file_conversion.py     # Utilitaires d'extraction
│   │
│   ├── output/                     # Résultats générés
│   │   ├── context/               # Données de contexte
│   │   │   ├── resultats_context_llm.json
│   │   │   └── resultats_context_llm.md
│   │   ├── analysis/              # Analyses principales
│   │   │   ├── element_vulnerable.md
│   │   │   ├── aloe_analyse.md
│   │   │   └── analyse_de_lien.md
│   │   ├── reference/             # Fichiers de référence
│   │   └── reports/               # Rapports finaux
│   │
│   └── prompt/
│       └── templates.py           # Templates de prompts LLM
│
├── pretraitement2/                # Documents d'entrée
│   └── DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md
│
├── .env                          # Variables d'environnement
├── requirements.txt
└── README.md
```

## Pipeline de Traitement

Le système suit un pipeline séquentiel en 4 étapes :

```
SUMMARIZER → ELEMENT_VUL → ALOE → LINK_ANALYSIS
     ↓            ↓         ↓        ↓
  context/     analysis/  analysis/ analysis/
```

### 1. Summarizer (Génération du contexte)
- **Entrée** : Document PDF traité
- **Sortie** : Contexte JSON et MD avec résumés par page
- **Fonction** : Génère le contexte global utilisé par toutes les analyses suivantes

### 2. Element_vulnerable (Analyse des vulnérabilités)
- **Entrée** : Document PDF + Contexte JSON
- **Sortie** : Analyse des éléments vulnérables par page
- **Fonction** : Identifie les vulnérabilités et éléments à risque

### 3. Aloe_analysis (Analyse ALOE)
- **Entrée** : Document PDF + Contexte JSON + Éléments vulnérables
- **Sortie** : Analyse ALOE détaillée
- **Fonction** : Analyse approfondie basée sur la méthodologie ALOE

### 4. Link_analysis (Analyse des liens)
- **Entrée** : Document PDF + Contexte JSON + Analyse ALOE
- **Sortie** : Analyse des interconnexions entre éléments
- **Fonction** : Identifie les liens et interactions entre les risques

## Installation et Configuration

### Prérequis
- Python 3.8+
- Clé API OpenRouter
- Accès à Internet pour les appels API

### Installation
```bash
# Cloner le projet
git clone [URL_DU_REPO]
cd CENTRALESUPELEC-LGI

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration
1. Créer un fichier `.env` à la racine du projet :
```env
llm_key=votre_clé_api_openrouter
```

2. Placer votre document PDF traité dans :
```
pretraitement2/DO - NOTE TECHNIQUE BAT ZZ.pdf_resultat.md
```

## Utilisation

### Exécution Individuelle des Scripts

```bash

# 1. Génération du contexte (obligatoire en premier)
python Summarizer.py

# 2. Analyse des vulnérabilités
python Element_vulnerable.py

# 3. Analyse ALOE
python Aloe_analysis.py

# 4. Analyse des liens
python Link_analysis.py
```

### Ordre d'Exécution Important
Les scripts doivent être exécutés dans l'ordre car ils dépendent des sorties des étapes précédentes :

1. **Summarizer** → Génère le contexte utilisé par tous
2. **Element_vulnerable** → Utilise le contexte, génère la base pour ALOE
3. **Aloe_analysis** → Utilise le contexte + éléments vulnérables
4. **Link_analysis** → Utilise le contexte + analyse ALOE + élément vulnerables

## Fichiers de Configuration

### templates.py
Contient les templates de prompts pour chaque type d'analyse :
- `prompt_context` : Pour la génération de contexte
- `prompt_de_base` : Pour l'analyse des vulnérabilités
- `prompt_aloe` : Pour l'analyse ALOE
- `prompt_links` : Pour l'analyse des liens

### file_conversion.py
Utilitaires d'extraction de contenu :
- `extract_pages()` : Extraction par balises XML
- `extract()` : Extraction par en-têtes markdown
- `extract_page()` : Extraction par patterns spécifiques

## Paramètres API

### Modèle utilisé
- **Modèle** : `deepseek/deepseek-r1-0528-qwen3-8b:free`
- **Température** : 0.1-0.4 selon le type d'analyse
- **Timeout** : 30-60 secondes
- **Plateforme** : OpenRouter

### Gestion d'erreurs
- Retry automatique en cas d'échec API
- Sauvegarde des erreurs dans les fichiers de sortie
- Logs détaillés pour le debugging

## Formats de Sortie

### Fichiers JSON
Structure standardisée pour les données de contexte :
```json
{
  "page": 1,
  "sectionTitle": "Titre de la section",
  "pageSummary": "Résumé de la page",
  "updatedGlobalSummary": "Contexte global mis à jour",
  "isContinuation": false
}
```


### Robustesse
- Création automatique des dossiers de sortie
- Gestion des erreurs avec continuation du traitement
- Validation des prérequis avant exécution

## Debugging et Maintenance

### Messages de Debug
Chaque script affiche :
- Progression détaillée
- Statistiques de traitement
- Informations sur les fichiers traités
- Résumé final avec métriques

### Logs d'Erreur
- Erreurs API sauvegardées
- Erreurs de format capturées
- Traceback complet pour le debugging

### Validation
- Vérification de l'existence des fichiers
- Validation du format JSON
- Contrôle de la cohérence des données

## Troubleshooting

### Problèmes Courants

**1. "Clé API non trouvée"**
- Vérifier le fichier `.env`
- S'assurer que la clé commence par `sk-`

**2. "Document non trouvé"**
- Vérifier le chemin vers `pretraitement2/`
- S'assurer que le fichier MD existe

**3. "0 pages extraites"**
- Vérifier le format du document d'entrée
- Tester différentes fonctions d'extraction

**4. "Contexte manquant"**
- Exécuter d'abord `Summarizer.py`
- Vérifier que le JSON de contexte est généré


## Contribution

### Structure de Développement
- Code modulaire avec fonctions séparées
- Gestion d'erreurs robuste
- Documentation inline
- Variables de configuration centralisées

### Standards de Code
- Noms de variables explicites
- Commentaires en français
- Gestion des exceptions
- Logs informatifs

## Licence

[À définir selon les besoins du projet]

## Contact

[Informations de contact à ajouter]

