"""
Utilitaires partagés pour le pipeline ETL Mexora RH.
"""
import os
from pathlib import Path


def ensure_directory(path: str) -> Path:
    """Crée un répertoire s'il n'existe pas et retourne le Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_file_size_str(filepath: str) -> str:
    """Retourne la taille d'un fichier en format lisible (Ko, Mo)."""
    size = os.path.getsize(filepath)
    if size < 1024:
        return f"{size} o"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} Ko"
    else:
        return f"{size / (1024 * 1024):.1f} Mo"


def print_step(layer: str, message: str):
    """Affiche un message de progression formaté pour le pipeline."""
    print(f"[{layer.upper()}] {message}")
