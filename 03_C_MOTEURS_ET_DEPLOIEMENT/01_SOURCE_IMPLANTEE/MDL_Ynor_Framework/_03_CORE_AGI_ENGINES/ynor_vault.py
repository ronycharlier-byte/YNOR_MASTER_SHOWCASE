import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

class YnorVault:
    """
    Système de Cryptographie Militaire AES-256 (Data at Rest) exclusif à MDL Ynor.
    Permet de chiffrer les bases de données JSON sur le disque dur.
    Le fichier d'origine est détruit et remplacé par un conteneur illisible (.enc).
    Le JSON n'est déchiffré qu'EN MÉMOIRE VIVE (RAM) grâce au mot de passe Administrateur.
    """
    def __init__(self, admin_password: str):
        self.password = admin_password.encode()
        # Sel cryptographique pour l'algorithme de hachage de la clé AES
        self.salt = b'YNOR_QUANTUM_IDENTITY_SALT_2026'

    def _get_fernet(self):
        """Génère la clé AES à partir du mot de passe Admin (PBKDF2)"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000, # Résistance maximale aux attaques par Force Brute
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return Fernet(key)

    def lock_file(self, json_file_path: str):
        """Chiffre un fichier JSON existant en .enc et détruit l'original."""
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
            
        # DÉTRUIT LE FICHIER EN CLAIR
        os.remove(json_file_path)
        print(f"🔒 [VAULT SUCCESS] Le fichier a été verrouillé -> {enc_path}")
        print("⚠️ L'original JSON a été définitivement purgé du disque pour votre sécurité.")

    def load_encrypted_to_ram(self, enc_file_path: str) -> dict:
        """Charge et décrypte le fichier .enc directement dans la RAM (Zéro trace sur disque)"""
        if not os.path.exists(enc_file_path):
            raise FileNotFoundError(f"[Alerte Sécurité] Base de données introuvable : {enc_file_path}")
            
        with open(enc_file_path, 'rb') as f:
            encrypted_data = f.read()
            
        fernet = self._get_fernet()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            _db = json.loads(decrypted_data.decode('utf-8'))
            print(f"🔓 [VAULT RAM] Base de données décryptée avec succès en mémoire vive.")
            return _db
        except InvalidKey:
            raise ValueError("[ALERTE INTRUSION] Mot de passe Administrateur Ynor invalide. Accès aux données refusé (AES Blocked).")
