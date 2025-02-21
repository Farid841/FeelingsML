## **Contexte du projet**  
Nous travaillons pour **SocialMetrics AI**, une entreprise fictive spécialisée dans l’analyse des données issues des réseaux sociaux. Notre client, **Daunale Treupe**, souhaite mettre en place un service permettant d’évaluer le sentiment des tweets en fonction de leur contenu.  

### **Objectifs du projet**  
1. Développer une **API Flask** pour traiter les tweets en temps réel et renvoyer une analyse de sentiment (positif ou négatif).  
2. Utiliser un **modèle de machine learning basé sur la régression logistique** pour effectuer ces prédictions.  
3. **Réentraîner régulièrement** le modèle avec de nouvelles données pour améliorer sa précision au fil du temps.  
4. Évaluer la performance du modèle à l’aide d’**indicateurs clés** (précision, rappel, F1-score) et de **matrices de confusion**.  


## **Acquisition des données**  
L’entraînement d’un bon modèle nécessite une **grande quantité de données** pour qu’il puisse apprendre efficacement. Nous avons récupéré **environ 80 000 tweets** grâce à **Kaggle** (merci Kaggle de nous avoir facilité cette étape !) :  
- **40 000 tweets** provenant de Twitter  
- **40 000 commentaires** issus de Reddit  

Ces données nous serviront à entraîner et tester notre modèle d’analyse de sentiment.  

### **Utilisation progressive des données**  
Pour la **première vague de tests**, nous allons utiliser **40 000 tweets uniquement**, afin d’avoir une base de départ sans surcharge de calcul. L’idée est d’utiliser **seulement 1/40k** pour faire des premiers tests et valider la faisabilité du modèle avant de l’affiner avec plus de données.  


## **Pourquoi bien diviser les données ?**  
Un bon modèle d’IA repose d’abord sur **beaucoup de données d’entraînement**, mais ce n’est pas suffisant. Il faut aussi s’assurer qu’il **généralise bien** et ne se contente pas de "mémoriser" les tweets qu’il a déjà vus. C’est là qu’intervient la division des données.  

### **Nettoyage des données**  
Avant de les utiliser, les données doivent être **nettoyées** pour supprimer :  
✅ **Les mots inutiles** (a, the, and…) qui n’apportent rien au sens global du tweet.  
✅ **Les caractères spéciaux**, les hashtags, les emojis, et autres éléments qui peuvent biaiser l’analyse.  
✅ **Les doublons**, afin d’éviter que le modèle surapprenne certaines expressions trop présentes.  

### **Pourquoi diviser les données en plusieurs ensembles ?**  
La division des données en plusieurs groupes permet de :  

1️⃣ **Entraîner le modèle** :  
- Le modèle apprend les **motifs et structures des tweets** pour différencier les sentiments positifs et négatifs.  
- Ex : Un tweet comme *"J'adore cette journée ! 😊"* sera étiqueté **positif**, et un tweet comme *"Cette journée est horrible 😡"* sera **négatif**.  

2️⃣ **Évaluer le modèle** :  
- Après l'entraînement, il faut tester le modèle sur des tweets **qu'il n'a jamais vus** pour vérifier qu'il ne fait pas d’erreurs.  
- Ex : Si on donne le tweet *"Ce produit est trop cher pour sa qualité"* et que le modèle le classe **positif**, cela signifie qu’il ne comprend pas bien le contexte.  

3️⃣ **Éviter le surapprentissage (overfitting)** :  
- Si on entraîne le modèle **uniquement sur les tweets qu’il connaît**, il risque d’apprendre "par cœur" au lieu de **comprendre réellement**.  
- Ex : Un étudiant qui mémorise toutes les réponses d’un examen d’entraînement mais qui échoue quand on lui pose une nouvelle question.  


## **Comment diviser les données ?**  
Pour entraîner et tester notre modèle, nous devons diviser notre dataset en **plusieurs ensembles** :  
🔹 **Données d’entraînement** (Training set) : utilisées pour apprendre.  
🔹 **Données de test** (Test set) : utilisées pour évaluer le modèle.  
🔹 **Données pour le réentraînement** : utilisées plus tard pour améliorer le modèle.  

### **Choix du pourcentage de division**  
Il existe plusieurs stratégies de répartition des données , chacune avec ses avantages et inconvénients. 


### **1️⃣ 70% entraînement / 30% test** (*méthode classique*)
---
📌 **Principe** :  
- 70% des tweets servent à entraîner le modèle.  
- 30% sont gardés pour tester sa performance.  

✅ **Avantages** :  
✔ Bonne répartition entre apprentissage et évaluation.  
✔ Permet une estimation fiable des performances du modèle.  
✔ Convient aux datasets de taille moyenne.  

❌ **Inconvénients** :  
✘ Peut être insuffisant pour un entraînement optimal si le dataset est trop petit.  
✘ Une répartition fixe ne prend pas en compte les évolutions des données.  

🔍 **Exemple** :  
Imaginons un modèle de classification de sentiments sur Twitter. Si nous avons **10 000 tweets**, alors **7 000** serviront à entraîner le modèle et **3 000** à le tester. Si les tendances sur Twitter changent rapidement, les **30% de test peuvent devenir obsolètes** après un certain temps.  


### **2️⃣ 80% entraînement / 20% test** (*si on a beaucoup de données*)  
---
📌 **Principe** :  
- On maximise l’apprentissage (80%).  
- On garde un test fiable (20%).  

✅ **Avantages** :  
✔ Plus de données pour l’apprentissage, donc un modèle potentiellement plus performant.  
✔ Toujours une bonne évaluation avec 20% de test.  

❌ **Inconvénients** :  
✘ Moins de données pour tester peut donner une évaluation légèrement moins précise.  
✘ Risque de surentraînement (overfitting) si les 80% sont trop homogènes.  

🔍 **Exemple** :  
Si nous avons **100 000 tweets**, **80 000** seront utilisés pour entraîner le modèle et **20 000** pour l’évaluer. Cette approche est particulièrement utile si nous avons des données variées et en grande quantité.  


### **3️⃣ 90% entraînement / 10% test** (*optimisation maximale de l’apprentissage*)  
---
📌 **Principe** :  
- 90% des données pour entraîner le modèle.  
- 10% seulement pour évaluer.  

✅ **Avantages** :  
✔ Idéal si on a un grand dataset et qu’on veut maximiser l’apprentissage.  
✔ Peut améliorer la précision du modèle sur de nouvelles données.  

❌ **Inconvénients** :  
✘ Peu de données pour tester → risque d’une évaluation peu fiable.  
✘ Risque d’overfitting car le modèle est trop optimisé pour l’ensemble d’entraînement.  

🔍 **Exemple** :  
Si nous avons **1 million de tweets**, nous utilisons **900 000** pour l’entraînement et seulement **100 000** pour le test. Cela permet d’entraîner un modèle puissant, mais nous avons moins de recul sur ses performances réelles.  


### **4️⃣ 66% entraînement / 33% pour réentraînement** (*notre choix*)  
---
📌 **Principe** :  
- 66% des données pour l’entraînement initial.  
- 33% des données mises de côté pour être utilisées plus tard comme nouvelles données de réentraînement.  

✅ **Avantages** :  
✔ Permet d’entraîner le modèle sur des données récentes.  
✔ Offre la possibilité de réentraînement avec des nouvelles données au fil du temps.  
✔ S’adapte aux tendances changeantes (ex. nouvelles expressions sur Twitter).  

❌ **Inconvénients** :  
✘ Au départ, on teste avec les mêmes données d’entraînement.  
✘ On doit attendre pour utiliser les données mises de côté, ce qui peut ralentir l’amélioration immédiate du modèle.  

🔍 **Exemple** :  
- On **cache 10 000 tweets**comme s'ils n'existaient pas.
- On utilise les **30 000 tweets restants** pour entraîner et valider le modèle.
- Une fois satisfait, on **réintègre les 10 000 tweets cachés** pour tester si le modèle généralise bien sur ces nouvelles données.


### **5️⃣ Validation croisée (Cross-Validation)**  
---
En plus de la division classique, nous pouvons utiliser une **validation croisée** pour mieux évaluer notre modèle.  

📌 **Principe** :  
On divise les données en plusieurs **sous-ensembles** et on entraîne plusieurs modèles en utilisant chaque sous-ensemble comme test à tour de rôle.  

✅ **Avantages** :  
✔ Permet une meilleure évaluation du modèle en utilisant toutes les données.  
✔ Réduit les biais de division fixe (ex. si les données sont mal réparties).  
✔ Utile surtout pour les petits datasets.  

❌ **Inconvénients** :  
✘ Plus coûteux en calculs → prend plus de temps.  
✘ Pas toujours nécessaire si on a beaucoup de données.  

🔍 **Exemple** :  
Avec une validation croisée **5-fold**, on divise les **10 000 tweets** en **5 groupes de 2 000 tweets**. On entraîne 5 modèles, chacun utilisant 4 groupes pour l’entraînement et 1 groupe pour le test, puis on fait la moyenne des performances.  
 

### **tableau recapitulatif : quel choix adopter ?**  

| Méthode                  | Avantages | Inconvénients | Idéal pour |
|-------------------------|-----------|--------------|------------|
| **70% entraînement / 30% test** | Bon équilibre entre apprentissage et test | Risque de ne pas capturer les évolutions des données | Datasets moyens |
| **80% entraînement / 20% test** | Plus d’apprentissage sans trop réduire l’évaluation | Légèrement moins fiable pour le test | Datasets volumineux |
| **90% entraînement / 10% test** | Maximisation de l’apprentissage | Test moins fiable, risque d’overfitting | Très grands datasets |
| **66% entraînement / 33% réentraînement** | Permet une adaptation continue du modèle | Nécessite un suivi régulier | Modèles évolutifs (ex. Twitter) |
| **Validation croisée** | Meilleure évaluation | Plus long à calculer | Petits datasets |

🚀 **Dans notre cas, nous avons choisi la répartition 66% / 33%** pour garantir un modèle qui **s’améliore dans le temps** et suit les évolutions du langage sur Twitter.


## **Explication du fichier `load_data.py`**

Le fichier `load_data.py` est responsable du **chargement, du nettoyage et de l'insertion des tweets dans la base de données MySQL**. Avant d'entraîner notre modèle, nous devons nous assurer que les données sont correctement structurées et prêtes à être exploitées.

### **📌 Étapes réalisées dans `load_data.py` :**

1️⃣ **Chargement des données brutes** 🔄
- Le fichier CSV `Twitter_Data.csv`, situé dans le dossier `dataset/`, est chargé avec **Pandas** (l'outil qui facilite la manipulation des données... contrairement à JavaScript qui préfère les transformer en chaos 🤡 t'es pas d'accord ? 

```js
  console.log('5' + 5); // Résultat : '55' 😵‍💫
  console.log('5' - 5); // Résultat : 0 🤯
  ```
bref..).

2️⃣ **Nettoyage des données** 🧹
- Suppression des lignes contenant des valeurs `NaN`.
- Conversion des colonnes catégoriques :
  - La colonne `category` contient une valeur unique (-1 pour négatif, 0 pour neutre, 1 pour positif).
  - La base de données MySQL a **deux colonnes distinctes** (`positive` et `negative`), donc nous devons transformer `category` en ce format binaire.

3️⃣ **Séparation des données en deux ensembles** 📊
- **66% des données** sont insérées immédiatement dans la base MySQL pour entraîner le modèle.
- **33% des données** sont mises de côté dans `dataset/retrain_tweets.csv` pour améliorer le modèle plus tard.

4️⃣ **Insertion dans MySQL** 🗄️
- Connexion à la base de données.
- Insertion des données nettoyées dans la table `tweets`.
- Enregistrement des données restantes pour un réentraînement futur.

📌 **Visualisation du traitement des données :**
![Résultat du script `load_data.py`](/assets/output_load_data.png)


## **Optimisation de la base de données** 🚀

Pour accélérer les recherches et optimiser l'accès aux données, nous avons **ajouté des index** dans notre modèle et dans le script de migration SQL (`init.sql`).

📌 **Améliorations apportées :**
- **Indexation de la colonne `text`** 📜 pour accélérer les recherches textuelles.
- **Indexation des colonnes `positive` et `negative`** ✅❌ pour optimiser les requêtes filtrant les sentiments.

Ces optimisations permettent à l'API d'être **plus rapide et plus efficace** lors de l'analyse des sentiments.


## **Relation entre le script d'entraînement et l'API Flask** 🔄

Nous avons identifié une relation directe entre le **script d'entraînement** (`train_initial_model.py`) et l'**endpoint `/analyze`** de l'API Flask.

### 📌 **Le script d'entraînement (`train_initial_model.py`) :**
- 📥 **Charge les tweets annotés** depuis MySQL.
- 🎯 **Entraîne un modèle de régression logistique** pour classer les tweets en positifs et négatifs.
- 💾 **Sauvegarde le modèle et le vectorizer** pour être utilisé plus tard par l'API.

### 📌 **L'endpoint `/analyze` dans Flask :**
- 📂 **Charge le modèle pré-entraîné** depuis les fichiers sauvegardés.
- 🔢 **Transforme les tweets en vecteurs numériques** avec `vectorizer`.
- 🔍 **Effectue une prédiction** du sentiment pour chaque tweet.
- 📤 **Retourne les résultats au format JSON**.

Grâce à cette architecture, nous pouvons **analyser des tweets en temps réel** avec un modèle mis à jour régulièrement.

---

## **Amélioration du schéma de la base de données** 🛠️

Afin d'éviter des pertes de données et d'améliorer la visibilité, nous avons **modifié le schéma de la base de données** :

✅ **Ajout d'une table `data_log`** pour stocker toutes les entrées et sorties du modèle.  
✅ **Ajout d'une gestion des transactions** pour permettre un **rollback** en cas d'erreur lors d'un entraînement.
✅ **Meilleure gestion des logs** pour tracer **quand** et **comment** les données ont été utilisées.

Grâce à ces améliorations, notre base de données devient **plus robuste**, ce qui permet de garantir un suivi des modifications et une meilleure fiabilité du modèle.

## Explication du script `train_model.py`

### **🚀 Objectif du script**
Le script `train_model.py` est conçu pour **entraîner un modèle de machine learning** capable d'analyser le sentiment des tweets enregistrés en base de données. Cependant, étant donné la grande quantité de données (~120K tweets), **il est optimisé pour fonctionner par petits lots (batches)** afin de **préserver la mémoire et éviter le crash de la machine (c'est ce qui m'est arrivé )**.

### **🔧 Fonctionnalités principales**
✅ Chargement des données depuis MySQL **par petits paquets (batch processing)**
✅ Nettoyage des tweets **au fur et à mesure** (pas de chargement massif en mémoire)
✅ Vectorisation des tweets avec **TF-IDF** sur chaque batch
✅ Entraînement du modèle par **mini-batchs** pour limiter l’utilisation de RAM
✅ Reprise automatique en cas d’arrêt (enregistre le dernier tweet traité)
✅ Sauvegarde des modèles entraînés pour les réutiliser plus tard


### **📂 Étapes détaillées du script**

#### **1️⃣ Chargement des tweets en petits paquets (batch processing)**
Plutôt que de charger **120K tweets d'un coup**, le script :
- Récupère **un petit lot de tweets (ex: 5000)** à la fois depuis MySQL.
- Utilise l’ID ou la date du dernier tweet traité pour reprendre là où il s'était arrêté.

#### **2️⃣ Nettoyage et vectorisation des données à la volée**
Chaque lot de tweets est immédiatement :
- Nettoyé (**passé en minuscules, suppression des espaces, etc.**)
- Converti en vecteurs numériques avec **TF-IDF** (**max_features=2000** pour limiter la mémoire)
- Préparé pour l’entraînement **sans être stocké en mémoire**

#### **3️⃣ Entraînement du modèle avec mini-batchs**
- Chaque batch de tweets est traité **indépendamment**
- L’entraînement se fait **progressivement** avec `warm_start=True`
- Utilisation de `solver='saga'` pour permettre un **entraînement en mini-batchs**

#### **4️⃣ Reprise automatique après arrêt**
- Le script enregistre le **dernier tweet traité** dans un fichier `last_processed.txt`
- Si le script est interrompu, il reprend à partir du dernier tweet sans recommencer depuis le début

#### **5️⃣ Sauvegarde des modèles après chaque batch**
- Les modèles sont enregistrés **après chaque lot traité** pour éviter toute perte
- Sauvegarde dans `models/logistic_regression_positive.pkl` et `models/logistic_regression_negative.pkl`

---

### **🔄 Optimisation : Mini-batchs et gestion de la mémoire**

| 🔧 Problème | 🚀 Solution |
|------------|------------|
| **Trop de tweets chargés en mémoire** | Chargement en **batches de 5000 tweets** |
| **Vectorisation trop lourde** | Réduction des features **(max_features=2000)** |
| **CPU surchargé** | Mini-batchs avec `solver='saga'` et `n_jobs=1` |
| **RAM saturée** | Entraînement **progressif avec warm_start=True** |
| **Script qui redémarre de zéro** | Reprise **depuis le dernier tweet traité** |

---

### **📌 Exécution du script**

### **💡 Avant de lancer l'entraînement**
1. Vérifier si des données existent en base de données :
   ```sql
   SELECT COUNT(*) FROM tweet;
   ```
   Si `0`, exécuter d'abord `load_data.py` pour ajouter des tweets.

2. Modifier la taille du batch (optionnel) :
   Dans le script, changer cette ligne :
   ```python
   BATCH_SIZE = 5000  # Augmenter ou réduire selon les performances
   ```

### **🚀 Lancer l'entraînement du modèle**
```bash
python3 train_model.py
```

### **📊 Vérifier les modèles sauvegardés**
Après l'entraînement, vérifier que les fichiers sont bien créés :
```bash
ls models/
```
Devrait afficher :
```
logistic_regression_positive.pkl
logistic_regression_negative.pkl
```
matrice de confusion  positive
![Matrix de confusion positive `load_data.py`](/outputs/confusion_matrix_positive_20250221.png)

matrix de confusion negative:
![Matrix de confusion positive `load_data.py`](/outputs/confusion_matrix_negative_20250221.png)

