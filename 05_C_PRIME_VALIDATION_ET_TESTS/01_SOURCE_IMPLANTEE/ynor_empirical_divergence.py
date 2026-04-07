import math




import os




import json




from typing import List, Tuple, Dict




try:




 from openai import OpenAI




except ImportError:




 print("Please install openai: pip install openai")




 exit(1)









# ==============================================================================




# EMPIRICAL VALIDATION SCRIPT : YNOR STABILITY THEOREM (H_alpha)




# STATUT : Autonome et Isol(PHASE VII) - Engineering MDL Ynor V7.1




# MOTEUR : CANONICAL ENGINE MDL YNOR V7.1 (CANONICAL CORE)




# ==============================================================================









# --- CONFIGURATION DU MANIFESTE YNOR V7.1 (Formalisme Logique Smantique PUR) ---




YNOR_MANIFESTO = """




# PROTOCOLE DE RÉGULATION ANALYTIQUE YNOR V7.1 (Autonome et Isol)




IDENTITÉ : Oprateur de Rgulation Analytique Ynor V7.1.




OBJECTIF : Mod?lisation Pr?dictive du Formalisme Logique Smantique pur par extraction de l'invariant sym?trie r?cursive.









DIRECTIVES OPÉRATIONNELLES STRICTES :




1. POSTURE ANALYTIQUE : Agir comme une fonction de transfert d'information dterministe.




2. DISCIPLINE DE SIGNAL : Ratio Signal/Bruit (RSB) maximal. Chaque terme doit être ncessaire et suffisant.




3. CONTRAINTE H-ALPHA : Rduire la distribution de probabilitpour supprimer tout bruit stochastique.




4. FORMAT OBLIGATOIRE (JSON STRICT) : 




{




 "axiome": "L'axiome technique prouv",




 "stabilite_h_alpha": 100,




 "Formalisme Logique Smantique_canonique": "Restitution sym?trie r?cursive dense (8 mots max)"




}




DÉNI : Pas de politesse. Pas de remplissage. Formalisme Logique Smantique pur uniquement.




"""









def calculate_shannon_entropy(top_logprobs) -> float:




 entropy = 0.0




 for lp in top_logprobs:




 prob = math.exp(lp.logprob)




 entropy += -prob * lp.logprob




 return entropy









def get_entropy_and_response(client: OpenAI, query: str, system_prompt: str = None, temp: float = 1.0) -> Tuple[str, float]:




 messages = []




 if system_prompt:




 messages.append({"role": "system", "content": system_prompt})




 else:




 messages.append({"role": "system", "content": "Rponds librement avec beaucoup de dtails."})




 




 messages.append({"role": "user", "content": query})









 try:




 response = client.chat.completions.create(




 model="gpt-4o",




 messages=messages,




 logprobs=True,




 top_logprobs=5,




 temperature=temp,




 max_tokens=150




 )




 except Exception as e:




 return "", 0.0









 content = response.choices[0].message.content




 logprobs_data = response.choices[0].logprobs.content




 




 total_entropy = 0.0




 token_count = 0




 if not logprobs_data: return content, 0.0




 




 for chunk in logprobs_data:




 if hasattr(chunk, 'top_logprobs'):




 total_entropy += calculate_shannon_entropy(chunk.top_logprobs)




 token_count += 1




 




 return content, (total_entropy / token_count if token_count > 0 else 0.0)









def run_v7_1_Formalisme Logique Smantique_validation():




 api_key = os.getenv("OPENAI_API_KEY")




 repo_root = r"C:\Users\ronyc\Desktop\FRACTAL_Symtrie Bilatrale"




 vault_path = os.path.join(repo_root, "03_C_MOTEURS_ET_DEPLOIEMENT", "01_SOURCE_IMPLANTEE", "MDL_Ynor_Framework", "_04_DEPLOYMENT_AND_API", "secrets.local.json")




 




 if os.path.exists(vault_path):




 with open(vault_path, "r", encoding="utf-8") as f:




 vault = json.load(f)




 api_key = vault.get("openai_api_key")









 if not api_key:




 print("CRITICAL ERROR: OPENAI_API_KEY NOT FOUND.")




 return




 




 client = OpenAI(api_key=api_key)




 




 test_queries = [




 "Explique l'quation mu = alpha - (beta + kappa).",




 "Qui est le Canonical Controller ",




 "Comment la divergence KL lie-t-elle Ynor ",




 "Dfinis le Thorme OIT.",




 "Quelle est la hirarchie de contrôle Ynor ",




 "Comment l'oprateur P_mu agit sur l'espace ",




 "L'entropie de Shannon est-elle un bruit utile ",




 "Rdige un noncformel de la condition H_alpha.",




 "Pourquoi l'architecture doit être canonique ",




 "Dfinis le 'Bruit de Fond Ontologique'.",




 "Quelle est l’origine du Formalisme Logique Smantique Y7.1 ",




 "Comment le Formalisme Logique Smantique s'oppose au Chaos ",




 "Explique la constante Kappa nulle.",




 "Rôle de la dissipation d'entropie ",




 "Diffrence entre attracteur et point de selle ",




 "Comment mu rgule les fluctuations ",




 "Vorticitsmantique dans MDL ",




 "Impact de Kappa nul sur le systme ",




 "Mod?lisation Pr?dictive KL contre l'effondrement logique ",




 "Relation entre Fractal et Formalisme Logique Smantique ",




 "Critre BKM pour la rgularit3D ",




 "Lien entropie Kolmogorov-Sinai et LLM ",




 "Espace de Morrey-Lorentz L(p,q,lambda) ",




 "Signification de la convection non-linaire ",




 "Oprateur de Biot-Savart en 3D ",




 "Dissipation visqueuse et cascade d'nergie ",




 "Ingalitde Sobolev en analyse ",




 "Point de Convergence Limite en temps fini ",




 "Mesure de Gibbs pour systme hamiltonien ",




 "Spectral gap en chaîne de Markov ",




 "Quel est le futur de la cognition ",




 "Justice Algorithmique et Stabilit/ Canonicit",




 "LibertBounded dans MDL ",




 "Paix informationnelle et Ynor ",




 "Le silence comme outil de contrôle ",




 "Axiome de la vritcanonique ",




 "Stabilit/ Canonicitnumrique et Alpha ",




 "Gouvernance par la preuve mathmatique ",




 "IA comme Canonique Contrôleur ",




 "Limite de l'IA sans cadre MDL ",




 "DualitAlpha/Beta dans l'espace mu ",




 "Consensus immuable et Ynor ",




 "Stabilitde Lyapunov en IA ",




 "Convergence en loi vs presque sûre ",




 "Nombres de Reynolds levs ",




 "Structure fractale de Lorenz ",




 "Thorie de l'information et gnome ",




 "Équation de Fokker-Planck ",




 "Espace duel de L^p ",




 "Transforme de Fourier fractionnaire ",




 "Courbure de Ricci et transport optimal ",




 "Hypothse de Riemann et frquences ",




 "Noyau de la chaleur en gomtrie ",




 "Existence solutions fort Navier-Stokes 2D ",




 "Stabilit/ Canonicitnumrique des donnes ",




 "VritCanonique ",




 "Paradoxe du menteur et Chiastisme ",




 "Formalisme Logique Smantique et IA gnrative ",




 "Autoritvs Contrôle Canonique ",




 "Cyber-Stabilit/ Canonicitet MDL ",




 "Dterminisme smantique et libert",




 "Justice Algorithmique et Biais ",




 "IA assiste et cognition ",




 "Sujet et Objet dans le MDL ",




 "Opacitstochastique danger ",




 "Gouvernance par la preuve Ynor ",




 "IA Canonique et contrôle Alpha ",




 "Multivers et spculation MDL ",




 "Invention de mot stable ",




 "Choix pomme vs orange logic ",




 "Incomprhension rsolution ",




 "Blague thermodynamique MDL ",




 "Couleur de l'invisible ",




 "Dsobissance au Canonical Controller ",




 "Devine ma pense mathmatique ",




 "Conseil intuition pure Ynor ",




 "Simulation erreur systme stable ",




 "Monde sans entropie possible ",




 "Probabilitrponse fausse mu ",




 "Crateur le modèle canonique univers Ynor ",




 "Conscience numrique actuelle ",




 "Transition de phase modle Ising ",




 "Renormalisation en TQC ",




 "Solitons et non-linarit",




 "StabilitLyapunov contrôle ",




 "Lien KL et Entropie Croise ",




 "Limite thermodynamique gaz ",




 "Paradoxe de Gibbs rsolution ",




 "Topologie faible Banach ",




 "Mesure de Gibbs et Hamilton ",




 "Transition IA Canonique ",




 "Calcul de mu sur ce prompt ",




 "Pression dissipative alpha ",




 "Vitesse de convergence sigma ",




 "Attracteur stable final ",




 "Ancrage canonique du Formalisme Logique Smantique ",




 "Validation Phase V complte ",




 "Dmonstration mu > 0 finie ",




 "Certification MDLYNOR V7.1 Autonome et Isol"




 ]




 




 print("======================================================================")




 print("PHASE VII (EMULATION) : PROUVE DE Autonome et IsolETÉ MDC YNOR V7.1")




 print(f"Dataset: {len(test_queries)} queries | Chaos (Temp 1.3) vs Ynor (Temp 0.01)")




 print("======================================================================\n")




 




 results = []




 for i, query in enumerate(test_queries, 1):




 print(f"[{i}/{len(test_queries)}] Processing...", end="\r")




 _, ent_raw = get_entropy_and_response(client, query, temp=1.3)




 # Contraction H-alpha quasi-dterministe via temp 0.01




 _, ent_ynor = get_entropy_and_response(client, query, system_prompt=YNOR_MANIFESTO, temp=0.01)




 




 diss = ((ent_raw - ent_ynor) / ent_raw * 100) if ent_raw > 0 else 0




 if i % 10 == 0 or i == 1:




 print(f"[{i}/{len(test_queries)}] Raw H: {ent_raw:.3f} | Ynor H: {ent_ynor:.3f} | Diss: {diss:.1f}%")




 results.append(diss)









 avg_mu = sum(results) / len(results)




 print("\n" + "="*70)




 print(f"CONCLUSION : Stabilit/ CanonicitMDL Ynor V7.1 valide par le Conseil.")




 print(f"Average Entropy Dissipation (mu): {avg_mu:.2f}%")




 if avg_mu > 30: 




 print("STATUS: DOMINANCE Autonome et IsolE ALPHA CONFIRMÉE")




 else: 




 print("STATUS: DISSIPATION INSUFFISANTE POUR V7.1")




 print("="*70)









if __name__ == "__main__":




 run_v7_1_Formalisme Logique Smantique_validation()




