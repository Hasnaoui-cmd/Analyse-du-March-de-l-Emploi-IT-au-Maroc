# 📄 Rapport de Traitement du Pipeline ETL (Data Lake Mexora RH)

**Réalisé par :** Aymane El Hasnaoui  
**Encadré par :** Pr. Zili  
**Établissement :** Faculté des Sciences et Techniques de Tanger (FSTT)  

---

## Introduction
Ce document justifie les transformations appliquées lors du passage des données de la zone **Bronze** (données brutes et immuables) vers la zone **Silver** (données nettoyées et standardisées), conformément aux exigences techniques du projet et aux principes de la Business Intelligence.

---

## 1. Normalisation des Titres de Postes
* **La règle appliquée :** Utilisation d'expressions régulières (Regex) pour scanner le champ `titre_poste` brut et le mapper vers l'une des familles de profils standards du marché (ex: "Data Engineer", "Data Analyst", "Développeur Full Stack", etc.).
* **Nombre de lignes avant / après :** 5 000 offres en entrée ➔ 5 000 offres en sortie (Aucune suppression de ligne pour conserver l'intégrité du volume global).
* **Les cas limites rencontrés et leur traitement :** * *Cas limite :* Des intitulés très spécifiques, mal orthographiés, ou ne correspondant à aucun métier IT classique (ex: "Intégrateur Odoo junior").
    * *Traitement :* Création d'une catégorie par défaut `Autre IT`. Si aucune expression régulière ne correspond, l'offre est classée dans `Autre IT` au lieu d'être supprimée, garantissant ainsi la complétude des données géographiques et salariales.

## 2. Normalisation des Salaires
* **La règle appliquée :** Extraction numérique des fourchettes de salaires depuis une chaîne de caractères libre. Conversion systématique des devises en MAD (Taux fixe utilisé : 1 EUR = 10.8 MAD). Calcul de la moyenne entre le minimum et le maximum extrait pour obtenir le `salaire_median_mad`.
* **Nombre de lignes avant / après :** 5 000 offres ➔ 5 000 offres enrichies de colonnes calculées (`salaire_min_mad`, `salaire_max_mad`, `salaire_connu`, `salaire_median_mad`).
* **Les cas limites rencontrés et leur traitement :**
    * *Cas limite 1 :* Présence de la lettre "K" pour abréger les milliers (ex: "15K-20K").
        * *Traitement :* Remplacement par une multiplication par 1000 avant la conversion en type `float`.
    * *Cas limite 2 :* Salaires masqués ("Selon profil", "Confidentiel") ou champs vides (Null).
        * *Traitement :* Le flag booléen `salaire_connu` passe à `False` et les montants numériques sont fixés à `None` (Null) pour ne pas fausser les moyennes lors de l'agrégation DuckDB (zone Gold).
    * *Cas limite 3 :* Valeurs aberrantes (salaires < 3000 MAD ou > 100 000 MAD par mois).
        * *Traitement :* Ces valeurs sont considérées comme des erreurs de saisie (Garbage in). Elles sont neutralisées via le passage du flag `salaire_connu` à `False`.

## 3. Normalisation de l'Expérience Requise
* **La règle appliquée :** Conversion des expressions textuelles en limites mathématiques précises (`experience_min_ans` et `experience_max_ans`).
* **Nombre de lignes avant / après :** 5 000 offres ➔ 5 000 offres avec colonnes d'expérience fortement typées (Entiers).
* **Les cas limites rencontrés et leur traitement :**
    * *Cas limite 1 :* Texte sans chiffre explicite (ex: "Débutant", "Junior", "Stage").
        * *Traitement :* Mapping forcé par mot-clé à `min = 0` et `max = 2`.
    * *Cas limite 2 :* Profils expérimentés sans limite supérieure définie (ex: "Senior", "Expert", "Lead").
        * *Traitement :* Mapping forcé à `min = 5` et `max = None` (infini).

## 4. Extraction des Compétences (Processus NLP)
* **La règle appliquée :** Concaténation des champs `competences_brut` et `description`. Parcours du dictionnaire `referentiel_competences_it.json`. Les alias du dictionnaire sont triés par ordre décroissant de longueur de chaîne. Utilisation des frontières de mots (`\b` en Regex) pour extraire les correspondances exactes.
* **Nombre de lignes avant / après :** 5 000 offres (Silver Offres) ➔ Génération d'une nouvelle table relationnelle (`competences.parquet`) d'environ ~15 000 à 25 000 lignes. Le grain de cette table change : 1 ligne = 1 association [Offre ↔ Compétence].
* **Les cas limites rencontrés et leur traitement :**
    * *Cas limite 1 :* Conflit d'inclusion (ex: "node" capturé à l'intérieur de "node.js").
        * *Traitement :* Le tri par longueur de chaîne garantit que "node.js" est testé et extrait avant "node".
    * *Cas limite 2 :* Les langages "C" ou "R" qui peuvent être confondus avec des lettres normales dans une phrase.
        * *Traitement :* L'utilisation stricte de la frontière de mot `\b` garantit que seules les lettres isolées sont capturées en tant que technologies.
    * *Cas limite 3 :* Une offre très courte ou non-technique ne contenant aucune compétence du référentiel.
        * *Traitement :* Génération d'une ligne d'échappement avec la valeur `non_détecté` pour la compétence et `inconnu` pour la famille. Cela permet de conserver la traçabilité de l'offre et de mesurer la qualité rédactionnelle des annonces sans casser les jointures.

---
**Conclusion sur la Gouvernance des Données :** L'approche choisie (Schema-on-read en Bronze puis typage strict en Silver) a permis de ne perdre aucune offre brute. L'isolation de la qualité des données via des attributs descriptifs (`salaire_connu`, `profil_normalise`) garantit que la couche analytique Gold reposera sur des bases mathématiques saines, éliminant le risque de "Data Swamp".