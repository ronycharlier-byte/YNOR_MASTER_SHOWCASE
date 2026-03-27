# MIROIR TEXTUEL - YNOR_RAG_OPTIMIZER_SNIPPET.py

Source : MDL_Ynor_Framework\_00_DISTS_AND_RELEASES\MDL_YNOR_GPT_ULTIMATE_UPLOAD_V17\YNOR_RAG_OPTIMIZER_SNIPPET.py
Taille : 735 octets
SHA256 : 724b7c38584dfbe56b59eb98a99fe3c9b26bd6ebf0267ce42033a7f28b0af9b2

```text
import tiktoken

def compress_context(files_content, max_tokens=1500):
    """
    Optimise le contexte envoyé à l'IA pour réduire les coûts (Stratégie MDL Ynor).
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    optimized_context = ""
    
    for filename, text in files_content.items():
        tokens = encoding.encode(text)
        if len(tokens) > 500:
            # On ne garde que le début, le milieu et la fin (Résumé extractif)
            summary = text[:300] + "\n[...]\n" + text[-300:]
            optimized_context += f"### SOURCE: {filename} (Compressed)\n{summary}\n\n"
        else:
            optimized_context += f"### SOURCE: {filename}\n{text}\n\n"
            
    return optimized_context

```