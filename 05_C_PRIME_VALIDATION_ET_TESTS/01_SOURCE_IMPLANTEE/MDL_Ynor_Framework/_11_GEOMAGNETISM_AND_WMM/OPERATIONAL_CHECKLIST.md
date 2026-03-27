# Check-list Opérationnelle : Gestion de la Dérive Magnétique

## 1. Détection et Veille
- [ ] Programmer des requêtes automatiques au modèle WMM (ou WMMHR / HDGM) pour les emplacements critiques (Aéroports, sites de forage).
- [ ] Définir un seuil d'alerte : Changement de déclinaison cumulative ≥ 1° depuis la dernière mise à jour.
- [ ] Détecter le point de bascule de l'arrondi (±5° par rapport à la dizaine la plus proche) pour les numéros de piste.

## 2. Infrastructure et Pistes (Aéronautique)
- [ ] Renommer les pistes : Mise à jour de la peinture au sol (Chiffres et Lettres L/R/C).
- [ ] Remplacer les panneaux indicateurs de direction (Signage).
- [ ] Mettre à jour les documents OACI / FAA et les cartes d'approche d'aéroport (AIP).
- [ ] Diffuser un NOTAM (Notice to Airmen) informant du changement de nom de piste.

## 3. Systèmes et Logiciels (Nav / GPS)
- [ ] Injecter la dernière API NOAA WMM dans le backend des applications de navigation mobile.
- [ ] Mettre à jour les bases de données d'inflexion magnétique dans les systèmes embarqués (Avions, Bateaux, Sous-marins).
- [ ] Prévoir des mécanismes de correction en temps réel (HDGM 2026) pour les perturbations atmosphériques et boréales.

## 4. Surveillance des Vulnérabilités (SAA)
- [ ] Renforcer le blindage des satellites lors du survol de l'Anomalie de l'Atlantique Sud (SAA).
- [ ] Programmer des arrêts temporaires des détecteurs sensibles (Télescopes, capteurs photoniques) dans la zone SAA.
- [ ] Surveiller les erreurs de bus données et les "bit flips" sur les composants CMOS à basse orbite (ISS).

## 5. Impact Écologique et Biologique
- [ ] Informer les équipes de conservation de la faune sur les risques de désorientation migratoire.
- [ ] Surveiller les comportements anormaux chez les espèces utilisant la magnétite (Baleines, tortues, saumons, oiseaux).
- [ ] Adapter les interventions expérimentales (e.g. retrait d'aimants artificiels sur la faune locale).
