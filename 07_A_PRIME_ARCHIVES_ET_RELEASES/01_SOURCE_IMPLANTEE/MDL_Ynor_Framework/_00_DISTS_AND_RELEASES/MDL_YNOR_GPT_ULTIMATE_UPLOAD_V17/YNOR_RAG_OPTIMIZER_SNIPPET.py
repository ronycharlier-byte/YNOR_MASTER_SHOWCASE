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
