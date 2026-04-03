# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
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



