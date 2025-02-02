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


<!-- 

## **Résumé de la réflexion**  (02/02/2025)
🔹 Nous avons récupéré **~80 000 tweets** (Twitter + Reddit).  
🔹 Nous utilisons **40 000 tweets** pour la première phase de tests.  
🔹 Nous devons **nettoyer les données** (supprimer les mots inutiles, emojis, etc.).  
🔹 La division des données permet de **mieux entraîner et tester** le modèle.  
🔹 Nous avons choisi **66% pour l’entraînement** et **33% pour le réentraînement** futur.  
<!-- 🔹 L’objectif final est d’avoir une IA **précise**, **généralisable** et **capable d’évoluer avec le temps**.   -->

-----
## **Comment diviser les données ?**  

Pour entraîner et tester notre modèle, nous devons diviser notre dataset en **plusieurs ensembles** :  
🔹 **Données d’entraînement (Training set)** : utilisées pour apprendre.  
🔹 **Données de test (Test set)** : utilisées pour évaluer le modèle.  
🔹 **Données pour le réentraînement** : utilisées plus tard pour améliorer le modèle.  

---

---


🔹 **Si on veut un modèle classique → 70/30**  
🔹 **Si on a beaucoup de données → 80/20**  
🔹 **Si on veut un modèle très précis → 90/10**  
🔹 **Si on veut réentraîner régulièrement → 66/33**  
🔹 **Si on a un petit dataset → Validation croisée**  
 -->

prochaine etape reflechire a comment integre tous ca techniqument
---