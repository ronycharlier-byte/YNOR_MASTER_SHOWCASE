import os

# ==============================================================================
# MDL YNOR ACADEMIC NORMALIZATION - QUICK FIXES
# ==============================================================================

ROOT_DIR = r"c:\Users\ronyc\Desktop\FRACTAL_CHIASTE_UNIVERSEL"

fixes = {
    "$\$$\mu = 1.0$$": "$\\mu = 1.0$",
    "CANONIQUEE": "CANONIQUE",
    "canoniquee": "canonique",
    "STABILITÉ / CANONICITÉ Totale": "Stabilité Totale",
    "$\$\mu = 1.0$$": "$\\mu = 1.0$"
}

def fix_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content
        for k, v in fixes.items():
            new_content = new_content.replace(k, v)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except:
        return False
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith((".md", ".txt", ".tex")):
                if fix_file(os.path.join(root, file)):
                    count += 1
    print(f"Fixes appliqués à {count} fichiers.")

if __name__ == "__main__":
    main()
