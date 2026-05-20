from pipeline.bronze_ingestion import ingerer_bronze
from pipeline.silver_transform import charger_depuis_bronze, nettoyer_titres_postes, normaliser_salaires, normaliser_experience
from pipeline.silver_nlp import extraire_competences, sauvegarder_silver
from pipeline.gold_aggregation import construire_gold

# Paths
SOURCE_FILE = "source_data/offres_emploi_it_maroc.json"
REF_COMPETENCES = "source_data/referentiel_competences_it.json"
DATA_LAKE_ROOT = "data_lake_mexora_rh"

def run_pipeline():
    print("=== Démarrage du Pipeline Mexora RH ===")
    
    # ÉTAPE 2.2 : Ingestion Bronze
    ingerer_bronze(SOURCE_FILE, DATA_LAKE_ROOT)
    
    print("\n-------------------------------------------")
    # ÉTAPE 2.3 : Transformation Silver
    df_bronze = charger_depuis_bronze(DATA_LAKE_ROOT)
    df_clean_titles = nettoyer_titres_postes(df_bronze)
    df_clean_salaries = normaliser_salaires(df_clean_titles)
    df_clean_exp = normaliser_experience(df_clean_salaries)
    
    print("\n-------------------------------------------")
    # ÉTAPE 2.4 : NLP & Sauvegarde Silver
    df_competences = extraire_competences(df_clean_exp, REF_COMPETENCES)
    sauvegarder_silver(df_clean_exp, df_competences, DATA_LAKE_ROOT)
    
    print("\n-------------------------------------------")
    # ÉTAPE 2.5 : Agrégation Gold avec DuckDB
    construire_gold(DATA_LAKE_ROOT)
    
    print("\n=== Pipeline Data Lake Terminé avec Succès ===")

if __name__ == "__main__":
    run_pipeline()