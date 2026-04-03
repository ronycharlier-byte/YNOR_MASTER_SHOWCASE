import os
import shutil

# Root directory of the framework
BASE_DIR = r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework"

# Files to synchronize (Source -> Targets)
# We choose the best/most complete version as source
SYNC_PLAN = [
    {
        "src": os.path.join(BASE_DIR, "_01_THEORY_AND_PAPERS", "MDL_YNOR_TECHNICAL_SPECIFICATIONS.md"),
        "targets": [
            os.path.join(BASE_DIR, "_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES", "MDL_YNOR_TECHNICAL_SPECIFICATIONS.md"),
            os.path.join(BASE_DIR, "MDL_YNOR_GPT_KNOWLEDGE", "MDL_YNOR_TECHNICAL_SPECIFICATIONS.md")
        ]
    },
    {
        "src": os.path.join(BASE_DIR, "_01_THEORY_AND_PAPERS", "MDL_YNOR_SCIENTIFIC_WHITE_PAPER.md"),
        "targets": [
            os.path.join(BASE_DIR, "_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES", "MDL_YNOR_SCIENTIFIC_WHITE_PAPER.md"),
            os.path.join(BASE_DIR, "MDL_GPT_KNOWLEDGE_PRODUCTION", "MDL_YNOR_SCIENTIFIC_WHITE_PAPER.md")
        ]
    },
    {
        "src": os.path.join(BASE_DIR, "_PREUVES_ET_RAPPORTS", "BENCHMARK_ULTRA_HARDCORE_ULTIMATE_10_10.md"),
        "targets": [
            os.path.join(BASE_DIR, "_01_THEORY_AND_PAPERS", "BENCHMARK_ULTRA_HARDCORE_ULTIMATE_10_10.md"),
            os.path.join(BASE_DIR, "_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES", "BENCHMARK_ULTRA_HARDCORE_ULTIMATE_10_10.md")
        ]
    }
]

def deep_sync():
    print("--- LANCEMENT DE LA SYNCHRONISATION PROFONDE DU CORPUS ---")
    for task in SYNC_PLAN:
        src = task["src"]
        if not os.path.exists(src):
            print(f"⚠️ Source manquante : {src}")
            continue
            
        for target in task["targets"]:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(src, target)
            print(f"✅ Synchronisé : {os.path.relpath(target, BASE_DIR)}")

    print("\n--- SYNCHRONISATION TERMINÉE ---")

if __name__ == "__main__":
    deep_sync()
