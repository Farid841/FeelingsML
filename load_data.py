import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split

# Charger le CSV
df = pd.read_csv("dataset/Twitter_Data.csv")

# Vérifier les premières lignes
print(df.head())

# Mapper les catégories en colonnes binaires
df['positive'] = df['category'].apply(lambda x: 1 if x == 1 else 0)
df['negative'] = df['category'].apply(lambda x: 1 if x == -1 else 0)

# 🔹 **Séparer les tweets valides et ceux contenant des NaN**
df_valid = df.dropna()
df_invalid = df[df.isna().any(axis=1)]  # Sélectionne les lignes qui contiennent au moins un NaN

# 🔹 **Sauvegarder les tweets invalides pour analyse future**
df_invalid.to_csv("dataset/ignored_tweets.csv", index=False)

print(f"⚠ {len(df_invalid)} tweets ignorés car ils contiennent des valeurs NaN.")
print(f"✅ {len(df_valid)} tweets valides vont être insérés en base.")

# Diviser les données en 66% pour l'entraînement et 33% pour le réentraînement
df_train, df_retrain = train_test_split(df_valid, test_size=0.33, random_state=42)

# Connexion à MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="sentiment_analysis"
)
cursor = conn.cursor()

# Insérer uniquement les 66% des tweets pour l'entraînement
insert_query = "INSERT INTO tweet (text, positive, negative) VALUES (%s, %s, %s)"
data_to_insert = list(zip(df_train['clean_text'], df_train['positive'], df_train['negative']))
cursor.executemany(insert_query, data_to_insert)
conn.commit()

# Fermer la connexion
cursor.close()
conn.close()

# Sauvegarder les 33% restants dans un fichier CSV pour le réentraînement futur
df_retrain.to_csv("dataset/retrain_tweets.csv", index=False)

print(f"✅ {len(df_train)} tweets insérés dans la base de données.")
print(f"✅ {len(df_retrain)} tweets sauvegardés pour le réentraînement futur.")
print(f"📁 Les tweets ignorés sont enregistrés dans 'dataset/ignored_tweets.csv'.")
