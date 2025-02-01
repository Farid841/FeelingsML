# FeelingsML API with Flask

Ce projet est une API Flask qui analyse les sentiments d'une liste de tweets. Elle retourne un score de sentiment pour chaque tweet et stocke les résultats dans une base de données MySQL.

## Fonctionnalités

- **Analyse des sentiments** : Un endpoint POST `/analyze` qui accepte une liste de tweets et retourne un score de sentiment pour chaque tweet.
- **Stockage des données** : Les tweets analysés sont stockés dans une base de données MySQL.
- **Test de l'API** : Un endpoint GET `/ping` pour vérifier que l'API est opérationnelle.

## Prérequis

- **Python >= 3.9** : Assure-toi d'avoir Python 3.12 installé. L'application est compatible avec les versions de Python à partir de 3.9.
- **Docker** : Pour exécuter l'application et la base de données MySQL dans des conteneurs.

## Installation


### 1. Configurer l'environnement virtuel

Crée un environnement virtuel Python et active-le :

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Sur Linux/Mac
 .\.venv\Scripts\activate  # Sur Windows
```

---

### 3. Installer les dépendances

Installe les dépendances Python nécessaires :

```bash
pip install -r requirements.txt
```

---



## 5. Lancer l'application avec Docker Compose
Assure-toi que Docker est installé et en cours d'exécution sur ta machine.


Utilise Docker Compose pour lancer l'application Flask et la base de données MySQL :

```bash
docker-compose up --build
```

Cela va :
- Construire l'image Docker pour l'application Flask.
- Lancer un conteneur MySQL.
- Exécuter l'application Flask.

Une fois les conteneurs en cours d'exécution, tu peux accéder à l'API Flask à l'adresse suivante :

- **API Flask** : `http://localhost:5000`
