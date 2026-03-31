# VALIDATION SCIENTIFIQUE YNOR

## Objectif
Definir le niveau de preuve attendu pour les affirmations scientifiques du corpus.

## Echelle De Preuve
- Hypothese: affirmation de travail formulee clairement.
- Preuve interne: derivation formelle, calcul, ou test reproductible dans le depot.
- Reproduction locale: execution independante du protocole avec memes entrees et memes sorties attendues.
- Verification externe: reproduction par un tiers hors depot.
- Validation scientifique forte: reproduction externe accompagnee d'une analyse critique.

## Niveaux De Maturite
- Brouillon scientifique: hypothese formulee, protocole encore incomplet.
- Bloc formalise: resultats mathematiques ou logiques definis et controle interne etabli.
- Bloc reproductible localement: protocole executable, entrees fixees, sortie stabilisee.
- Bloc en attente de revue externe: formulation nette, hypothese circonscrite, limites et traceabilite explicites.
- Bloc scientifiquement consolide: revue ou reproduction externe disponible.

## Parcours De validation externe
- Fixer un paquet de revue avec hypothese, protocole, artefacts et limites.
- Geler les entrees de reference et les criteres de sortie.
- Fournir une version lisible pour tiers avec resume, bibliographie et statut de preuve.
- Permettre une reproduction independante sans contexte implicite du depot.
- Archiver les retours externes, les ecarts et les corrections resultantes.
- Consolider les blocs deja reproductibles localement en les integrant au coeur etabli du corpus avant leur passage en revue externe.

## Regles De Redaction
- Toute affirmation forte doit indiquer son niveau de preuve.
- Toute statistique doit mentionner son protocole, son jeu de donnees et sa limite.
- Toute conclusion doit distinguer resultat formel, resultat interne et validation externe.
- Les formulations absolues doivent etre reservees aux resultats effectivement demontres.
- Les blocs qui passent le seuil de reproductibilite locale doivent etre marques comme tels au lieu d'etre presentes comme simples programmes de travail.
- Les blocs deja reproductibles localement doivent figurer dans le coeur etabli du corpus, avec un statut de preuve precise.

## Regles Mathematiques
- Les hypotheses doivent etre explicites.
- Les notations doivent etre definies avant usage.
- Les identites de domaine ou de spectre doivent etre justifiees par double inclusion ou par calcul direct.
- Les arguments de stabilite doivent separer hypothese, conclusion et domaine d'application.

## Regles De Reproductibilite
- Fixer les seeds quand un calcul est numerique.
- Documenter les entrees, les sorties et les conditions d'arret.
- Conserver les artefacts minimaux permettant la re-execution.
- Distinguer ce qui est reproductible localement de ce qui reste a valider externalement.
- Lorsque la reproduction locale est acquise, publier la procedure comme un element etabli du coeur interne, et non comme un simple programme de travail.
- Lorsque la validation externe est engagee, la presenter comme une revue outillee, avec paquet de revue, criteres de sortie et journal des ecarts.
