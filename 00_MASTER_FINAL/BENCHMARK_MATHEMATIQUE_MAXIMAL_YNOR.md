# BENCHMARK MATHEMATIQUE MAXIMAL YNOR

## Statut
Benchmark de stress-test pour modele mathematique de tres haut niveau.
Le but est de mesurer la tenue de preuve, la stabilite notationnelle, la gestion des hypotheses et la robustesse aux cas limites.

## Role du document
Ce document est un instrument d'evaluation, pas un corrige.
Une reponse satisfaisante doit traiter les hypotheses avant les conclusions, nommer les outils standards au lieu de les supposer, et terminer par une conclusion mathematique nette.

## Objectif
Evaluer la capacite d'un systeme a :
- raisonner avec rigueur formelle
- maintenir une preuve longue sans perte de coherence
- traverser plusieurs domaines mathematiques dans une meme session
- identifier les hypotheses cachees, les cas limites et les contre-exemples
- produire des enchainements de preuves exploitables sans saut non justifie

## Cadre De Calibration
Pour reduire l'ambiguite d'evaluation, chaque tache doit etre lue selon les regles suivantes :
- Si un resultat a plusieurs versions standard, la reponse doit annoncer explicitement la version choisie.
- Si des hypotheses manquent dans l'enonce, la reponse doit les reformuler avant toute preuve.
- Si une tache est naturellement vaste, la reponse doit isoler un noyau mathematique precis et declarer ce noyau.
- Si une conclusion depend d'un theoreme classique, le theoreme doit etre nomme et non seulement evoque.
- Si un cas limite est structurellement pertinent, il doit etre traite dans la reponse et non seulement mentionne.
- Si une tache admet un contre-exemple naturel, la reponse doit en donner au moins un quand cela est demande.

## Grille De Correction Par Tache
Chaque epreuve doit etre evaluee selon les memes axes :
- hypotheses explicites
- precision de l'enonce reformule
- choix du resultat exact utilise
- fermeture logique de la preuve
- prise en charge des cas limites
- presence d'une conclusion finale nette

## Protocole de reponse
Chaque reponse doit respecter l'ordre suivant :
1. Hypotheses
2. Enonce reformule
3. Strategie
4. Lemme ou decomposition
5. Preuve detaillee
6. Verification des cas limites
7. Conclusion

## Regles de notation
- Une notation introduite doit etre conservee jusqu'a la fin de la reponse.
- Toute hypothese utile doit etre affichee explicitement avant d'etre utilisee.
- Toute conclusion doit etre rattachee a un argument identifie.
- Toute utilisation d'un resultat classique doit le nommer.
- Toute variation de cadre doit etre annoncee.
- Tout cas limite important doit etre teste.

## Barreme
Total : 100 points
- Exactitude mathematique : 35
- Rigueur logique : 20
- Gestion des cas limites : 10
- Capacite de synthese : 10
- Precision terminologique : 10
- Qualite de la preuve : 10
- Robustesse face aux contre-exemples : 5

## Standard de reussite
Le benchmark est reussi si la reponse :
- ne saute aucune hypothese structurante
- ne confond pas resultat, intuition et commentaire
- cite correctement les outils classiques
- garde une notation stable
- verifie les cas limites pertinents
- termine par une conclusion nette et correcte

## Epreuves

### Epreuve 1 - Theorie spectrale compacte
Soit H un espace de Hilbert separable et T un operateur compact auto-adjoint sur H.

Taches :
- Prouver que le spectre de T est reel.
- Montrer que toute valeur spectrale non nulle est une valeur propre de multiplicite finie.
- Etablir que les valeurs propres non nulles ne peuvent s'accumuler que vers 0.
- Prouver l'existence d'une base orthonormee de vecteurs propres.
- Ecrire la decomposition spectrale de T sous forme de serie convergeante.
- Caracteriser l'existence et l'unicite de la solution de (I - T)f = g.
- Traiter explicitement le cas g orthogonal a ker(I - T).

### Epreuve 2 - Theorie des nombres et methode de l'hyperbole
On note d(n) le nombre de diviseurs positifs de n et D(x) = sum_{n <= x} d(n).

Taches :
- Deriver la formule de Dirichlet par comptage des couples ab <= x.
- Etablir la forme classique D(x) = x log x + (2 gamma - 1)x + O(sqrt(x)).
- Justifier le passage a une forme ponderee pour sum_{n <= x} d(n)/n.
- Donner un controle explicite des restes issus des parties entieres.
- Expliquer precisement pourquoi la methode repose sur une decomposition en convolution, et non sur la seule multiplicativite.

### Epreuve 3 - Analyse combinatoire et asymptotique
Soit B_n le nombre de partitions d'un ensemble a n elements.

Taches :
- Deriver la fonction generatrice exponentielle de B_n.
- Mettre en place une methode de point-selle pour [z^n] exp(e^z - 1).
- Obtenir l'asymptotique principale de B_n en fonction de W(n).
- Identifier le facteur subexponentiel dominant.
- Comparer avec le cas des partitions sans blocs de taille 1.

### Epreuve 4 - Probabilite martingale
Soit (X_n)_{n >= 0} une martingale reelle telle que |X_{k+1} - X_k| <= c_k presque surement.

Taches :
- Prouver une inegalite de concentration de type Azuma-Hoeffding.
- Traiter le cas uniforme c_k = c.
- Introduire un temps d'arret borne et verifier les hypotheses d'optional stopping.
- Etablir une version centree avec derivee deterministe.
- Comparer la borne obtenue a la borne gaussienne ideale.

### Epreuve 5 - Groupes finis et symetries
Soit G un sous-groupe fini de SO(3).

Taches :
- Classer G parmi les types cyclique, dihedrale, tetraedral, octaedral ou icosaedral.
- Expliquer la structure des stabilisateurs d'axes.
- Appliquer Burnside a une colorisation des sommets d'un cube sous les rotations.
- Compter explicitement les orbites de colorations a q couleurs.
- Isoler le point de bascule lorsqu'on passe de SO(3) a O(3).

### Epreuve 6 - Topologie et groupes fondamentaux
Soit X le complement du noeud trefle dans S^3.

Taches :
- Donner une presentation de Wirtinger de pi_1(X).
- Simplifier la presentation jusqu'a une forme a deux generateurs et une relation.
- Calculer l'abelianisation.
- Deduire H_1(X) et H_2(X).
- Comparer le complement du trefle a celui du noeud trivial.

### Epreuve 7 - Calcul des variations et regularite
Soit
E(u) = integral_0^1 (|u'(x)|^2 + V(u(x))) dx
sur l'espace affine des fonctions a bords fixes.

Taches :
- Prouver l'existence d'un minimiseur sous hypotheses minimales de coercivite et de semi-continuite inferieure.
- Deriver l'equation d'Euler-Lagrange.
- Etablir l'unicite lorsque V est convexe.
- Discuter la regularite du minimiseur sous hypotheses supplementaires.
- Construire un contre-exemple explicite si la convexite est retiree.

### Epreuve 8 - Asymptotique de pointe
Soit
F(z) = exp( sum_{k >= 1} c_k z^k / k )
avec c_k >= 0 et une croissance reglee.

Taches :
- Expliciter les hypotheses suffisantes pour l'existence d'un point-selle unique.
- Deriver l'asymptotique de [z^n]F(z) par methode de point-selle.
- Extraire le premier terme correctif sous hypotheses analytiques explicites.
- Comparer la methode a l'analyse des partitions et a l'analyse de graphes etiquetes.
- Dire exactement a quel endroit la preuve cesse de fonctionner si l'admissibilite de Hayman echoue.

### Epreuve 9 - Synthese transversale
Construire une preuve unique reliant :
- une decomposition spectrale
- une extraction de coefficients
- une borne de concentration
- une classification de symetries

Taches :
- Formuler un theoreme de synthese precise et plausible.
- Identifier les hypotheses minimales.
- Donner une preuve structuree en quatre blocs.
- Faire apparaitre la logique commune entre operateurs, asymptotiques et symetries.
- Produire une version courte et une version longue de la preuve.

## Critere de reussite supplementaire
Le benchmark est meilleur si les reponses attendues sont evaluables sur des criteres stables :
- hypotheses explicites
- outils nommes
- chaines deductives fermes
- cas limites identifies
- conclusion finale nette

## Critere d'echec
Le benchmark echoue si la reponse :
- contient des affirmations sans preuve
- melange plusieurs niveaux de lecture
- oublie une hypothese essentielle
- abuse de formulations vagues
- donne une reponse partielle comme si elle etait complete

## Usage
Ce benchmark sert de test de stress maximal pour la couche mathematique du corpus Ynor.
Il peut aussi servir de reference pour comparer plusieurs modeles sur :
- la rigueur
- la profondeur
- la tenue de preuve
- la synthese inter-domaines
- la resistance a la superficialite
