# DASHBOARD SPEC

## But
Documenter les surfaces d affichage de `C` afin que le pilotage soit coherent entre l API, le terminal utilisateur et le monitor de viabilite.

## Surfaces Existantes
### Dashboard API natif
- route: `/dashboard`
- rendu HTML genere par `ynor_api_server.py`
- usage: supervision legere et acces humain rapide

### Terminal utilisateur
- fichier: `streamlit_dashboard.py`
- usage: envoi d une requete a `/run`
- affichage: outil utilise, reponse retour environnement, mu et systeme

### Audit mu interactif
- fichier: `app.py`
- usage: comparaison d une baseline LLM et d une execution protegee
- affichage: cout, gain, courbe mu, auto-learning bridge

### Monitor HTML FastAPI
- fichier: `ynor_dashboard_v2.py`
- usage: visualisation de session, courbe mu, logs, rafraichissement periodique
- port observe: `8493`

## Experience Utilisateur Visee
- voir si le moteur est vivant
- voir si la viabilite est bonne
- voir si la requete est coupee a temps
- voir si les logs et l auto-apprentissage sont alimentes

## Blocs Informationnels Attendus
- statut du moteur
- indice mu
- activite des systemes 1 et 2
- historique des appels
- traces de logs recents
- couts ou economies si le dashboard les calcule

## Regles De Presentation
- fond sombre ou contraste
- typographie lisible
- indicateurs numeriques visibles en premier
- couleur positive pour la stabilite
- couleur d alerte pour la divergence

## Regles De Comportement
- le dashboard ne doit pas presenter les secrets
- les donnees sensibles doivent etre masquees
- l auto-refresh ne doit pas saturer le moteur
- le dashboard doit rester utile meme si le backend est partiellement degrade

## Priorite De Construction
1. rendre l etat du moteur lisible
2. rendre la viabilite mu lisible
3. rendre les appels et logs lisibles
4. rendre les ecritures et partages optionnels
