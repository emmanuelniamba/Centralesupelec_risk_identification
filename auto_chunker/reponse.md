
---

# Page 1

```json
{
  "element_vulnerable": "Dimensionnement du bâtiment ZZ basé sur un périmètre des déchets révisé (exclusion des déchets de l’installation n°4 et des colis type A/B de l’installation n°1) pour des raisons financières, rendant le dimensionnement subjectif et potentiellement sous-estimé.",
  "menace_associee": "Évaluation sous-estimée des volumes de déchets",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts en raison des ajustements nécessaires pour agrandir le bâtiment ou construire une deuxième unité.",
      "Durée": "Retard dans la livraison du bâtiment dû aux modifications et aux travaux supplémentaires.",
      "Qualité": "Risque de non-conformité aux exigences d'entreposage des déchets contaminés si le bâtiment n'est pas dimensionné correctement."
    },
    "justification": "Le dimensionnement du bâtiment ZZ repose sur une estimation des déchets qui a exclu certains volumes pour des raisons financières. Si les volumes réels de déchets sont plus importants, le bâtiment sera insuffisant, nécessitant des ajustements coûteux, des retards et une non-conformité aux exigences."
  }
}
```

---

# Page 2

```json
{
  "element_vulnerable": "Stockage des déchets très irradiants dans les emballages type F",
  "menace_associee": "Épuisement des espaces de stockage",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Processus de gestion et d'entreposage des déchets radioactifs"
    },
    "attributs_affectes": ["Durée", "Qualité", "Coût"],
    "impact_attributs": {
      "Durée": "Retard dans la finalisation des travaux d'extension du bâtiment ZZ en raison du besoin urgent d'espaces supplémentaires, entraînant des ajustements de programme.",
      "Qualité": "Risque de non-conformité aux normes de sécurité en cas de surstockage, compromettant la qualité du traitement des déchets et des installations.",
      "Coût": "Augmentation des coûts liée aux travaux d'extension ou d'acquisition d'espaces supplémentaires, ainsi qu'aux retards dans la réalisation des objectifs projet."
    },
    "justification": "L'utilisation exclusive d'emballages type F génère un nombre important de colis (161 pour 50 ans), pouvant épuiser les espaces de stockage disponibles. Cela impacte directement le processus de gestion et d'entreposage des déchets, entraînant des retards (Durée), des risques de non-conformité (Qualité) et des dépenses supplémentaires (Coût)."
  }
}
```

---

# Page 3

```json
{
  "element_vulnerable": "Système d'exutoire des effluents actifs et douteux",
  "menace_associee": "Capacité limitée des cuves tampons et défaillance des exutoires",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable / Produit",
      "nom": "Installation ZZ (bâtiment d'entreposage des déchets)"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des dépenses liées aux interventions de maintenance et aux solutions d'urgence pour éviter les débordements.",
      "Durée": "Retard dans la livraison des installations d'exutoire et des aménagements nécessaires pour gérer les effluents.",
      "Qualité": "Non-conformité aux normes de sécurité et d'environnement si les effluents ne sont pas correctement évacués, compromettant l'acceptabilité du projet."
    },
    "justification": "La menace liée à la capacité limitée des cuves tampons et à la défaillance des exutoires expose directement le Livrable Produit (Installation ZZ) à des risques opérationnels. En cas de défaillance, le projet subira des retards (attribut Durée), des coûts supplémentaires (attribut Coût), et des problèmes de conformité (attribut Qualité)."
  }
}
```

---

# Page 4

```json
{
  "element_vulnerable": "Procédure d'analyse des effluents actifs et douteux",
  "menace_associee": "Dysfonctionnement du système d'analyse",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Analyse des effluents"
    },
    "attributs_affectes": ["Qualité", "Durée", "Coût"],
    "impact_attributs": {
      "Qualité": "Les analyses inexactes entraînent des mauvais classements des effluents, compromettant la conformité réglementaire.",
      "Durée": "Les interruptions ou ralentissements du processus d'analyse retardent le traitement des effluents, impactant le calendrier global du projet.",
      "Coût": "Les interventions correctives et les conséquences des mauvais classements augmentent les dépenses du projet."
    },
    "justification": "Un dysfonctionnement du système d'analyse compromet la fiabilité de la procédure, affectant directement la qualité des analyses, le déroulement des activités et le budget alloué."
  }
},
{
  "element_vulnerable": "Capacité d’entreposage du bâtiment ZZ",
  "menace_associee": "Saturation prématurée de la capacité d’entreposage",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable / Produit",
      "nom": "Bâtiment ZZ"
    },
    "attributs_affectes": ["Durée", "Capacité", "Qualité"],
    "impact_attributs": {
      "Durée": "La saturation prématurée oblige à repousser les échéances de livraison des autres phases du projet.",
      "Capacité": "Le nombre réel d'entreposages disponibles est inférieur à ce qui était prévu, réduisant la capacité d'accueil des déchets.",
      "Qualité": "L'entreposage dans des conditions non optimales peut compromettre la sécurité et la conformité des déchets."
    },
    "justification": "La saturation prématurée du bâtiment ZZ impacte directement son utilisation prévue, affectant son attribut de capacité et entraînant des retards dans le projet global."
  }
},
{
  "element_vulnerable": "Exutoire et traitements externes",
  "menace_associee": "Retard ou annulation des traitements conventionnés",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Organisation / Acteur",
      "nom": "Convention avec le CEA civil"
    },
    "attributs_affectes": ["Durée", "Coût", "Qualité"],
    "impact_attributs": {
      "Durée": "Les retards dans les traitements externes prolongent le temps de stockage sur site, bloquant les activités suivantes.",
      "Coût": "Les frais supplémentaires liés au stockage prolongé et éventuellement à la recherche d'alternatives augmentent le budget global.",
      "Qualité": "Le non-respect des délais ou des normes de traitement peut entraîner des non-conformités réglementaires."
    },
    "justification": "Le retard ou l'annulation des traitements conventionnés avec le CEA civil impacte directement la dépendance organisationnelle, affectant la durée, le coût et la qualité du traitement des effluents."
  }
}
```

---

# Page 5

```json
{
  "element_vulnerable": "Barrière biologique du bâtiment ZZ",
  "menace_associee": "Défaillance technique de la barrière de protection biologique",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts en raison des réparations et des arrêts d'activité nécessités par la défaillance.",
      "Durée": "Retard dans le calendrier de production (Installation n°1) en raison des interruptions et des réparations.",
      "Qualité": "Non-conformité aux normes de sécurité du personnel, compromettant l'objectif principal du projet."
    },
    "justification": "La défaillance de la barrière de protection biologique expose le personnel aux radiations, obligeant à des réparations, des retards et des coûts supplémentaires, tout en compromettant la qualité de sécurité attendue."
  }
}

{
  "element_vulnerable": "Capacité d’entreposage des déchets mixtes",
  "menace_associee": "Saturation des installations d’entreposage",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Processus",
      "nom": "Gestion des déchets et entreposage"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts en raison de l'extension des capacités d'entreposage ou de la réduction des opérations de production.",
      "Durée": "Retard dans la production (Installation n°1) en raison de la saturation des installations d'entreposage.",
      "Qualité": "Non-respect des délais de production, pouvant entraîner des écarts par rapport aux exigences qualité."
    },
    "justification": "La saturation des installations d’entreposage impacte le processus de gestion des déchets, ce qui peut entraîner des retards, des augmentations de coûts et une dégradation de la qualité du projet."
  }
}

{
  "element_vulnerable": "Dimensionnement de la tranche T2 du bâtiment ZZ",
  "menace_associee": "Sous- ou sur-dimensionnement des installations",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable",
      "nom": "Dimensionnement de la tranche T2"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Sous-dimensionné : augmentation des coûts pour agrandir les installations ; sur-dimensionné : gaspillage des ressources.",
      "Durée": "Sous-dimensionné : retard pour construire une seconde tranche ; sur-dimensionné : temps perdu à utiliser une capacité non nécessaire.",
      "Qualité": "Non-respect des objectifs de dimensionnement, pouvant entraîner des problèmes de performance ou de sécurité."
    },
    "justification": "Le sous- ou sur-dimensionnement de la tranche T2 impacte le livrable 'Dimensionnement de la tranche T2', ce qui peut entraîner des variations de coût, de durée et de qualité."
  }
}

{
  "element_vulnerable": "Précision des classifications des effluents",
  "menace_associee": "Erreurs de classification des déchets",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Processus",
      "nom": "Classification des effluents"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts liée à la correction des erreurs de classification et au traitement des déchets mal classés.",
      "Durée": "Retard dans la production en raison des interruptions pour réclasser les déchets.",
      "Qualité": "Non-conformité aux exigences de classification, compromettant la qualité du projet."
    },
    "justification": "Les erreurs de classification des déchets impactent le processus de gestion, ce qui peut entraîner des retards, des augmentations de coûts et une dégradation de la qualité."
  }
}

{
  "element_vulnerable": "Systèmes de monitoring de l’exposition",
  "menace_associee": "Détection insuffisante des expositions",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Processus",
      "nom": "Surveillance de l'exposition des travailleurs"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts en raison des investigations et des mesures correctives nécessaires.",
      "Durée": "Retard dans la production en raison des interruptions pour gérer les expositions non détectées.",
      "Qualité": "Non-respect des normes de sécurité, compromettant la qualité du projet."
    },
    "justification": "La détection insuffisante des expositions impacte le processus de surveillance, ce qui peut entraîner des retards, des augmentations de coûts et une dégradation de la qualité."
  }
}
```

---

# Page 6

```json
[
  {
    "element_vulnerable": "Présence d'équipements électriques dans le bâtiment ZZ",
    "menace_associee": "Défaillance électrique (court-circuit ou arc électrique)",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable / Produit",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectés": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Augmentation des coûts en raison des dommages matériels, des interruptions de travail et des frais de réparation suite à un incendie.",
        "Durée": "Retard dans la livraison du bâtiment dû à l'arrêt des travaux et aux investigations nécessaires.",
        "Qualité": "Risque de non-conformité aux normes de sécurité et de qualité si l'incendie endommage les structures ou les équipements."
      },
      "justification": "Une défaillance électrique dans les équipements du bâtiment ZZ peut provoquer un incendie, impactant directement le livrable (le bâtiment) en augmentant les coûts, en prolongeant sa durée de construction et en compromettant sa qualité."
    }
  },
  {
    "element_vulnerable": "Stockage des colis contenant des carburants",
    "menace_associee": "Fuite ou mauvais entreposage des colis",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Activité / Processus",
        "nom": "Processus d'entreposage des déchets"
      },
      "attributs_affectés": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Augmentation des coûts liée aux dommages matériels, aux mesures de sécurité renforcées et aux indemnisations éventuelles.",
        "Durée": "Retard dans le calendrier d'entreposage des déchets, affectant la planification globale du projet.",
        "Qualité": "Risque de non-conformité aux normes de sécurité si une fuite compromet l'étanchéité ou la stabilité des colis."
      },
      "justification": "Une mauvaise gestion du stockage des colis contenant des carburants peut entraîner une fuite ou une explosion, impactant le processus d'entreposage des déchets en augmentant les coûts, en prolongeant sa durée et en compromettant sa qualité de sécurité."
    }
  }
]
```

---

# Page 7

```json
{
  "element_vulnerable": "Batteries des moyens de manutention",
  "menace_associee": "Explosion par accumulation d’hydrogène gazeux",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Processus de manutention sécurisée des déchets"
    },
    "attributs_affectes": ["Durée", "Coût", "Qualité"],
    "impact_attributs": {
      "Durée": "Retard dans la mise en service des installations de manutention et du bâtiment d'entreposage, nécessitant des ajustements dans le calendrier projet.",
      "Coût": "Augmentation des coûts liés aux interventions de sécurité, aux arrêts non programmés, et aux réparations post-explosion.",
      "Qualité": "Risque de non-conformité aux normes de sûreté et aux exigences réglementaires pour l'installation d'entreposage."
    },
    "justification": "L'explosion due à l'accumulation d'hydrogène des batteries impacte directement le processus de manutention sécurisée des déchets, entraînant des retards dans la réalisation des activités, des coûts supplémentaires pour les mesures correctives, et une possible dégradation de la qualité des installations."
  }
}

{
  "element_vulnerable": "Colis stockés",
  "menace_associee": "Chute des colis pendant l'entretien ou le stockage",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable / Produit",
      "nom": "Stock de déchets conditionnés"
    },
    "attributs_affectes": ["Qualité", "Durée"],
    "impact_attributs": {
      "Qualité": "Dommages aux colis, potentiellement compromettant la conformité des déchets aux normes de transport et d'entreposage.",
      "Durée": "Temps supplémentaire nécessaire pour inspecter, réparer ou remplacer les colis endommagés, impactant le rythme d'approvisionnement."
    },
    "justification": "La chute des colis affecte directement le stock de déchets conditionnés, pouvant entraîner des dégradations des produits et un délai dans le traitement ou l'expédition."
  }
}

{
  "element_vulnerable": "Ponts roulants",
  "menace_associee": "Défaillance mécanique due à une mauvaise maintenance ou des conditions d'utilisation agressives",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Ressource",
      "nom": "Équipement de manutention (ponts roulants)"
    },
    "attributs_affectes": ["Durée", "Coût"],
    "impact_attributs": {
      "Durée": "Arrêts prolongés des opérations de manutention, retardant le traitement et l'entreposage des déchets.",
      "Coût": "Frais supplémentaires pour la réparation ou le remplacement des ponts roulants, ainsi que pour les heures d'inactivité."
    },
    "justification": "La défaillance des ponts roulants, une ressource critique pour le déchargement et le stockage, perturbe les opérations et génère des retards et des coûts supplémentaires."
  }
}

{
  "element_vulnerable": "Systèmes électriques et matériels électroniques",
  "menace_associee": "Cortocircuit en cas d’inondation interne",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Sûreté électrique et contrôle des équipements critiques"
    },
    "attributs_affectes": ["Qualité", "Durée"],
    "impact_attributs": {
      "Qualité": "Défaillance des systèmes de contrôle et de sécurité, compromettant la conformité aux normes de sûreté du site d'entreposage.",
      "Durée": "Temps consacré aux diagnostics et réparations des équipements électriques, retardant les opérations et les inspections nécessaires."
    },
    "justification": "Un cortocircuit lié à une inondation affecte le processus de contrôle et de maintenance électrique, impactant la qualité de la sûreté et la durée des opérations."
  }
}
```

---

# Page 8

```json
{
  "element_vulnerable": "Infrastructure dimensionnée pour conditions climatiques extrêmes (dimensionnée pour résister à une tornade EF2 et aux projectiles induits)",
  "menace_associee": "Vent fort dépassant les caractéristiques spécifiées ou chute d'avion (avec impact direct sur les éléments structurels)",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable / Produit",
      "nom": "Bâtiment ZZ"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts estimée à 15-20% en raison des dépannages et des réparations urgentes nécessaires pour restaurer les éléments structurels endommagés (fenêtres, couvertures, systèmes d'ingénierie).",
      "Durée": "Retard d'environ 2-4 mois dans la livraison finale du bâtiment, dû aux interruptions des travaux et aux temps d'attente pour les interventions techniques et les réparations.",
      "Qualité": "Risque de non-conformité aux normes initiales (Eurocode, CEA) si les dommages causent des dégradations structurelles ou fonctionnelles non prévues, compromettant l'intégrité du produit final."
    },
    "justification": "L'infrastructure du bâtiment ZZ (élément vulnérable) est conçue pour résister à des vents forts (tornade EF2) et aux projectiles, mais une menace dépassant ces paramètres (vents violents ou chute d'avion) peut causer des dommages concrets au livrable 'Bâtiment ZZ'. Ces dommages affectent directement le coût (réparations), la durée (retard des travaux) et la qualité (non-conformité aux normes initiales)."
  }
}
```

---

# Page 9

```json
[
  {
    "element_vulnerable": "Systèmes d'alerte et de gestion des urgences",
    "menace_associee": "Mesures de protection contre les catastrophes naturelles pourraient être insuffisantes",
    "analyse_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Processus de gestion des urgences",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "La défaillance des systèmes d'alerte nécessiterait des interventions de maintenance urgentes et des réparations coûteuses, augmentant les dépenses imprévues.",
        "Durée": "Les retards dans la gestion des urgences pourraient entraîner des arrêts prolongés du chantier, impactant directement la durée prévue du projet.",
        "Qualité": "Une gestion inadéquate des urgences compromettrait la conformité aux normes de sécurité et la qualité des opérations, pouvant entraîner des sanctions ou des révisions ultérieures."
      },
      "justification": "Le système d'alerte est un composant critique du processus de gestion des urgences. Une insuffisance des mesures de protection contre les catastrophes naturelles compromet directement ce processus, affectant sa qualité, sa durée et son coût."
    }
  },
  {
    "element_vulnerable": "Infrastructure de manutention des déchets",
    "menace_associee": "Défaillance des systèmes d’utilités critiques (alimentation électrique, ventilation)",
    "analyse_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Processus de manutention des déchets",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Les interruptions des services d’utilités nécessiteraient des réparations et des ajustements de planning, augmentant les coûts globaux du projet.",
        "Durée": "Les arrêts dus à des défaillances des systèmes d’utilités provoqueraient des retards dans le processus de manutention des déchets, impactant la durée totale du projet.",
        "Qualité": "Une mauvaise gestion des déchets en raison de défaillances techniques compromettrait la conformité aux normes environnementales et de sécurité."
      },
      "justification": "Le processus de manutention des déchets dépend directement des systèmes d’utilités critiques. Une défaillance de ces systèmes impacte immédiatement la qualité, la durée et le coût de ce processus essentiel."
    }
  }
]
```

---

# Page 10

```json
{
  "analyses": [
    {
      "element_vulnerable": "Réservoir de fioul de l’installation GEF",
      "menace_associee": "Explosion due à une mauvaise ventilation ou dégazage de la cuve",
      "analyse_aloe": {
        "objet_aloe": {
          "categorie": "Ressource",
          "nom": "Réservoir de fioul de l’installation GEF"
        },
        "attributs_affectes": ["Coût", "Durée", "Qualité"],
        "impact_attributs": {
          "Coût": "Augmentation des coûts liés aux réparations ou remplacements suite à une explosion, potentiellement des dommages à d'autres installations.",
          "Durée": "Retard dans le remplissage du réservoir et le transport d’hydrocarbure, impactant le calendrier des opérations.",
          "Qualité": "Dégradation physique du réservoir, compromettant sa conformité aux normes de sécurité et son bon fonctionnement."
        },
        "justification": "L’explosion due à une mauvaise ventilation ou dégazage du réservoir, bien que partiellement exclue par la RFS I.2.d., reste un risque potentiel. Cette menace exploite la vulnérabilité structurelle du réservoir, impactant directement sa disponibilité (Durée), sa sécurité (Qualité) et nécessitant des interventions financières (Coût)."
      }
    },
    {
      "element_vulnerable": "Colis des déchets contaminés",
      "menace_associee": "Explosion externe liée à un accident de transport d’hydrocarbure voisin",
      "analyse_aloe": {
        "objet_aloe": {
          "categorie": "Livrable",
          "nom": "Colis de déchets contaminés"
        },
        "attributs_affectes": ["Qualité", "Durée", "Coût"],
        "impact_attributs": {
          "Qualité": "Désintégration des colis sous l’effet d’une onde de surpression, compromettant la sécurité et la conformité des déchets.",
          "Durée": "Retard dans le traitement et l’entreposage des déchets endommagés, impactant le planning global du projet.",
          "Coût": "Frais supplémentaires pour le nettoyage, le traitement et la gestion des déchets endommagés, ainsi que des interventions d’urgence."
        },
        "justification": "L’explosion externe générée par un accident de transport d’hydrocarbure à proximité du bâtiment ZZ expose les colis à une onde de surpression (50 mbar). Cette menace exploite leur vulnérabilité résiduelle malgré les normes de conception, affectant directement leur état (Qualité), leur temps de traitement (Durée) et engendrant des dépenses (Coût)."
      }
    }
  ]
}
```

---

# Page 11

```json
[
  {
    "element_vulnerable": "Infrastructure de manutention (ponts)",
    "menace_associee": "Accident de manutention (déraillement, surcharge ou panne d’équipement)",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Activité",
        "nom": "Manutention des colis radioactifs"
      },
      "attributs_affectes": ["Durée", "Qualité", "Coût"],
      "impact_attributs": {
        "Durée": "Retard dans l’acheminement des colis et des contrôles de conformité dus à l’arrêt des opérations de manutention.",
        "Qualité": "Risque de mauvaise caractérisation des colis si les inspections sont interrompues, compromettant leur stockage sécurisé.",
        "Coût": "Surcoût dû aux réparations des ponts, aux dommages matériels et aux indemnisations en cas d’accident."
      },
      "justification": "L’infrastructure de manutention est fragile en raison de la complexité logistique et de l’utilisation de ponts pour manipuler des conteneurs radioactifs. Un accident peut directement impacter l’activité de manutention, entraînant des retards, une dégradation de la qualité des opérations et des coûts supplémentaires."
    }
  },
  {
    "element_vulnerable": "Infrastructures techniques (ventilation nucléaire)",
    "menace_associee": "Panne ou non-conformité du système de ventilation",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectes": ["Qualité", "Durée", "Coût"],
      "impact_attributs": {
        "Qualité": "Non-respect des normes de confinement nucléaire, compromettant la sécurité des déchets stockés et la conformité aux exigences réglementaires.",
        "Durée": "Retard dans les inspections et réparations nécessaires pour restaurer la conformité, impactant le calendrier d’achèvement du projet.",
        "Coût": "Frais supplémentaires pour les contrôles, les réparations et les retards d’exécution, incluant les pénalités pour non-conformité."
      },
      "justification": "La ventilation nucléaire est critique pour le confinement des polluants. Sa panne peut affecter directement le livrable 'Bâtiment ZZ', en dégradant sa qualité, prolongeant sa durée de réalisation et augmentant son coût."
    }
  },
  {
    "element_vulnerable": "Stockage des colis (contenant d’activité)",
    "menace_associee": "Fuite ou manipulation inappropriée des colis",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Activité",
        "nom": "Stockage et caractérisation des colis"
      },
      "attributs_affectes": ["Qualité", "Durée", "Coût"],
      "impact_attributs": {
        "Qualité": "Contamination des espaces ou des colis adjacents, entraînant des non-conformités aux normes de sécurité et de gestion des déchets.",
        "Durée": "Arrêts d’activité pour décontamination, investigations et réorganisation des processus, retardant l’acheminement des colis.",
        "Coût": "Dépenses supplémentaires pour la décontamination, les analyses de contrôle et les retards d’exécution des opérations."
      },
      "justification": "Le stockage des colis est vulnérable en raison de la sensibilité des déchets radioactifs. Une fuite ou mauvaise manipulation impacte directement l’activité de stockage, affectant sa qualité, sa durée et son coût en raison des mesures de sécurité nécessaires."
    }
  }
]
```

---

# Page 12

```json
{
  "element_vulnerable": "Système de ventilation pour l'extension du bâtiment ZZ",
  "menace_associee": "Incapacité à répondre aux exigences de sécurité dans un scénario d'accident",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Processus de ventilation et de gestion des classes d'air"
    },
    "attributs_affectes": ["Qualité", "Durée"],
    "impact_attributs": {
      "Qualité": "Risque de non-conformité aux normes de sécurité en cas de conception inadaptée, pouvant entraîner des conséquences graves lors d'un accident.",
      "Durée": "Retard dans la mise en service du système si des modifications ou réparations sont nécessaires pour corriger les défauts de conception."
    },
    "justification": "Le système de ventilation est complexe en raison de sa capacité à gérer plusieurs classes d'air (C2 et C3). Une conception inadéquate pourrait compromettre sa réactivité en cas d'accident, impactant la qualité du processus et pouvant entraîner des retards dans la mise en service du bâtiment."
  }
},
{
  "element_vulnerable": "Travaux de construction de l'extension du bâtiment ZZ",
  "menace_associee": "Retard ou augmentation des coûts en raison d'une externalisation non optimisée",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Activité de construction de l'extension du bâtiment ZZ"
    },
    "attributs_affectes": ["Coût", "Durée"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts en raison de retards, d'une main-d'œuvre sous-allocation ou de prix d'emballage dus à une externalisation non optimisée.",
      "Durée": "Prolongation des délais de réalisation du chantier en raison de contraintes logistiques ou de ressources insuffisantes."
    },
    "justification": "Les travaux de construction sont sensibles aux fluctuations économiques et à la surcharge d'accès au site. Une externalisation non optimisée expose à des retards et des augmentations de coût liés à des difficultés d'approvisionnement ou à une gestion inefficace des ressources."
  }
},
{
  "element_vulnerable": "Estimation financière avec incertitudes techniques",
  "menace_associee": "Sous-estimation des coûts due à des impondérables techniques non anticipés",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Ressource",
      "nom": "Budget alloué à l'extension du bâtiment ZZ"
    },
    "attributs_affectes": ["Coût"],
    "impact_attributs": {
      "Coût": "Surcoût dépassant la borne haute estimée (341 M€) en raison de provisions techniques non suffisantes pour absorber les imprévus techniques."
    },
    "justification": "L'incertitude de 50% dans l'estimation initiale rend le budget vulnérable aux variations imprévues. Une sous-estimation des coûts techniques peut entraîner des dépenses supplémentaires non couvertes, compromettant la viabilité financière du projet."
  }
}
```

---

# Page 13

```json
[
  {
    "element_vulnerable": "Système de ventilation nucléaire",
    "menace_associee": "Défaillance technique",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable / Produit",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "La défaillance nécessite des réparations coûteuses et peut entraîner des dommages supplémentaires, augmentant le budget global estimé à 227 M€ HT.",
        "Durée": "Les travaux d'installation ou de réparation du système de ventilation retardent la mise en service du bâtiment, pouvant pousser la fin du projet de 2025 à 2027.",
        "Qualité": "Le manque de ventilation appropriée compromet la conformité des déchets entreposés aux normes de sécurité, réduisant la qualité du livrable final."
      },
      "justification": "La défaillance du système de ventilation nucléaire impacte directement la capacité à entreposer les fûts type D et colis type C, des composantes clés du projet. L'objet impacté est le Livrable 'Bâtiment ZZ' car sans ventilation adéquate, le bâtiment ne peut atteindre son objectif de sécurité et de conformité."
    }
  },
  {
    "element_vulnerable": "Installation de confinement C2",
    "menace_associee": "Inondation ou endommagement structurel",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable / Produit",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectes": ["Durée", "Qualité", "Coût"],
      "impact_attributs": {
        "Durée": "L'endommagement nécessite des réparations ou des travaux de remise en état, entraînant un retard dans la livraison du bâtiment (objectif initial 2025).",
        "Qualité": "Le local de confinement C2 ne répond plus aux normes de sécurité, ce qui réduit la qualité du livrable et expose à des risques radiologiques.",
        "Coût": "Les réparations et les dommages supplémentaires augmentent le coût global du projet, pouvant dépasser les 227 M€ HT."
      },
      "justification": "L'endommagement de l'installation de confinement C2 compromet la sécurité du confinement radiologique, impactant directement le Livrable 'Bâtiment ZZ' qui doit garantir l'intégrité des déchets colis A et B."
    }
  },
  {
    "element_vulnerable": "Intégrité fonctionnelle du local BàG",
    "menace_associee": "Rupture ou panne des systèmes de confinement",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable / Produit",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectes": ["Durée", "Qualité", "Coût"],
      "impact_attributs": {
        "Durée": "Les réparations ou les arrêts d'activité dans le local BàG retardent l'entreposage des colis A et B, impactant la durée globale du projet.",
        "Qualité": "Le manque de confinement dans le local BàG expose à des risques, ce qui réduit la qualité du livrable et compromet l'objectif de sécurité.",
        "Coût": "Les réparations et les mesures de sécurité supplémentaires augmentent le coût du projet, avec une estimation de 15 % d'indétermination technique déjà prévue."
      },
      "justification": "La rupture des systèmes de confinement dans le local BàG compromet la sécurité du projet, impactant le Livrable 'Bâtiment ZZ' qui doit garantir un entreposage sécurisé des colis A et B."
    }
  }
]
```

---

# Page 14

```json
[
  {
    "element_vulnerable": "Fûts type D",
    "menace_associee": "Surcharger de déchets",
    "analyse_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Une augmentation de la production de déchets nécessite des ajustements structurels ou des extensions du bâtiment, entraînant des dépenses supplémentaires estimées à +15% du budget initial.",
        "Durée": "La surcharge de déchets peut provoquer des retards dans l'installation et le traitement des déchets, pouvant compresser le calendrier global du projet de 2 à 4 mois.",
        "Qualité": "Un surdimensionnement ou une mauvaise gestion du stockage peut compromettre la conformité aux normes de sécurité, risquant des non-conformités et des retours qualité."
      },
      "justification": "La surcharge de déchets dans les fûts type D, qui constituent la plus grande partie des déchets à entreposer, met directement en cause la capacité d'accueil du bâtiment ZZ, impactant son coût, sa durée et sa qualité."
    }
  },
  {
    "element_vulnerable": "Colis type C",
    "menace_associee": "Épuisement de la capacité de stockage",
    "analyse_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Un épuisement prématuré des capacités d'entreposage nécessite des rehaussements de capacité non prévus, augmentant le coût total du projet de 10-20%.",
        "Durée": "L'épuisement des places pour colis type C oblige à bloquer les ressources ou à annuler des opérations, pouvant retarder le projet de 1 à 3 mois.",
        "Qualité": "Un manque de conteneurs peut entraîner des non-conformités dans le traitement des déchets, affectant la qualité globale du projet."
      },
      "justification": "L'épuisement des 176 places prévues pour les colis type C expose directement la capacité d'accueil du bâtiment ZZ, impactant son efficacité et sa qualité."
    }
  },
  {
    "element_vulnerable": "Caisson 5m³ (installation n°3)",
    "menace_associee": "Saturation prématurée",
    "analyse_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Une saturation prématurée des caissons 5m³ (6 unités) nécessite des rehaussements de capacité, augmentant le budget de 5-15%.",
        "Durée": "Des retards dans la gestion des déchets pour l'installation n°3 peuvent compresser le calendrier global, prolongeant la durée par 1 à 2 mois.",
        "Qualité": "Une mauvaise gestion des caissons peut entraîner des non-conformités, affectant la qualité du traitement des déchets."
      },
      "justification": "La saturation des caissons 5m³ liée à l'installation n°3 met directement en cause la capacité d'accueil du bâtiment ZZ, impactant son efficacité et sa qualité."
    }
  },
  {
    "element_vulnerable": "Colis type A et B",
    "menace_associee": "Non-respect des standards de stockage",
    "analyse_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ",
      "attributs_affectes": ["Qualité", "Coût"],
      "impact_attributs": {
        "Qualité": "Un non-respect des standards BàG spécifiques pour les colis A/B peut entraîner des non-conformités, baissant la qualité du stockage et du traitement.",
        "Coût": "Des amendes pour non-conformité ou des corrections nécessaires peuvent augmenter le budget de 5-10%."
      },
      "justification": "Le non-respect des standards de stockage pour les colis A/B expose le projet à des risques de non-conformité, impactant directement la qualité et le coût."
    }
  },
  {
    "element_vulnerable": "Effluents actifs (auto-générés)",
    "menace_associee": "Capacité de stockage insuffisante",
    "analyse_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Une utilisation compressée du local de 70m² peut nécessiter des extensions, augmentant le coût de 8-12%.",
        "Durée": "Des retards dans le traitement des effluents actifs peuvent prolonger la durée du projet de 1 à 3 mois.",
        "Qualité": "Une mauvaise gestion des effluents compromet la qualité du traitement, risquant des non-conformités."
      },
      "justification": "L'estimation inexacte des effluents actifs expose la capacité d'accueil du local de 70m² du bâtiment ZZ, impactant son efficacité et sa qualité."
    }
  },
  {
    "element_vulnerable": "Effluents douteux (auto-générés)",
    "menace_associee": "Compromission de la sécurité ou de la conformité",
    "analyse_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment ZZ",
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Des opérations d'urgence ou des amendes pour non-conformité peuvent augmenter le budget de 10-20%.",
        "Durée": "Des retards pour gérer les incidents de sécurité ou de conformité peuvent prolonger le projet de 2 à 5 mois.",
        "Qualité": "Une compromission de la sécurité ou de la conformité réduit la qualité du traitement des déchets."
      },
      "justification": "La gestion inadéquate des effluents douteux expose le projet à des risques de sécurité et de non-conformité, impactant directement la qualité, la durée et le coût du bâtiment ZZ."
    }
  }
]
```

---

# Page 15

```json
{
  "element_vulnerable": "Unité de ventilation du bâtiment 438",
  "menace_associee": "Défaillance du système de ventilation (pompe, filtre, moteur)",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Objectif",
      "nom": "Confinement des déchets contaminés"
    },
    "attributs_affectes": ["Qualité", "Durée"],
    "impact_attributs": {
      "Qualité": "La défaillance du système de ventilation compromet le confinement des déchets A/B, entraînant un risque de contamination et une non-conformité aux normes de sécurité.",
      "Durée": "Les retards pour effectuer les réparations et les vérifications nécessaires impactent le calendrier du projet, pouvant entraîner des délais supplémentaires."
    },
    "justification": "L'unité de ventilation est cruciale pour le confinement des déchets contaminés. Une défaillance expose directement le projet à des risques de non-conformité (Qualité) et génère des interruptions dans le programme (Durée)."
  }
},
{
  "element_vulnerable": "Système de Chauffage/ ventilation (HVAC) du local de caractérisation",
  "menace_associee": "Non-respect de l'hermétisme du local due à une ventilation insuffisante",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité",
      "nom": "Caractérisation des colis type C"
    },
    "attributs_affectes": ["Qualité", "Coût"],
    "impact_attributs": {
      "Qualité": "Une ventilation insuffisante compromet la fiabilité des mesures de caractérisation, rendant les résultats non conformes aux exigences techniques.",
      "Coût": "Les réparations ou ajustements nécessaires pour corriger l'insuffisance ventilatoire génèrent des dépenses imprévues pouvant allonger le budget alloué."
    },
    "justification": "Le système HVAC est essentiel pour maintenir un environnement contrôlé dans le local de caractérisation. Sa mauvaise performance affecte directement la qualité des analyses et peut engendrer des coûts supplémentaires pour remédier au problème."
  }
}
```

---

# Page 16

```json
[
  {
    "element_vulnerable": "Incertitude technique dans le dimensionnement des servitudes",
    "menace_associee": "Défaillance technique dans l’implantation des espaces nécessaires",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Activité",
        "nom": "Extension du bâtiment 438"
      },
      "attributs_affectes": ["Coût", "Durée", "Qualité"],
      "impact_attributs": {
        "Coût": "Augmentation des coûts en raison des ajustements ultérieurs nécessaires pour corriger le dimensionnement initial des servitudes.",
        "Durée": "Retard dans la réalisation des travaux d'extension due à des modifications non prévues du maillage initial.",
        "Qualité": "Risque de non-conformité aux normes de construction si les espaces ne sont pas correctement dimensionnés depuis le départ."
      },
      "justification": "L'incertitude technique dans le dimensionnement des servitudes expose le projet à une défaillance technique lors de l'implantation des espaces nécessaires, impactant directement l'activité d'extension du bâtiment 438."
    }
  },
  {
    "element_vulnerable": "Complexité logistique liée aux interactions entre bâtiments",
    "menace_associee": "Retard ou perturbation liée à la coactivité",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Activité",
        "nom": "Exploitation du bâtiment ZZ et extension du bâtiment 438"
      },
      "attributs_affectes": ["Durée", "Qualité", "Coût"],
      "impact_attributs": {
        "Durée": "Retard dans la mise en service de l'extension due à des conflits logistiques entre le bâtiment en exploitation et le chantier.",
        "Qualité": "Baisse de la qualité opérationnelle résultant de perturbations récurrentes dans l'accès et l'occupation spatiale.",
        "Coût": "Augmentation des coûts liée aux heures supplémentaires et aux ajustements nécessaires pour résoudre les conflits logistiques."
      },
      "justification": "La complexité logistique entre le bâtiment ZZ en exploitation et l'extension du bâtiment 438 expose le projet à des retards et perturbations, impactant l'activité d'exploitation et d'extension."
    }
  },
  {
    "element_vulnerable": "Incertitude financière dans le chiffrage des extensions",
    "menace_associee": "Inflation ou sous-estimation des coûts réels",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Ressource",
        "nom": "Budget d'exécution du projet"
      },
      "attributs_affectes": ["Coût", "Durée"],
      "impact_attributs": {
        "Coût": "Sous-estimation des coûts réels pouvant entraîner un décalage significatif entre le budget alloué et les dépenses réelles.",
        "Durée": "Retard dans le calendrier du projet en raison de difficultés financières pour engager les prestataires nécessaires."
      },
      "justification": "L'incertitude financière dans le chiffrage expose le projet à une sous-estimation des coûts, impactant directement la ressource financière et potentiellement la durée du projet."
    }
  }
]
```

---

# Page 17

```json
{
  "element_vulnerable": "Les conteneurs J équipés de recombineurs",
  "menace_associee": "Défaillance du catalyseur au palladium",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable / Produit",
      "nom": "Conteneur J avec recombineur"
    },
    "attributs_affectes": ["Qualité", "Durée", "Coût"],
    "impact_attributs": {
      "Qualité": "La défaillance du catalyseur compromet la capacité du conteneur à recombiner les gaz, entraînant un risque de contamination et une non-conformité aux normes de sécurité.",
      "Durée": "La nécessité de réparer ou de remplacer le conteneur provoque des retards dans le calendrier de livraison des colis A/B.",
      "Coût": "Des coûts supplémentaires sont engendrés pour la réparation ou l'achat d'un conteneur neuf, impactant le budget global du projet."
    },
    "justification": "La défaillance du catalyseur dans le conteneur J expose directement le projet à des risques de sécurité et de non-conformité, perturbant la qualité du livrable, retardant les échéances et augmentant les coûts."
  }
},
{
  "element_vulnerable": "L’interopérabilité entre fûts type D et conteneurs J",
  "menace_associee": "Incompatibilité dimensionnelle ou structurelle",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Processus d'installation et de stockage des conteneurs J"
    },
    "attributs_affectes": ["Qualité", "Durée", "Coût"],
    "impact_attributs": {
      "Qualité": "Des incompatibilités structurelles peuvent entraîner des fuites ou des dommages, compromettant la sécurité et la conformité du stockage.",
      "Durée": "Les retards pour corriger les incompatibilités impactent le calendrier de mise en service des colis A/B.",
      "Coût": "Des ajustements ou des réparations supplémentaires augmentent les dépenses liées au processus d'installation."
    },
    "justification": "L'incompatibilité entre les fûts D et les conteneurs J affecte directement le processus de stockage, compromettant sa qualité, prolongeant les délais et augmentant les coûts."
  }
},
{
  "element_vulnerable": "Le calendrier de mise en service et d’extension parasismique",
  "menace_associee": "Retard dans l’extension parasismique",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Objectif",
      "nom": "Objectif de mise en service finale des colis B"
    },
    "attributs_affectes": ["Durée", "Coût", "Qualité"],
    "impact_attributs": {
      "Durée": "Un retard dans l’extension parasismique entraîne un report des échéances de stockage des colis B, impactant le calendrier global du projet.",
      "Coût": "Des dépenses supplémentaires sont nécessaires pour compenser le retard, allongeant le budget alloué.",
      "Qualité": "Un retard prolongé pourrait compromettre la conformité des colis B aux exigences réglementaires et techniques."
    },
    "justification": "Le retard dans l’extension parasismique perturbe directement l’objectif de mise en service des colis B, affectant sa qualité, son calendrier et son coût."
  }
},
{
  "element_vulnerable": "La phase de transit dans le bâtiment 438",
  "menace_associee": "Inadaptation du bâtiment 438 pour le stockage temporaire",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable / Produit",
      "nom": "Bâtiment 438"
    },
    "attributs_affectes": ["Qualité", "Durée", "Coût"],
    "impact_attributs": {
      "Qualité": "Un bâtiment 438 non adapté pourrait endommager les colis A/B, compromettant leur intégrité et leur conformité.",
      "Durée": "Des retards sont générés pour trouver une solution alternative au stockage, impactant le calendrier global.",
      "Coût": "Des investissements supplémentaires sont nécessaires pour adapter ou remplacer le bâtiment 438, augmentant les dépenses."
    },
    "justification": "L’inadaptation du bâtiment 438 pour le transit des colis A/B affecte directement son rôle de livrable, compromettant sa qualité, prolongeant les délais et augmentant les coûts."
  }
}
```

---

# Page 18

```json
[
  {
    "element_vulnerable": "Travaux préparatoires",
    "menace_associee": "Retard dans l’aménagement des servitudes",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Objectif",
        "nom": "Mise en service à fin 2036"
      },
      "attributs_affectes": ["Durée", "Coût"],
      "impact_attributs": {
        "Durée": "Retard dans l’aménagement des servitudes entraînerait un report de la phase de réalisation, pouvant prolonger la durée totale du projet au-delà de 2036.",
        "Coût": "Un retard nécessiterait des travaux supplémentaires et des ajustements financiers, augmentant le budget global du projet de plusieurs millions d'euros."
      },
      "justification": "Le retard dans l’aménagement des servitudes (menace) impacte directement l’objectif de mise en service à fin 2036 (Objet ALOE) en perturbant le calendrier et le budget prévisionnel."
    }
  },
  {
    "element_vulnerable": "Chantier",
    "menace_associee": "Variabilité des délais et des coûts",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Activité",
        "nom": "Phase de réalisation du bâtiment ZZ"
      },
      "attributs_affectes": ["Durée", "Coût"],
      "impact_attributs": {
        "Durée": "La variabilité des délais prolongerait la phase de réalisation, reportant la mise en service à plus tard que prévu et compromettant le planning initial.",
        "Coût": "Des ajustements imprévus et des retards dus à des incohérences avec d’autres installations augmenteraient les dépenses totales, incluant les coûts d’immobilisation et les surcouts de main-d’œuvre."
      },
      "justification": "La variabilité des délais et des coûts (menace) affecte directement l’activité de réalisation du chantier (Objet ALOE), perturbant son avancement et son budget prévisionnel."
    }
  },
  {
    "element_vulnerable": "Schéma MOE interne",
    "menace_associee": "Optimisation insuffisante des ressources",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Objectif",
        "nom": "Mise en service à fin 2036"
      },
      "attributs_affectes": ["Durée", "Coût"],
      "impact_attributs": {
        "Durée": "Une optimisation insuffisante des ressources prolongerait la conception-réalisation, retardant la mise en service et compromettant le calendrier global.",
        "Coût": "Des engagements financiers imprévus liés à l’externalisation ou à des ajustements de ressources augmenteraient le budget total du projet."
      },
      "justification": "L’optimisation insuffisante des ressources (menace) impacte l’objectif de mise en service (Objet ALOE) en rendant les prévisions de durée et de coût moins fiables."
    }
  }
]
```

---

# Page 19

```json
{
  "element_vulnerable": "Sensibilité des coûts prévisionnels : Les estimations financières du Bâtiment 461 varient considérablement selon les itérations (de 341 M€ à 85 M€), indiquant une forte réactivité aux décisions de conception et une absence de points d'ancrage solides pour la réelle charge financière.",
  "menace_associee": "Évaluation non exhaustive des facteurs d’incertitude dans les itérations : L’absence d’une analyse complète des scénarios de référence et des configurations (fichier annexé) permet aux erreurs d’inclusion/omission de postes de s’installer, conduisant à une dérive des coûts sans contrôle.",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité / Processus",
      "nom": "Évaluation des coûts et des risques"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Une estimation non exhaustive des facteurs d’incertitude entraîne une sous-estimation ou une surestimation des coûts réels, pouvant générer des débordements budgétaires importants.",
      "Durée": "Des coûts imprévus obligent à revoir le calendrier du projet, provoquant des retards dans les phases de réalisation et d’achèvement des livrables.",
      "Qualité": "Des ajustements financiers constants pour corriger les erreurs initiales peuvent compromettre la qualité des livrables et la conformité aux spécifications initiales."
    },
    "justification": "La sensibilité des coûts prévisionnels expose une vulnérabilité dans le processus d’évaluation des risques et coûts. Si la menace d’évaluation non exhaustive est concrètement exploitée, elle impacte directement l’activité d’évaluation des risques, altérant ainsi ses attributs de coût, de durée et de qualité."
  }
}
```

---

# Page 20

```json
{
  "element_vulnerable": "Capacité de stockage au-delà de 15 ans pour les colis type B",
  "menace_associee": "Négligence dans l’évaluation des contraintes post-transition",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable",
      "nom": "Bâtiment de stockage pour colis type B au-delà de 15 ans"
    },
    "attributs_affectes": ["Coût", "Durée", "Qualité"],
    "impact_attributs": {
      "Coût": "Augmentation des coûts estimée à 10-20 % supplémentaires pour les adaptations postérieures liées à la négligence des contraintes post-transition.",
      "Durée": "Retard dans la planification de l'extension pouvant entraîner un report de plusieurs mois dans le calendrier global du projet.",
      "Qualité": "Non-conformité aux exigences de sécurité réglementaires si les contraintes post-transition ne sont pas correctement évaluées et documentées."
    },
    "justification": "La négligence dans l’évaluation des contraintes post-transition compromet directement la qualité et la faisabilité du projet d'extension, entraînant des coûts et délais supplémentaires."
  }
}
```

```json
{
  "element_vulnerable": "Structure en charpente métallique face aux agressions externes et internes",
  "menace_associee": "Sismicité ou phénomènes atmosphériques hors norme",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Livrable",
      "nom": "Structure en charpente métallique du bâtiment de stockage"
    },
    "attributs_affectes": ["Durée", "Coût", "Qualité"],
    "impact_attributs": {
      "Durée": "Arrêt total du stockage pouvant entraîner un report de plusieurs mois à un an du calendrier de livraison.",
      "Coût": "Coûts de réparations estimés à plusieurs dizaines de millions d’euros, voire annulation partielle ou totale du projet.",
      "Qualité": "Non-respect des exigences de sûreté, risque d’accident majeur et de non-conformité réglementaire."
    },
    "justification": "Un événement dépassant les normes de conception expose la structure à une défaillance critique, impactant directement la qualité, la durée et le coût du projet."
  }
}
```

```json
{
  "element_vulnerable": "Fiabilité des analyses de sûreté pour les différents scénarios d'agressions",
  "menace_associee": "Erreur dans les hypothèses de calcul ou modélisation",
  "analyse_aloe": {
    "objet_aloe": {
      "categorie": "Activité",
      "nom": "Analyses de sûreté pour les différents scénarios d'agressions"
    },
    "attributs_affectes": ["Qualité", "Coût", "Durée"],
    "impact_attributs": {
      "Qualité": "Risque de sous-estimation des risques, conduisant à une conception insuffisante de la structure ou du système de stockage.",
      "Coût": "Risque de coûts supplémentaires pour adapter ou réparer les systèmes en raison d’erreurs dans les analyses.",
      "Durée": "Retard dans la validation des conceptions pouvant entraîner des compressions de calendrier ultérieures."
    },
    "justification": "Les erreurs dans les hypothèses compromettent la qualité des analyses, impactant directement la faisabilité et les coûts du projet."
  }
}
```

---

# Page 21

```json
[
  {
    "element_vulnerable": "Capacité d’entreposage des colis B au-delà de 15 ans",
    "menace_associee": "Épuisement des ressources d’entreposage",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectes": ["Coût", "Durée"],
      "impact_attributs": {
        "Coût": "Augmentation des coûts en raison des études, des modifications de conception et des travaux supplémentaires pour l'extension ou le développement d'un nouveau système d'entreposage.",
        "Durée": "Retard dans la réalisation du projet en raison des modifications nécessaires et des travaux supplémentaires, pouvant entraîner un report de la mise en service du bâtiment ZZ au-delà de l'échéance initiale."
      },
      "justification": "L’épuisement des ressources d’entreposage nécessite des modifications du projet (extension, nouveau système) ce qui augmente le coût et allonge la durée du projet."
    }
  },
  {
    "element_vulnerable": "Structure en charpente métallique",
    "menace_associee": "Insuffisance de la tenue aux agressions externes",
    "analyse_aloe": {
      "objet_aloe": {
        "categorie": "Livrable",
        "nom": "Bâtiment ZZ"
      },
      "attributs_affectes": ["Qualité", "Durée", "Coût"],
      "impact_attributs": {
        "Qualité": "Risque de non-conformité aux exigences de sûreté (séisme, tornade, chute d'avion) si la structure ne résiste pas aux événements attendus, compromettant ainsi la sécurité et l'intégrité du bâtiment.",
        "Durée": "Interruption des travaux ou des activités en cas de défaillance structurelle, pouvant entraîner des retards dans la construction ou dans l'utilisation du bâtiment.",
        "Coût": "Augmentation des coûts en raison des réparations, des dommages matériels, des arrêts d'activité, et potentiellement des conséquences humanitaires ou environnementales."
      },
      "justification": "Une insuffisance de la tenue de la structure face aux agressions externes peut entraîner des défaillances structurelles, impactant la qualité du livrable, provoquant des retards et augmentant les coûts."
    }
  }
]
```

---

# Page 1

```json
[]
```

---

# Page 2

```json
[]
```

---

# Page 3

```json
[]
```

---

# Page 4

```json
[
  {
    "Lien": "Influence",
    "Objet 1": "Analyse des effluents",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "Des analyses inexactes des effluents peuvent entraîner un mauvais classement des déchets, compromettant la capacité d'accueil du bâtiment ZZ et réduisant sa capacité d'entreposage."
  },
  {
    "Lien": "Échange",
    "Objet 1": "Analyse des effluents",
    "Objet 2": "Convention avec le CEA civil",
    "Justification": "L'analyse des effluents fournit des données nécessaires au CEA pour traiter les effluents, et la convention facilite l'accès aux services de traitement, créant un échange d'informations et de ressources."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Bâtiment ZZ",
    "Objet 2": "Convention avec le CEA civil",
    "Justification": "Le bâtiment ZZ ne peut accueillir les déchets qu'après l'établissement d'une convention avec le CEA civil pour gérer les traitements externes, donc il doit être achevé après la conclusion de cette convention."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Convention avec le CEA civil",
    "Objet 2": "Projet",
    "Justification": "La convention avec le CEA civil contribue à la réalisation du projet en assurant un traitement régulier et conforme des effluents, soutenant ainsi l'entreposage dans le bâtiment ZZ et respectant les délais et coûts prévus."
  }
]
```

---

# Page 5

```json
[
  {
    "Lien": "Influence",
    "Objet 1": "Barrière biologique du bâtiment ZZ",
    "Objet 2": "Gestion des déchets et entreposage",
    "Justification": "La défaillance de la barrière biologique expose le personnel aux radiations, obligeant des retards et des coûts supplémentaires dans la gestion des déchets."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Barrière biologique du bâtiment ZZ",
    "Objet 2": "Classification des effluents",
    "Justification": "La défaillance de la barrière peut entraîner des erreurs de classification des effluents en raison des interruptions et des retards."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Barrière biologique du bâtiment ZZ",
    "Objet 2": "Surveillance de l'exposition des travailleurs",
    "Justification": "La défaillance de la barrière compromet la surveillance de l'exposition, car elle expose le personnel et nécessite des investigations."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Gestion des déchets et entreposage",
    "Objet 2": "Dimensionnement de la tranche T2",
    "Justification": "Le dimensionnement de la tranche T2 doit tenir compte de la capacité d'entreposage actuelle et future, dépendant de la gestion des déchets."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Classification des effluents",
    "Objet 2": "Gestion des déchets et entreposage",
    "Justification": "Une mauvaise classification des effluents peut entraîner des retards et des coûts supplémentaires dans la gestion des déchets."
  }
]
```

---

# Page 6

```json
[]
```

---

# Page 7

```json
[
  {
    "Lien": "Influence",
    "Objet 1": "Équipement de manutention (ponts roulants)",
    "Objet 2": "Processus de manutention sécurisée des déchets",
    "Justification": "La défaillance des ponts roulants entraîne des retards dans la mise en service des installations de manutention, impactant la durée et le coût du processus sécurisé."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Équipement de manutention (ponts roulants)",
    "Objet 2": "Stock de déchets conditionnés",
    "Justification": "Les arrêts prolongés des opérations de manutention causent des dommages aux colis, affectant la qualité et le calendrier du stock d'entreposage."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Séreté électrique et contrôle des équipements critiques",
    "Objet 2": "Processus de manutention sécurisée des déchets",
    "Justification": "Les défaillances électriques compromettent les contrôles de sécurité, impactant la qualité et la conformité des opérations de manutention."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Séreté électrique et contrôle des équipements critiques",
    "Objet 2": "Stock de déchets conditionnés",
    "Justification": "Un court-circuit lié à une inondation peut endommager le stock de déchets, affectant sa qualité et sa durée de vie sécurisée."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Séreté électrique et contrôle des équipements critiques",
    "Objet 2": "Équipement de manutention (ponts roulants)",
    "Justification": "Les contrôles électriques sont essentiels pour maintenir la sécurité des équipements de manutention, donc leurs retards impactent directement la durée et le coût des opérations."
  }
]
```

---

# Page 8

```json
[]
```

---

# Page 9

```json
[]
```

---

# Page 10

```json
[
  {
    "Lien": "Influence",
    "Objet 1": "RÃ©servoir de fioul de lâ€™installation GEF",
    "Objet 2": "Colis de dÃ©chets contaminÃés",
    "Justification": "Le risque d'explosion externe lié à un accident de transport d'hydrocarbure (dont le réservoir de fioul est la source) expose les colis de déchets à une onde de surpression (50 mbar), affectant leur qualité (désintégration des colis), leur durée (retard dans le traitement) et leur coût (frai de nettoyage et gestion des déchets endommagés)."
  }
]
```

---

# Page 11

```json
[
  {
    "Lien": "Contribution",
    "Objet 1": "Bâtiment ZZ",
    "Objet 2": "Manutention des colis radioactifs",
    "Justification": "Le bâtiment ZZ fournit l'infrastructure et les locaux techniques nécessaires pour la manutention des colis radioactifs."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Bâtiment ZZ",
    "Objet 2": "Stockage et caractérisation des colis",
    "Justification": "Le bâtiment ZZ offre l'espace et les installations requises pour le stockage et la caractérisation des colis radioactifs."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Bâtiment ZZ",
    "Objet 2": "Manutention des colis radioactifs",
    "Justification": "Le bâtiment ZZ doit être achevé avant que les opérations de manutention des colis ne puissent démarrer."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Bâtiment ZZ",
    "Objet 2": "Stockage et caractérisation des colis",
    "Justification": "Le bâtiment ZZ doit être construit avant que le stockage et la caractérisation des colis ne puissent être réalisés."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Manutention des colis radioactifs",
    "Objet 2": "Stockage et caractérisation des colis",
    "Justification": "L'activité de manutention doit être achevée avant de passer au stockage et à la caractérisation des colis."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Manutention des colis radioactifs",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "Un accident de manutention peut endommager le bâtiment ZZ, affectant sa durabilité et augmentant son coût (d'après l'analyse ALOE sur les infrastructures de manutention)."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Stockage et caractérisation des colis",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "Une fuite ou manipulation inappropriée des colis pendant le stockage peut compromettre la qualité et le calendrier de livraison du bâtiment ZZ (d'après l'analyse ALOE sur le stockage des colis)."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Manutention des colis radioactifs",
    "Objet 2": "Stockage et caractérisation des colis",
    "Justification": "Une mauvaise manutention peut entraîner des retards et une dégradation de la qualité dans le processus de stockage et de caractérisation des colis (d'après l'analyse ALOE sur la manutention)."
  }
]
```

---

# Page 12

```json
[
  {
    "Lien": "Séquentiel",
    "Objet 1": "Processus de ventilation et de gestion des classes d'air",
    "Objet 2": "Activité de construction de l'extension du bâtimen ZZ",
    "Justification": "Le système de ventilation doit être installé après la réalisation des travaux de construction de l'extension."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Activité de construction de l'extension du bâtimen ZZ",
    "Objet 2": "Budget alloué à l'extension du bâtimen ZZ",
    "Justification": "Les retards ou les difficultés rencontrées lors de la construction peuvent entraîner une augmentation des coûts, impactant directement le budget alloué."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Budget alloué à l'extension du bâtimen ZZ",
    "Objet 2": "Processus de ventilation et de gestion des classes d'air",
    "Justification": "Un budget insuffisant pourrait compromettre la qualité du système de ventilation, pouvant entraîner des retards dans sa mise en service."
  },
  {
    "Lien": "Échange",
    "Objet 1": "Activité de construction de l'extension du bâtimen ZZ",
    "Objet 2": "Budget alloué à l'extension du bâtimen ZZ",
    "Justification": "Les ressources financières allouées au budget sont nécessaires pour financer les travaux de construction de l'extension."
  }
]
```

---

# Page 13

```json
[
  {
    "Lien": "Influence",
    "Objet 1": "Système de ventilation nucléaire",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "La défaillance du système de ventilation nucléaire impacte le coût, la durée et la qualité du projet, en augmentant les coûts de réparation, en retardant la mise en service et en compromettant la conformité aux normes de sécurité."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Installation de confinement C2",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "L'endommagement de l'installation de confinement C2 entraîne des retards dans la livraison, une réduction de la qualité du livrable et une augmentation des coûts de réparation, compromettant ainsi la sécurité et le respect des normes."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Intégrité fonctionnelle du local BAG",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "La rupture des systèmes de confinement dans le local BAG provoque des retards, une diminution de la qualité du livrable et une augmentation des coûts, exposant le projet à des risques de sécurité et d'indétermination technique."
  }
]
```

---

# Page 14

```json
[]
```

---

# Page 15

```json
[
  {
    "Lien": "Séquentiel",
    "Objet 1": "Caractérisation des colis type C",
    "Objet 2": "Confinement des déchets contaminés",
    "Justification": "La caractérisation des colis type C doit être réalisée avant d'atteindre le confinement des déchets contaminés, car elle fournit les données nécessaires pour valider les conditions de confinement."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Caractérisation des colis type C",
    "Objet 2": "Confinement des déchets contaminés",
    "Justification": "La caractérisation des colis type C contribue au confinement en garantissant que les déchets sont correctement identifiés et classés, réduisant les risques de non-conformité."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Caractérisation des colis type C",
    "Objet 2": "Confinement des déchets contaminés",
    "Justification": "Une caractérisation inadéquate des colis type C compromet le confinement des déchets, car elle expose à des risques de contamination et d'infidélité aux normes de sécurité."
  }
]
```

---

# Page 16

```json
[
  {
    "Lien": "Contribution",
    "Objet 1": "Extension du bâtiment 438",
    "Objet 2": "Exploitation du bâtiment ZZ et extension du bâtiment 438",
    "Justification": "L'extension du bâtiment 438 est un élément clé de l'exploitation du bâtiment ZZ, contribuant activement à la gestion des déchets et à la conformité des installations."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Extension du bâtiment 438",
    "Objet 2": "Budget d'exécution du projet",
    "Justification": "L'incertitude technique dans le dimensionnement des servitudes expose le projet à des augmentations de coût pour l'extension du bâtiment 438, impactant directement le budget d'exécution."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Exploitation du bâtiment ZZ et extension du bâtiment 438",
    "Objet 2": "Budget d'exécution du projet",
    "Justification": "La complexité logistique liée à l'exploitation du bâtiment ZZ et à l'extension du bâtiment 438 génère des retards et des ajustements coûteux, influençant négativement le budget d'exécution."
  }
]
```

---

# Page 17

```json
[
  {
    "Lien": "Séquentiel",
    "Objet 1": "Conteneur J avec recombineur",
    "Objet 2": "Processus d'installation et de stockage des conteneurs J",
    "Justification": "Le processus d'installation dépend de la présence et de la conformité du conteneur J, qui doit être préparé avant son installation."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Processus d'installation et de stockage des conteneurs J",
    "Objet 2": "Objectif de mise en service finale des colis B",
    "Justification": "Le processus d'installation doit être achevé pour que les colis B soient stockés dans le conteneur J et que l'objectif de mise en service finale soit atteint."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Bâtiment 438",
    "Objet 2": "Processus d'installation et de stockage des conteneurs J",
    "Justification": "Le processus d'installation des conteneurs J ne peut démarrer que si le bâtiment 438 est prêt et adapté au stockage temporaire."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Bâtiment 438",
    "Objet 2": "Objectif de mise en service finale des colis B",
    "Justification": "Le bâtiment 438 doit être construit et opérationnel avant que les colis B ne puissent être transférés pour leur stockage final dans l'extension parasismique."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Conteneur J avec recombineur",
    "Objet 2": "Processus d'installation et de stockage des conteneurs J",
    "Justification": "Une défaillance du catalyseur ou une incompatibilité structurelle avec les fûts D affecte directement la qualité, la durée et le coût du processus d'installation."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Conteneur J avec recombineur",
    "Objet 2": "Objectif de mise en service finale des colis B",
    "Justification": "Le risque de défaillance du catalyseur ou d'incompatibilité prolonge les délais et augmente les coûts, compromettant la réalisation de l'objectif de mise en service finale."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Bâtiment 438",
    "Objet 2": "Processus d'installation et de stockage des conteneurs J",
    "Justification": "L'inadaptation du bâtiment 438 expose à des risques de dommages aux colis A/B, impactant la qualité et la durée du processus d'installation."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Bâtiment 438",
    "Objet 2": "Objectif de mise en service finale des colis B",
    "Justification": "Un retard dans la construction ou une mauvaise adaptation du bâtiment 438 entraîne des reports dans le calendrier et des surcoûts pour l'objectif de mise en service finale."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Processus d'installation et de stockage des conteneurs J",
    "Objet 2": "Conteneur J avec recombineur",
    "Justification": "Le processus d'installation garantit la conformité et la sécurité opérationnelle du conteneur J, contribuant à sa qualité et à son bon fonctionnement."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Bâtiment 438",
    "Objet 2": "Processus d'installation et de stockage des conteneurs J",
    "Justification": "Le bâtiment 438 fournit l'infrastructure nécessaire au stockage temporaire, soutenant activement le processus d'installation des conteneurs J."
  }
]
```

---

# Page 18

```json
[
  {
    "Lien": "Séquentiel",
    "Objet 1": "Phase de réalisation du bâtiment ZZ",
    "Objet 2": "Mise en service à fin 2036",
    "Justification": "La phase de réalisation du bâtiment ZZ doit être achevée avant que la mise en service à fin 2036 ne puisse être atteinte."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Phase de réalisation du bâtiment ZZ",
    "Objet 2": "Mise en service à fin 2036",
    "Justification": "La variabilité des délais et des coûts (menace) impacte directement la durée et le coût de la réalisation, compromettant ainsi la mise en service à fin 2036."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Phase de réalisation du bâtiment ZZ",
    "Objet 2": "Mise en service à fin 2036",
    "Justification": "Le retard dans l’aménagement des servitudes (menace) perturbe le calendrier de réalisation, pouvant retarder la mise en service et augmenter les coûts."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Phase de réalisation du bâtiment ZZ",
    "Objet 2": "Mise en service à fin 2036",
    "Justification": "L’optimisation insuffisante des ressources (menace) affecte la durée et le coût de la réalisation, compromettant la mise en service à fin 2036."
  }
]
```

---

# Page 19

```json
[]
```

---

# Page 20

```json
[
  {
    "Lien": "Contribution",
    "Objet 1": "Structure en charpente métallique du bâtiment de stockage",
    "Objet 2": "Bâtiment de stockage pour colis type B au-delà de 15 ans",
    "Justification": "La structure en charpente métallique est un élément clé du bâtiment de stockage, sans laquelle il ne peut être réalisé."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Bâtiment de stockage pour colis type B au-delà de 15 ans",
    "Justification": "Les analyses de sécurité garantissent la conformité du bâtiment aux exigences de sûreté, contribuant à sa qualité et à son acceptation."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Structure en charpente métallique du bâtiment de stockage",
    "Justification": "Les analyses de sécurité sont nécessaires pour valider la conception de la structure, assurant sa conformité aux normes."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Structure en charpente métallique du bâtiment de stockage",
    "Justification": "Les analyses de sécurité doivent être achevées avant de pouvoir approuver la conception de la structure."
  },
  {
    "Lien": "Séquentiel",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Bâtiment de stockage pour colis type B au-delà de 15 ans",
    "Justification": "Les analyses de sécurité doivent être finalisées avant de pouvoir approuver le bâtiment."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Structure en charpente métallique du bâtiment de stockage",
    "Objet 2": "Bâtiment de stockage pour colis type B au-delà de 15 ans",
    "Justification": "La structure en charpente métallique, étant soumise à des risques (séismes, tornades), peut entraîner des retards et des augmentations de coûts si ces risques ne sont pas correctement gérés."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Structure en charpente métallique du bâtiment de stockage",
    "Justification": "Les analyses de sécurité, si elles contiennent des erreurs, peuvent mener à une conception de structure insuffisante, augmentant les coûts et les délais."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Bâtiment de stockage pour colis type B au-delà de 15 ans",
    "Justification": "Les analyses de sécurité, si elles sont inadéquates, peuvent entraîner une conception du bâtiment non conforme, augmentant les risques sur la qualité, les coûts et les délais."
  },
  {
    "Lien": "Échange",
    "Objet 1": "Analyses de sécurité pour les différents scénarios d'agressions",
    "Objet 2": "Structure en charpente métallique du bâtiment de stockage",
    "Justification": "Les analyses de sécurité utilisent les caractéristiques de la structure pour évaluer les risques et, à l'inverse, fournissent des recommandations pour la conception."
  }
]
```

---

# Page 21

[
  {
    "Lien": "Contribution",
    "Objet 1": "Épuisement des ressources d’entreposage",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "L’épuisement des ressources d’entreposage nécessite des modifications du projet (extension ou nouveau système) ce qui influence directement le Bâtiment ZZ."
  },
  {
    "Lien": "Contribution",
    "Objet 1": "Insuffisance de la tenue aux agressions externes",
    "Objet 2": "Bâtiment ZZ",
    "Justification": "L’insuffisance de la tenue de la structure face aux agressions externes nécessite des validations et des ajustements pour le Bâtiment ZZ."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Épuisement des ressources d’entreposage",
    "Objet 2": "Coût du Bâtiment ZZ",
    "Justification": "L’épuisement des ressources d’entreposage entraîne une augmentation des coûts en raison des études, modifications et travaux supplémentaires."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Épuisement des ressources d’entreposage",
    "Objet 2": "Durée du projet",
    "Justification": "L’épuisement des ressources d’entreposage cause des retards dans la réalisation du projet en raison des modifications nécessaires."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Insuffisance de la tenue aux agressions externes",
    "Objet 2": "Qualité du Bâtiment ZZ",
    "Justification": "L’insuffisance de la tenue aux agressions externes expose le Bâtiment ZZ à des risques de non-conformité aux exigences de sécurité."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Insuffisance de la tenue aux agressions externes",
    "Objet 2": "Durée du projet",
    "Justification": "Les défaillances structurelles dues à l’insuffisance de la tenue peuvent entraîner des interruptions des travaux et des retards."
  },
  {
    "Lien": "Influence",
    "Objet 1": "Insuffisance de la tenue aux agressions externes",
    "Objet 2": "Coût du Bâtiment ZZ",
    "Justification": "Les défaillances structurelles et les réparations liées à l’insuffisance de la tenue augmentent les coûts du projet."
  }
]
