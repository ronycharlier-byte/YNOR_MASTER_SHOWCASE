# Rebuild des PDFs LaTeX

Ce dossier contient le script PowerShell de reconstruction des PDFs à partir des sources `.tex` corrigées.

## Prerequis

- Un moteur LaTeX disponible dans le `PATH`
- `latexmk` est prefere, sinon `pdflatex`, `xelatex` ou `lualatex`

## Ordre recommande

1. `P0` : noyau central et textes de reference
2. `P1` : releases majeures et proofs
3. `P2` : miroirs, exports memoire et variantes augmentees

## Commandes utiles

Reconstruire uniquement le noyau prioritaire :

```powershell
.\rebuild_latex_pdfs.ps1 -Priority P0
```

Reconstruire tout le corpus :

```powershell
.\rebuild_latex_pdfs.ps1 -Priority All
```

Forcer un compilateur precis :

```powershell
.\rebuild_latex_pdfs.ps1 -Priority P1 -Compiler pdflatex
```

Limiter le nombre de fichiers pour un test rapide :

```powershell
.\rebuild_latex_pdfs.ps1 -Priority P2 -Limit 3
```

## Notes

- Le script reconstruit les PDFs dans le dossier source de chaque `.tex`.
- Si un fichier source est absent, il est marque `Missing` et le traitement continue.
- L'environnement actuel ne dispose pas d'un compilateur LaTeX, donc le lancement effectif devra se faire sur une machine ou un environnement qui l'expose dans le `PATH`.
