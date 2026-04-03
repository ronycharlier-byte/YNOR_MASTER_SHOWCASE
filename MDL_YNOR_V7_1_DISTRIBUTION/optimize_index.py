import json
import numpy as np
import os

def optimize():
    # PATHS
    JSON_PATH = "corpus_index.json"
    META_PATH = "index_meta.json"
    VECT_PATH = "index_vectors.npy"

    if not os.path.exists(JSON_PATH):
        print(f"Erreur: {JSON_PATH} non trouvé.")
        return

    print(f"Chargement de {JSON_PATH} (98MB)...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Extraction des métadonnées ({len(data)} vecteurs)...")
    # On ne garde que le texte et le nom du fichier pour les métadonnées
    meta = [{"text": item["text"], "file": item["file"]} for item in data]
    
    print(f"Formatage de la matrice d'embeddings...")
    # On convertit les listes de floats en un array numpy (Float32 pour économiser 50% vs Float64)
    vectors = np.array([item["embedding"] for item in data], dtype=np.float32)

    print(f"Sauvegarde des métadonnées dans {META_PATH}...")
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)

    print(f"Sauvegarde des vecteurs dans {VECT_PATH}...")
    np.save(VECT_PATH, vectors)

    print("OPTIMISATION COMPLÉTÉE (Total Diamond Memory Optimization)")
    print(f"Taille finale Meta: {os.path.getsize(META_PATH)/1024/1024:.2f} MB")
    print(f"Taille finale Vect: {os.path.getsize(VECT_PATH)/1024/1024:.2f} MB")

if __name__ == "__main__":
    optimize()
