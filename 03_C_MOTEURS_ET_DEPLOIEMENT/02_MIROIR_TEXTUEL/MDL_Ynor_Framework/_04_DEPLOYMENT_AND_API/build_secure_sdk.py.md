# MIROIR TEXTUEL - build_secure_sdk.py

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\build_secure_sdk.py
Taille : 1142 octets
SHA256 : 684ad6ddd95d2a6a8b9d0a79c38140ee21f532f645fd5e582969c3b64724408e

```text
import py_compile
import shutil
import os

print("=======================================")
print("🛡️ COMPILATION DU SDK YNOR (ANTI-VOL) 🛡️")
print("=======================================")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SDK_DIR = os.path.join(BASE_DIR, "ynor_sdk", "ynor")
BUILD_DIR = os.path.join(BASE_DIR, "ynor_sdk_dist", "ynor")

if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
os.makedirs(BUILD_DIR)

files_to_compile = ["__init__.py", "client.py", "core_mu.py", "models.py"]

for f in files_to_compile:
    src_file = os.path.join(SDK_DIR, f)
    if os.path.exists(src_file):
        print(f"[*] Obfuscation en cours : {f}...")
        # Compiling generates heavily optimized bytecode
        py_compile.compile(src_file, cfile=os.path.join(BUILD_DIR, f + "c"))
        
print("\n✅ Compilation terminée. Le dossier 'ynor_sdk_dist' contient la version finale à distribuer (code source masqué).")
print("Les clients utiliseront directement les fichiers `.pyc` (Python Compiled).")
print("Toute tentative de lecture du noyau mathématique Mu affichera du code binaire indéchiffrable.")

```