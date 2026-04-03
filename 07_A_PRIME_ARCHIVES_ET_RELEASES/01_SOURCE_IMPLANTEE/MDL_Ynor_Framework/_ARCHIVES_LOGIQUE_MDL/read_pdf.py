# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import PyPDF2

file_path = "Chapitre I  Formalisation axiomatique minimale.pdf"

try:
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        # Only read the first 5 pages to get the gist
        num_pages = min(len(reader.pages), 5)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
            
    print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")



