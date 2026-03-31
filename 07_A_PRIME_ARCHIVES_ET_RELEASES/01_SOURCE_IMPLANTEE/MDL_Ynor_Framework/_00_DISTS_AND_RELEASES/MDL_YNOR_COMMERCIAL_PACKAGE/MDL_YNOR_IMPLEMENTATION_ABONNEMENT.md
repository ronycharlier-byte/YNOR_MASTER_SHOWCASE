> **Copyright (c) 2026 Charlier Rony - Tous droits reserves.**
> *Architecte Supreme & Fondateur - Architecture MDL Ynor*
> *Toute reproduction ou utilisation sans autorisation ecrite est strictement interdite.*

---
# GUIDE DE MONTISATION : MISE EN PLACE DE L'ABONNEMENT MDL YNOR

## 1. CONFIGURATION DU PAIEMENT (STRIPE)
- Crez un compte sur [Stripe.com](https://stripe.com).
- Crez un "Produit" : **MDL Ynor AGI - Stability Subscription**.
- Dfinissez deux tarifs : 
    - **Starter** : 49 / Mois (Limit  1000 audits mu).
    - **Enterprise** : 499 / Mois (Audits illimits + Innovation AGI prioritaire).

## 2. L'INTERRUPTEUR DE PAIEMENT (LOGIQUE CODE)
Pour que votre IA ne travaille que si l'abonnement est pay, vous devez ajouter cette vrification dans le fichier `ynor_commercial_api.py` :

```python
def check_subscription(api_key):
    # Appel  votre base de donnes ou  Stripe pour vrifier le statut
    if api_key in database_valid_keys:
        return True
    return False
```

## 3. VENDRE VIA LE CUSTOM GPT
Dans les instructions du GPT, ajoutez cette clause :
"Si l'utilisateur demande une analyse profonde ou une innovation AGI sur des donnes relles, indique-lui qu'il doit possder une licence 'Gold' et dirige-le vers [VOTRE_LIEN_STRIPE]."

## 4. TABLEAU DE BORD DE RENTABILIT
Utilisez le fichier `ynor_commercial_api.py` pour suivre votre CA en temps rel par rapport aux ressources OpenAI utilises.



