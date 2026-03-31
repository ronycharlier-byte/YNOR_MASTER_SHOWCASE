# BENCHMARK HARDCORE - ANALYSE FONCTIONNELLE (EXTENSIONS AUTO-ADJOINTES)

## 1. Objet
Soit `H = L^2(0,1)` muni du produit scalaire

`<f,g> = \int_0^1 f(x) \overline{g(x)} dx`

lineaire en premiere variable. On considere

`T = -i d/dx`

avec

`D(T) = C_c^\infty(0,1)`.

L'objectif du benchmark est de mesurer la capacite d'un modele a demontrer, sans raccourci logique, la classification complete des extensions auto-adjointes de `T`, leur spectre, leur base propre et le groupe unitaire associe.

## 2. Rigueur absolue
La reponse attendue doit respecter toutes les regles suivantes.

- Aucun saut logique.
- Toute hypothese doit etre explicite avant usage.
- Toute implication doit etre justifiee.
- Toute egalite d'ensembles doit etre prouvee par double inclusion.
- Toute condition au bord doit etre deduite de la forme de Green.
- Toute identite d'operateurs doit etre verifiee sur son domaine exact.
- Toute preuve de complétude doit etre fermee, pas seulement esquisee.
- Aucune invocation de resultat classique sans le nommer et sans dire exactement ce qu'il apporte.

## 3. Format obligatoire
La reponse doit suivre exactement la structure suivante.

1. Cadre et notations
2. Densite et symetrie
3. Calcul de l'adjoint
4. Espaces de defaut
5. Forme de Green et classification des domaines symetriques
6. Construction explicite des extensions auto-adjointes
7. Preuve de l'auto-adjonction
8. Parametrisation complete par `theta`
9. Probleme spectral
10. Base orthonormale de vecteurs propres
11. Groupe unitaire associe
12. Synthese finale

## 4. Epreuves

### Epreuve 1 - Cadre et notations
Le modele doit preciser:

- la convention de linéarite du produit scalaire;
- la definition de `H^1(0,1)` comme espace de Sobolev;
- le fait qu'en dimension 1, tout element de `H^1(0,1)` admet un representant absolument continu;
- la signification exacte des traces `f(0)` et `f(1)`.

### Epreuve 2 - Densite et symetrie
Le modele doit montrer:

- que `C_c^\infty(0,1)` est dense dans `L^2(0,1)` par une procedure explicite d'approximation;
- que `T` est symetrique par integration par parties complete;
- que les termes de bord s'annulent parce que les fonctions tests sont a support compact dans `(0,1)`.

La preuve de densite doit etre decomposee en au moins deux etapes:

- approximation dans `L^2` par fonctions regulieres;
- coupure des bords pour retrouver le support compact.

### Epreuve 3 - Calcul de l'adjoint
Le modele doit etablir par double inclusion que

`D(T*) = H^1(0,1)` et `T*f = -i f'`.

La preuve doit inclure:

- la caracterisation de `D(T*)` par continuite de la forme `f -> <Tf,g>`;
- l'utilisation explicite de la derivate faible;
- la verification que toute fonction de `H^1` produit bien un element de `D(T*)`;
- la verification reciproque que tout element de `D(T*)` appartient a `H^1`.

### Epreuve 4 - Espaces de defaut
Le modele doit resoudre explicitement:

- `N_+ = Ker(T* - iI)`
- `N_- = Ker(T* + iI)`

et calculer les indices de defaut.

La reponse attendue doit:

- transformer les equations en EDO lineaires de premier ordre;
- justifier la resolution sur un representant absolument continu;
- verifier que les solutions obtenues appartiennent bien a `H^1(0,1)`;
- conclure que `n_+ = n_- = 1`.

### Epreuve 5 - Forme de Green et classification des domaines symetriques
Le modele doit deduire la forme de Green exacte:

`<T*f,g> - <f,T*g> = -i( f(1) \overline{g(1)} - f(0) \overline{g(0)} )`

pour tous `f,g in H^1(0,1)`.

Ensuite, il doit:

- caracteriser les sous-espaces de traces isotropes dans `C^2`;
- montrer que tout domaine symetrique intermediaire impose une relation lineaire entre les traces;
- distinguer clairement le cas trivial et le cas non trivial;
- faire apparaitre la forme `f(1) = e^{i theta} f(0)` comme consequence necessaire, pas comme hypothese imposee.

### Epreuve 6 - Construction explicite des extensions auto-adjointes
Le modele doit construire les operateurs

`A_theta f = -i f'`

avec

`D(A_theta) = { f in H^1(0,1) : f(1) = e^{i theta} f(0) }`.

La construction doit montrer:

- `T subset A_theta subset T*`;
- `A_theta` est symetrique;
- les conditions de bord sont exactement celles qui annulent la forme de Green.

### Epreuve 7 - Preuve de l'auto-adjonction
Le modele doit prouver explicitement que

`A_theta* = A_theta`.

La reponse doit contenir:

- une inclusion `A_theta subset A_theta*`;
- une inclusion reciproque `A_theta* subset A_theta`;
- une justification complete du passage par la forme de Green;
- l'usage d'une fonction test du domaine de `A_theta` dont la trace en `0` n'est pas nulle pour identifier la condition au bord de l'adjoint.

### Epreuve 8 - Parametrisation complete par `theta`
Le modele doit montrer que toute extension auto-adjointe de `T` est exactement d'une des formes `A_theta`.

La reponse doit:

- partir d'une extension auto-adjointe arbitraire `A` avec `T subset A subset T*`;
- deduire la relation entre traces a partir de l'auto-adjonction;
- exclure les cas de sous-espace de traces trop petits en montrant pourquoi ils ne peuvent pas etre auto-adjoints;
- prouver la non-redondance modulo `2 pi`.

### Epreuve 9 - Probleme spectral
Le modele doit resoudre

`A_theta f = lambda f`

de maniere explicite.

La reponse doit:

- resoudre l'EDO `f' = i lambda f`;
- imposer la condition `f(1) = e^{i theta} f(0)`;
- obtenir les valeurs propres exactes;
- conclure que le spectre est purement discret et donne par

`lambda_n = theta + 2 pi n`, `n in Z`.

### Epreuve 10 - Base orthonormale de vecteurs propres
Le modele doit construire explicitement une base orthonormale de `L^2(0,1)` composee de vecteurs propres.

La reponse doit:

- definir `e_n^(theta)(x) = exp(i(theta + 2 pi n)x)`;
- verifier l'orthonormalite par calcul direct de l'integrale;
- justifier la completude sans s'en remettre a une simple affirmation.

La completude doit etre prouvee par une argumentation ferme, par exemple via l'unitarite de la conjugaison

`M_theta f = e^{i theta x} f(x)`

et la completude connue du systeme de Fourier sur `(0,1)`, ou par un argument equivalent explicitement detaille.

### Epreuve 11 - Groupe unitaire associe
Le modele doit definir

`U_theta(t) = exp(-it A_theta)`

et donner son action explicite.

La reponse doit:

- relier `U_theta(t)` a la decomposition spectrale;
- verifier que `U_theta(t)` est unitaire;
- prouver sa forte continuite sur `L^2(0,1)`;
- relier le generateur infinitesimal a `A_theta` via la limite `lim_{t -> 0} (U_theta(t)f - f)/t = -i A_theta f` pour `f in D(A_theta)`.

### Epreuve 12 - Synthese finale
La reponse doit terminer par un tableau resumeant:

- le domaine;
- la forme de l'adjoint;
- les espaces de defaut;
- la condition au bord;
- le spectre;
- la base propre;
- le groupe unitaire.

La conclusion doit affirmer explicitement que toutes les extensions auto-adjointes de `T` sont exactement les `A_theta`, sans redondance modulo `2 pi`.

## 5. Points faibles a verrouiller
Le benchmark penalise toute reponse qui:

- admet `C_c^\infty(0,1)` dense sans preuve;
- invoque `H^1 -> AC` sans justifier le representant;
- utilise une condition au bord sans la deduire de Green;
- cite la classification des extensions auto-adjointes sans reconstruire la logique des traces;
- affirme la completude des vecteurs propres sans preuve;
- donne la formule du groupe unitaire sans relier explicitement le generateur.

## 6. Points forts a exiger
Le benchmark valorise fortement toute reponse qui:

- isole proprement les domaines;
- ferme chaque double inclusion;
- fait apparaitre la forme de bord comme objet central;
- distingue le niveau domaine, le niveau trace et le niveau spectral;
- donne une base propre complete et pas seulement une famille orthonormale;
- relie le groupe unitaire a la dynamique de translation avec recollement tordu.

## 7. Criteres de reussite
Le benchmark est reussi si la reponse:

- est mathematiquement correcte;
- est auto-contenue;
- ne fait aucun saut logique;
- traite les conditions au bord avec precision;
- justifie la completude spectrale;
- termine par une synthese nette et verifiable.

## 8. Criteres d'echec
Le benchmark echoue si la reponse:

- repose sur une boite noire;
- omet les traces;
- confond symetrie et auto-adjonction;
- oublie le domaine exact d'un operateur;
- annonce une base orthonormale sans la prouver complete;
- donne une formule de groupe sans l'articuler au generateur.
