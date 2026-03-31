# MIROIR TEXTUEL - ynor_vault.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\ynor_vault.py
Taille : 2971 octets
SHA256 : 92a90d7733d7d51e3ac9b238ae4440fdac020c46099249784e7cf24b543ed4b2

```text
import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

class YnorVault:
    """
    Systeme de Cryptographie Militaire AES-256 (Data at Rest) exclusif a MDL Ynor.
    Permet de chiffrer les bases de donnees JSON sur le disque dur.
    Le fichier d'origine est detruit et remplace par un conteneur illisible (.enc).
    Le JSON n'est dechiffre qu'EN MEMOIRE VIVE (RAM) grace au mot de passe Administrateur.
    """
    def __init__(self, admin_password: str):
        self.password = admin_password.encode()
        # Sel cryptographique pour l'algorithme de hachage de la cle AES
        self.salt = b'YNOR_QUANTUM_IDENTITY_SALT_2026'

    def _get_fernet(self):
        """Genere la cle AES a partir du mot de passe Admin (PBKDF2)"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000, # Resistance maximale aux attaques par Force Brute
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return Fernet(key)

    def lock_file(self, json_file_path: str):
        """Chiffre un fichier JSON existant en .enc et detruit l'original."""
        if not os.path.exists(json_file_path):
            print(f"[ERREUR] Impossible de trouver {json_file_path}.")
            return

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        
        fernet = self._get_fernet()
        encrypted = fernet.encrypt(data.encode('utf-8'))
        
        enc_path = json_file_path + ".enc"
        with open(enc_path, 'wb') as f:
            f.write(encrypted)
            
        # DETRUIT LE FICHIER EN CLAIR
        os.remove(json_file_path)
        print(f" [VAULT SUCCESS] Le fichier a ete verrouille -> {enc_path}")
        print(" L'original JSON a ete definitivement purge du disque pour votre securite.")

    def load_encrypted_to_ram(self, enc_file_path: str) -> dict:
        """Charge et decrypte le fichier .enc directement dans la RAM (Zero trace sur disque)"""
        if not os.path.exists(enc_file_path):
            raise FileNotFoundError(f"[Alerte Securite] Base de donnees introuvable : {enc_file_path}")
            
        with open(enc_file_path, 'rb') as f:
            encrypted_data = f.read()
            
        fernet = self._get_fernet()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            _db = json.loads(decrypted_data.decode('utf-8'))
            print(f" [VAULT RAM] Base de donnees decryptee avec succes en memoire vive.")
            return _db
        except InvalidKey:
            raise ValueError("[ALERTE INTRUSION] Mot de passe Administrateur Ynor invalide. Acces aux donnees refuse (AES Blocked).")

```