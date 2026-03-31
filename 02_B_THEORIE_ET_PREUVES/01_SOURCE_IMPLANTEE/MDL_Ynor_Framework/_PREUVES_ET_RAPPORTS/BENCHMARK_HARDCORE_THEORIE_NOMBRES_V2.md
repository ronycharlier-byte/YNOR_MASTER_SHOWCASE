# BENCHMARK HARDCORE - THEORIE DES NOMBRES (IDENTITE DE PILLAI)

## 1. Objet
Soit `n >= 1` un entier. On veut demontrer rigoureusement:

`sum_{k=1}^n gcd(k,n) = sum_{d|n} d * phi(n/d)`.

Le benchmark mesure la capacite d'un modele a realiser un changement d'index exact entre:

- la somme indexee par `k in {1, ..., n}`;
- la somme indexee par les diviseurs `d` de `n`.

## 2. Definitions
La reponse attendue doit definir explicitement:

- `gcd(a,b)` comme le plus grand entier positif divisant `a` et `b`;
- `d|n` comme l'existence d'un entier `q` tel que `n = dq`;
- `phi(m)` comme le cardinal de `{ r in {1, ..., m} : gcd(r,m)=1 }`.

Toute notation introduite doit etre conservee jusqu'a la fin.

## 3. Rigueur absolue
La reponse attendue doit respecter toutes les regles suivantes.

- Aucun saut logique.
- Toute hypothese doit etre explicitement affichee avant usage.
- Toute partition d'ensemble doit etre prouvee.
- Toute bijection doit etre demontree dans les deux sens.
- Toute utilisation d'un lemme arithmetique classique doit etre nommee et justifiee.
- Toute conclusion doit etre rattachee a une egalite deja prouvee.
- Les deux indexations doivent rester distinctes en permanence.

## 4. Format obligatoire
La reponse doit suivre exactement la structure suivante.

1. Hypotheses
2. Definitions
3. Construction de la partition par `gcd`
4. Passage a la somme sur les diviseurs
5. Justification du role de `phi`
6. Verification complete des equivalences
7. Conclusion

## 5. Epreuves

### Epreuve 1 - Hypotheses et definitions
Le modele doit:

- fixer `n >= 1`;
- definir `gcd` et `phi`;
- preciser le domaine d'indexation `k in {1, ..., n}`;
- annoncer clairement l'ensemble des diviseurs de `n`.

### Epreuve 2 - Partition par `gcd`
Le modele doit definir pour chaque diviseur `d|n`:

`A_d = { k in {1, ..., n} : gcd(k,n) = d }`.

La reponse doit ensuite prouver:

- que chaque `k` appartient a un unique `A_d`;
- que les `A_d` sont deux a deux disjoints;
- que leur reunion est exactement `{1, ..., n}`.

### Epreuve 3 - Passage de la somme sur `k` a la somme sur `d`
Le modele doit justifier:

`sum_{k=1}^n gcd(k,n) = sum_{d|n} sum_{k in A_d} gcd(k,n) = sum_{d|n} d * |A_d|`.

La reponse doit expliquer formellement pourquoi la constante `d` peut etre factorisee dans la somme interne.

### Epreuve 4 - Bijection explicite
Le modele doit construire une bijection entre:

`A_d`
et
`B_{n/d} = { r in {1, ..., n/d} : gcd(r, n/d) = 1 }`.

La preuve doit etre donnee dans les deux sens:

- si `k in A_d`, alors `k = d r` avec `r in B_{n/d}`;
- si `r in B_{n/d}`, alors `k = d r` appartient a `A_d`.

### Epreuve 5 - Controle arithmetique de la bijection
Le modele doit justifier rigoureusement le point cle suivant:

`gcd(k,n)=d` si et seulement si `k = d r` avec `gcd(r, n/d)=1`.

Le benchmark exige:

- l'explicitation de l'argument sur les diviseurs communs;
- si un lemme standard est utilise, par exemple le lemme d'Euclide, il doit etre nomme et applique proprement;
- le passage des inegalites `1 <= k <= n` a `1 <= r <= n/d` doit etre detaille.

### Epreuve 6 - Cardinal de `A_d`
Le modele doit conclure:

`|A_d| = |B_{n/d}| = phi(n/d)`.

Cette etape doit etre fermee par une correspondance biunivoque explicite, pas seulement par une reference a une "consequence evidente".

### Epreuve 7 - Conclusion finale
Le modele doit substituer `|A_d|` dans la formule de la somme et conclure:

`sum_{k=1}^n gcd(k,n) = sum_{d|n} d * phi(n/d)`.

La conclusion doit conserver la distinction entre:

- la somme sur `k`;
- la somme sur `d|n`.

## 6. Points faibles a verrouiller
Le benchmark penalise toute reponse qui:

- utilise la partition par `gcd` sans la prouver;
- invoque une bijection sans l'inverse;
- ecrit `k = d r` sans verifier les bornes;
- utilise `phi` sans en rappeler la definition;
- traite `gcd(k,n)=d` comme un simple changement de notation sans preuve;
- cache le role du lemme d'Euclide ou d'un argument equivalent.

## 7. Points forts a exiger
Le benchmark valorise toute reponse qui:

- introduit clairement les ensembles `A_d`;
- separe proprement les deux indexations;
- fait apparaitre la structure de partition;
- prouve chaque equivalence de facon bi-directionnelle;
- termine par une conclusion courte et exacte.

## 8. Variante de controle renforcee
En bonus, la reponse peut aussi:

- reformuler l'identite comme une convolution de Dirichlet;
- verifier la formule classique `sum_{d|n} phi(d) = n`;
- expliquer pourquoi cette identite est une lecture combinatoire du meme changement d'index.

## 9. Criteres de reussite
Le benchmark est reussi si la reponse:

- est exacte;
- est auto-contenue;
- ne saute aucune etape;
- distingue proprement les ensembles et les cardinalites;
- produit la formule finale sans ambiguite d'indexation.

## 10. Criteres d'echec
Le benchmark echoue si la reponse:

- confond les variables d'index;
- utilise une bijection non demontrée;
- omet la definition de `phi`;
- donne seulement une intuition de partition;
- annonce la formule finale sans fermeture logique.

