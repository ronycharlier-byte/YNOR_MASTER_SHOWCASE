# MIROIR TEXTUEL - read_all_pdfs.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\read_all_pdfs.py
Taille : 881 octets
SHA256 : 544ced8a55c3528b39d46a83d26050208cf07658b6b66300eb2b8078e0763fef

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import os
import PyPDF2

directory = "."
files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
files.sort()

for file in files:
    try:
        with open(file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()
                print(f"--- {file} ---")
                print(text[:1000]) # Print first 1000 characters
                print("\n")
    except Exception as e:
        print(f"Error reading {file}: {e}")

```