import os



def fractal_expand():

 print("=== YNOR FRACTAL EXPANDER (V12.0) ===")

 

 # Structure Sym?trie R?cursive Standard

 chiastic_skeleton = [

 '_01_A_FONDATION_LOCAL',

 '_02_B_THEORIE_LOCAL',

 '_03_C_MOTEUR_LOCAL',

 '_04_X_NOYAU_LOCAL',

 '_05_C_PRIME_VALIDATION_LOCAL',

 '_06_B_PRIME_GOUVERNANCE_LOCAL',

 '_07_A_PRIME_ARCHIVE_LOCAL'

 ]

 

 # Identification des 7 couches racine

 all_dirs = [d for d in os.listdir('.') if os.path.isdir(d)]

 layers_prefixes = ['01_A', '02_B', '03_C', '04_X', '05_C_PRIME', '06_B_PRIME', '07_A_PRIME']

 

 target_layers = []

 for pref in layers_prefixes:

 d = next((d for d in all_dirs if d.startswith(pref)), None)

 if d:

 target_layers.append(d)

 

 print(f"Nodes Parents Dtects : {len(target_layers)}")

 

 expanded_count = 0

 

 for parent in target_layers:

 print(f"\n--- Expansion de : {parent} ---")

 for sub in chiastic_skeleton:

 sub_path = os.path.join(parent, sub)

 if not os.path.exists(sub_path):

 try:

 os.makedirs(sub_path)

 print(f"[NEW] {sub_path} -> CRÉE")

 

 # Ajout d'un 00_NODE.md explicatif

 node_md = os.path.join(sub_path, '00_NODE.md')

 with open(node_md, 'w', encoding='utf-8') as f:

 f.write(f"# {sub.replace('_', ' ').strip()}\n")

 f.write(f"Ce rpertoire est un sous-noeud fractal du module {parent}.\n")

 f.write(f"Status : Initialispar le Protocole Ynor V12.\n")

 

 expanded_count += 1

 except Exception as e:

 print(f"[ERREUR] Impossible de crer {sub_path}: {e}")

 else:

 print(f"[OK] {sub_path} -> EXISTANT")

 

 print(f"\n=== EXPANSION TERMINÉE : {expanded_count} NODES FRACTALISÉS ===")

 print("STATUT : HIERACHIE INITIALISÉE.")



if __name__ == "__main__":

 fractal_expand()

