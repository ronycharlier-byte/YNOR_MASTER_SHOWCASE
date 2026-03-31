import tiktoken

def compress_context(files_content, max_tokens=1500):
    """
    Optimise le contexte envoye a l'IA pour reduire les couts (Strategie MDL Ynor).
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    optimized_context = ""
    
    for filename, text in files_content.items():
        tokens = encoding.encode(text)
        if len(tokens) > 500:
            # On ne garde que le debut, le milieu et la fin (Resume extractif)
            summary = text[:300] + "\n[...]\n" + text[-300:]
            optimized_context += f"### SOURCE: {filename} (Compressed)\n{summary}\n\n"
        else:
            optimized_context += f"### SOURCE: {filename}\n{text}\n\n"
            
    return optimized_context



