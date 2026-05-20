# 🚀 Data Lake Mexora RH - Miniprojet 2

**Réalisé par :** Aymane El Hasnaoui  
**Encadré par :** Pr. Zili  
**Établissement :** Faculté des Sciences et Techniques de Tanger (FSTT)  
**Date :** Mai 2026  

## 📖 Description du Projet
Ce projet implémente une architecture Data Lake complète (zones Bronze, Silver et Gold) pour analyser le marché de l'emploi IT au Maroc. Il a pour but d'aider la direction des Ressources Humaines de l'entreprise fictive Mexora (basée à Tanger) à définir sa stratégie de recrutement en traitant 5000 offres d'emploi brutes.

## 🛠️ Prérequis
Assurez-vous d'avoir **Python 3.11** ou supérieur installé sur votre machine.  
Les bibliothèques suivantes sont requises pour exécuter le pipeline :

```bash
pip install -r requirements.txt
```

Ou bien installez-les manuellement :

```bash
pip install pandas pyarrow duckdb
```

## 📂 Structure du Projet

```
mexora_rh_project/
│
├── source_data/                              # Fichiers bruts générés (offres, référentiel, entreprises)
├── data_lake_mexora_rh/                      # Le Data Lake (généré automatiquement par le pipeline)
│   ├── bronze/                               # Données brutes immuables (JSON)
│   ├── silver/                               # Données nettoyées (Parquet compressé)
│   └── gold/                                 # Tables analytiques (Parquet via DuckDB)
│
├── pipeline/                                 # Scripts ETL Python
│   ├── bronze_ingestion.py                   # Ingestion et partitionnement
│   ├── silver_transform.py                   # Nettoyage (salaires, dates, profils)
│   ├── silver_nlp.py                         # Extraction de compétences par NLP
│   └── gold_aggregation.py                   # Requêtes analytiques DuckDB
│
├── main.py                                   # Orchestrateur central du pipeline
├── generate_companies.py                     # Script de génération de données (mock)
├── generate_skills.py                        # Script de génération de données (mock)
├── generate_mock_data.py                     # Script de génération de données (mock)
├── README.md                                 # Instructions d'exécution
└── rapport_pipeline.md                       # Rapport de nettoyage technique
```

## 🚀 Instructions pour reproduire le pipeline

### Étape 1 : Génération des données sources
L'énoncé stipulant qu'aucun fichier de données n'est fourni, vous devez d'abord générer les fichiers bruts. Exécutez ces scripts dans cet ordre précis :

```bash
python generate_companies.py
python generate_skills.py
python generate_mock_data.py
```

> **Note :** Assurez-vous de déplacer les fichiers générés (`offres_emploi_it_maroc.json`, `referentiel_competences_it.json`, `entreprises_it_maroc.csv`) dans le dossier `source_data/`.

### Étape 2 : Exécution du Pipeline Data Lake
Pour exécuter l'ensemble du pipeline ETL, de l'ingestion brute jusqu'à la création des tables analytiques Gold, lancez simplement la commande suivante à la racine du projet :

```bash
python main.py
```

### Étape 3 : Vérification
Le script affichera dans la console la progression détaillée des traitements.  
Une fois terminé, le répertoire `data_lake_mexora_rh/gold/` contiendra les 5 fichiers `.parquet` (Top compétences, Salaires par profil, etc.) prêts à être analysés dans l'Étape 3 avec DuckDB.