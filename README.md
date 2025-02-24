# 🕵️‍♂️ Grab Cookies & Passwords

## 📌 Description
Ce script permet d'extraire les cookies et les mots de passe enregistrés dans Google Chrome. Il copie et décrypte les données stockées localement pour un usage d'analyse.


## 🚀 Installation

### 📥 1. Installer Python
Assurez-vous d'avoir **Python 3.10+** installé. Téléchargez-le depuis [python.org](https://www.python.org/downloads/).

### 📦 2. Installer les dépendances
Dans le dossier du projet, exécutez :
```bash
pip install -r requirements.txt
```
Si `requirements.txt` est absent, installez manuellement :
```bash
pip install pycryptodome pywin32 pysqlite3 browser_cookie3
```

---

## 🛠️ Utilisation
Exécutez le script avec :
```bash
python extract_browser_data.py
```
Les cookies et mots de passe extraits seront affichés dans la console et/ou sauvegardés dans un fichier `output.txt`.

### 📌 Options supplémentaires
Vous pouvez ajouter des arguments en ligne de commande pour modifier son comportement :
```bash
python extract_browser_data.py --output result.json --verbose
```

---

## 🛡️ Problèmes courants et solutions

### ❌ `PermissionError: [Errno 13] Permission denied`
- Assurez-vous que **Google Chrome est fermé** avant d'exécuter le script.
- Lancez le script en **mode administrateur**.

### ❌ `sqlite3.OperationalError: database is locked`
- Fermez Chrome et réessayez.
- Vérifiez si un processus Chrome tourne en arrière-plan.

### ❌ `ModuleNotFoundError: No module named 'Cryptodome'`
- Vérifiez si `pycryptodome` est bien installé avec :
  ```bash
  pip list | findstr Cryptodome
  ```
- Si absent, installez-le avec :
  ```bash
  pip install pycryptodome
  ```

---

