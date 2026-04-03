import os
import glob
import json
from openai import OpenAI

# Configuration : Dossier racine de votre PC contenant le corpus
CORPUS_ROOT = os.path.abspath(os.path.join(os.getcwd(), ".."))
INDEX_FILE = "corpus_index.json"

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def get_embedding(client, text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def build_index():
    print("========================================")
    print("MOTEUR Autonome et Isolé : Indexation Vectorielle")
    print("========================================")
    
    # 1. Scanner tous les fichiers markdown (Corpus global + Canonical Distribution)
    md_files = glob.glob(os.path.join(CORPUS_ROOT, "**", "*.md"), recursive=True)
    
    print(f"[{len(md_files)}] fichiers Markdown trouvés à indexer.")
    
    if len(md_files) == 0:
        print("Erreur: Aucun fichier trouvé dans", CORPUS_ROOT)
        return

    client = OpenAI() # S'appuie sur os.environ["OPENAI_API_KEY"]
    index_data = []

    for file_path in md_files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # 2. Chunking (découpage intelligent)
            chunks = chunk_text(content, chunk_size=400, overlap=50)
            
            for i, chunk in enumerate(chunks):
                if len(chunk.split()) < 20: continue # Ignorer les blocs trop petits
                
                # 3. Récupération de l'embedding (Vectorisation sémantique)
                print(f"Vectorisation : {os.path.basename(file_path)} (Chunk {i+1}/{len(chunks)})")
                emb = get_embedding(client, chunk)
                
                index_data.append({
                    "file": os.path.basename(file_path),
                    "chunk_id": i,
                    "text": chunk,
                    "embedding": emb
                })
        except Exception as e:
            print(f"X Erreur sur {file_path}: {e}")
            
    # 4. Sauvegarde des poids dans des fichiers optimisés pour la mémoire
    META_PATH = "index_meta.json"
    VECT_PATH = "index_vectors.npy"
    
    print(f"Sauvegarde des métadonnées dans {META_PATH}...")
    meta_data = [{"text": item["text"], "file": item["file"]} for item in index_data]
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, ensure_ascii=False)
        
    print(f"Sauvegarde des vecteurs binaires dans {VECT_PATH}...")
    import numpy as np
    vectors = np.array([item["embedding"] for item in index_data], dtype=np.float32)
    np.save(VECT_PATH, vectors)
        
    print("========================================")
    print(f"SUCCÈS : Index Vectoriel Optimisé généré.")
    print(f"Total des vecteurs : {len(index_data)}")
    print("========================================")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ ERREUR CRITIQUE : OPENAI_API_KEY absente des variables d'environnement.")
    else:
        build_index()
