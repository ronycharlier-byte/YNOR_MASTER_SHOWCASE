import os
import re

ROOT_DIR = r"c:\Users\ronyc\Desktop\MDL Ynor"

def strip(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False
        
    original = content
    # Retire "", "", "", "" etc.
    # Ex: "Corpus Chiaste" -> "Corpus Chiaste"
    # Ex: "FRACTAL_CHIASTE" -> "FRACTAL_CHIASTE"
    content = re.sub(r'(?i)[_\s\-]*(le)?(s)?\b', '', content)
    
    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        if '.git' in root or '.obsidian' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith(('.md', '.txt', '.tex', '.json', '.py', '.bat', '.yaml', '.yml')):
                filepath = os.path.join(root, file)
                if strip(filepath):
                    count += 1
    
    print(f"Termine. Le mot '(le)' a ete retire de {count} fichiers.")

if __name__ == '__main__':
    main()
