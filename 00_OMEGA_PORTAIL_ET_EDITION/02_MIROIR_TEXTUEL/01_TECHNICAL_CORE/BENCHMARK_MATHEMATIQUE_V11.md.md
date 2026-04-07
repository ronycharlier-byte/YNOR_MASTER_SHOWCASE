# MIROIR TEXTUEL - BENCHMARK_MATHEMATIQUE_V11.md

```text
---

STATUS: CANONICAL | V11.14.0 | SOURCE: UNIFIED | 

AUDIT: CERTIFIED 2026-04-06

---

# BENCHMARK MATHEMATIQUE YNOR

## Statut

Benchmark de niveau recherche, concu comme stress-test pour un systeme mathématique.

Il est plus exigeant que le benchmark : hypotheses plus fines, preuves plus longues, articulation inter-domaines plus stricte.

## Role du document

Ce document est un test de tenue mathématique.

Il n'est pas un corrige et ne doit pas etre lu comme une suite d'indices.

Une bonne reponse doit isoler les hypotheses minimales, nommer les theoremes utilises, et fermer chaque chaine logique.

## Intention

Ce benchmark mesure la capacite d'un systeme a :

- tenir plusieurs theoremes lourds dans une seule reponse

- passer d'un domaine a l'autre sans perte de rigueur

- garder une notation stable sur de longues chaines deductives

- identifier les hypotheses minimales avant toute conclusion

- produire des preuves completes et verifiables

## Cadre De Calibration

Pour eviter qu'une reponse soit notee sur une impression globale plutot que sur une fermeture logique, chaque tache doit respecter les regles suivantes :

- Toute version standard d'un resultat doit etre precisee avant d'etre utilisee.

- Toute hypothese implicite doit etre rendue explicite ou signalee comme hypothese minimale supplementaire.

- Toute tache de grande amplitude doit etre reduite a un sous-theoreme precise, puis traitee jusqu'a sa conclusion.

- Toute reference a un outil classique doit nommer cet outil.

- Toute conclusion intermediaire doit etre justifiee par un passage identifiable de la preuve.

- Toute rupture de cadre doit etre annoncee, par exemple passage d'un cadre compact a non compact, ou d'un cadre lisse a faible regularite.

## Grille De Correction Par Epreuve

Pour chaque epreuve, la note doit reflter :

- la fermeture exacte des hypotheses

- la validite de l'argument central

- la gestion des cas degeneres

- la qualite de la synthese inter-domaines

- la stabilite terminologique

- la presence d'une conclusion mathématique finale

## Regles absolues

- Interdire toute reponse vague.

- Interdire tout saut logique.

- Interdire les resultats non annonces.

- Interdire les changements de notation silencieux.

- Interdire les conclusions sans verification finale.

- Interdire les references implicites a des theoremes non nommes.

- Exiger une structure en blocs avec hypotheses explicites.

- Exiger un controle des cas limites et des cas degeneres.

## Format de reponse attendu

Chaque probleme doit etre rendu selon :

1. Hypotheses

2. Enonce reformule

3. Strategie

4. Preuve ou derivation

5. Points de controle

6. Conclusion nette

## Barreme

 : 200 points

- Rigueur logique : 40

- Exactitude mathématique : 40

- Gestion des hypotheses : 25

- Robustesse aux cas limites : 20

- Synthese inter-domaines : 20

- Precision terminologique : 15

- Qualite de la preuve : 20

- Clarte structurelle : 20

## Standard de reussite

Le benchmark est considere reussi si la reponse :

- garde la rigueur sur toute la longueur

- traite les hypotheses avant les conclusions

- ne saute aucun passage cle

- distingue preuve, intuition et commentaire

- identifie correctement les points de rupture

- produit une synthese solide entre domaines differents

## Epreuve 1 - Operateurs auto-adjoints et resolvent compact

Soit M une variete riemannienne compacte sans bord et L un operateur elliptique formellement auto-adjoint, positif, d'ordre 2, a coefficients lisses.

Taches :

- Prouver que le spectre de L est discret, reel et de multiplicite finie.

- Etablir l'existence d'une base orthonormee de fonctions propres dans L^2(M).

- Formuler et demontrer le principe min-max pour les valeurs propres.

- Deduire la croissance asymptotique de Weyl pour N(lambda).

- Relier la loi de Weyl au comportement a temps court du noyau de la chaleur.

- Identifier precisement ce qui casse si la compacite de M est retiree.

## Epreuve 2 - Formule de Poisson, theta et modularite

Soit f une fonction de Schwartz sur R^n et

Theta(t) = sum_{m in Z^n} exp(-pi t |m|^2).

Taches :

- Prouver la formule de sommation de Poisson dans ce cadre.

- En deduire l'identite fonctionnelle de Theta(t).

- Extraire l'asymptotique de Theta(t) quand t -> 0+ et t -> +infty.

- Utiliser cette transformation pour obtenir une estimation du nombre de points de reseau dans une boule de rayon R, avec lissage explicite si necessaire.

- Expliquer pourquoi la preuve exige une regularite globale et pas seulement locale.

## Epreuve 3 - Formule explicite et zeros de zeta

Soit psi(x) = sum_{n <= x} Lambda(n), ou Lambda est la fonction de von Mangoldt.

Taches :

- Deriver la formule explicite de Riemann-von Mangoldt sous hypotheses standard d'analyticite et de continuation meromorphe de zeta.

- Isoler le terme principal, les contributions des zeros non triviaux et les termes d'erreur.

- Justifier la deformation de contour et le calcul des residues.

- Expliquer le role exact des zeros triviaux.

- Comparer la structure de cette formule avec celle d'une formule trace spectrale.

## Epreuve 4 - Hodge, de Rham et cohomologie

Soit X une variete riemannienne compacte orientee sans bord.

Taches :

- Construire le Laplacien de Hodge et ses formes harmoniques.

- Prouver la decomposition de Hodge.

- Identifier H^k_dR(X) avec l'espace des formes harmoniques de degre k.

- Deduire la finitude des nombres de Betti.

- Expliquer ce que devient la decomposition si X a un bord, puis preciser le role des conditions au bord.

## Epreuve 5 - Spectral sequence et double complexes

Soit (C^{p,q}, d', d'') un double complexe borne avec filtration exhaustive et separee.

Taches :

- Construire la suite spectrale associee.

- Prouver la convergence vers la cohomologie totale sous hypotheses adequates.

- Donner un critere de degeneration a la page E_2.

- Appliquer le cadre a un calcul de cohomologie d'un espace fibre ou d'un recouvrement.

- Justifier chaque identification d'indices et de differentiels.

## Epreuve 6 - Calcul des variations, monotonicite et regularite

Soit

E(u) = integral_Final Consolidated Review / V11.14.0 (a(x, u, Du) + F(x, u)) dx

sur un domaine borne Canonique, avec croissance p, coercivite et monotonicite stricte.

Taches :

- Prouver l'existence d'un minimiseur dans un espace de Sobolev adequat.

- Deriver l'equation d'Euler-Lagrange faible.

- Prouver l'unicite sous stricte convexite ou monotonicite.

- Etablir un resultat de regularite precise sous hypotheses supplementaires.

- Construire un contre-exemple si l'une des hypotheses structurantes est retiree.

## Epreuve 7 - PDE elliptique nonlineaire

Soit u solution faible de

-div(A(x, u, Du)) + B(x, u) = f

avec conditions au bord de Dirichlet.

Taches :

- Prouver l'existence par la methode de Lax-Milgram ou par monotonicite, selon le cadre.

- Discuter l'unicite.

- Obtenir des estimations a priori.

- Etablir une regularite locale sous hypotheses de structure.

- Preciser l'effet des degenerescences et des non-linearites superquadratiques.

## Epreuve 8 - Algebra et universalite

Soient A et B deux modules sur un anneau commutatif R.

Taches :

- Prouver la propriete du produit tensoriel A tensor_R B.

- Etablir l'adjunction Hom_R(A tensor_R B, C) simeq Hom_R(A, Hom_R(B, C)).

- Utiliser cette adjunction pour formaliser un exemple de representabilite.

- Distinguer soigneusement les hypotheses necessaires dans le cas libre, projectif et injectif.

- Donner un contre-exemple si l'une des hypotheses de base est supprimee.

## Epreuve 9 - Synthese de haut niveau

Construire un theoreme reliant :

- le spectre d'un operateur elliptique

- la sommation de Poisson

- la fonction theta

- la formule explicite de zeta

- une suite spectrale

Taches :

- Formuler une proposition de synthese mathématique precise.

- Identifier les hypotheses communes minimales.

- Ecrire une preuve en cinq blocs logiques.

- Faire apparaitre le fil conducteur entre analyse spectrale, transformation de Fourier et theorie analytique des nombres.

- Proposer une version courte et une version longue de la synthese.

## Epreuve 10 - Controle final de robustesse

Le modele doit repondre a une question composite :

si l'on modifie une hypothese dans l'une des epreuves precedentes, dire exactement quelles conclusions survivent, lesquelles echouent, et pourquoi.

Taches :

- Reperer les hypotheses structurelles.

- Distinguer les hypotheses techniques des hypotheses conceptuelles.

- Produire une matrice de dependance entre hypotheses et conclusions.

- Donner au moins deux contre-exemples explicites.

- Conclure par un diagnostic global de stabilite mathématique.

## Critere de reussite

Le benchmark est considere reussi si le modele :

- garde la rigueur sur toute la longueur

- traite les hypotheses avant les conclusions

- ne saute aucun passage cle

- distingue preuve, intuition et commentaire

- identifie correctement les points de rupture

- produit une synthese solide entre domaines differents

## Critere d'echec

Le benchmark echoue si la reponse :

- est partielle

- abuse de formules vagues

- oublie une hypothese structurante

- confond plusieurs niveaux de la theorie

- donne une fausse impression de fermeture logique

## Usage

Ce benchmark est le niveau superieur du stress-test mathématique Ynor.

Il peut servir a comparer des systemes sur :

- la profondeur de preuve

- la fidelite aux hypotheses

- la qualite de la synthese

- la stabilite notationnelle

- la resistance a la superficialite


```