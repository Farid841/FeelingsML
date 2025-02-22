import mysql.connector
import pandas as pd
import pickle
import os
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from app.evaluate_model import evaluate_model
from app.save_evaluation import save_evaluation_report

# Création des dossiers pour stocker les modèles et matrices de confusion
os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# 🛠 Paramètres configurables
BATCH_SIZE = 5000  # Nombre de tweets à traiter à chaque exécution
USE_DATE = False   # Mettre à True pour filtrer par date au lieu de l'ID
LAST_PROCESSED_FILE = "last_processed.txt"  # Fichier pour stocker l'ID ou la date traitée

# 🔍 Récupération du dernier ID ou de la dernière date traitée
def get_last_processed():
    if not os.path.exists(LAST_PROCESSED_FILE):
        return None
    with open(LAST_PROCESSED_FILE, "r") as f:
        return f.read().strip()

# 📝 Mise à jour du dernier ID ou de la dernière date traitée
def update_last_processed(value):
    with open(LAST_PROCESSED_FILE, "w") as f:
        f.write(str(value))

# 📥 Connexion à MySQL et récupération des données par batchs
def get_data_from_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",
            password="password",
            database="sentiment_analysis"
        )
        last_processed = get_last_processed()

        if USE_DATE:
            # 🔄 Filtrage par date
            query = f"SELECT id, text, positive, negative, date FROM tweet WHERE date > '{last_processed}' ORDER BY date ASC LIMIT {BATCH_SIZE}" if last_processed else f"SELECT id, text, positive, negative, date FROM tweet ORDER BY date ASC LIMIT {BATCH_SIZE}"
        else:
            # 🔢 Filtrage par ID
            query = f"SELECT id, text, positive, negative FROM tweet WHERE id > {last_processed} ORDER BY id ASC LIMIT {BATCH_SIZE}" if last_processed else f"SELECT id, text, positive, negative FROM tweet ORDER BY id ASC LIMIT {BATCH_SIZE}"

        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("⚠ Aucun nouveau tweet à traiter.")
            return None

        # Mise à jour du dernier ID ou date traitée
        last_value = df["date"].iloc[-1] if USE_DATE else df["id"].iloc[-1]
        update_last_processed(last_value)

        return df
    except mysql.connector.Error as e:
        print(f"❌ Erreur de connexion à MySQL : {e}")
        return None

# 🔄 Prétraitement des données avec TF-IDF
def preprocess_data(df):
    df['text'] = df['text'].astype(str).str.lower().str.strip()
    vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)  
    X = vectorizer.fit_transform(df['text']).toarray()
    y_pos = df['positive']
    y_neg = df['negative']
    return X, y_pos, y_neg, vectorizer

# 📈 Entraînement du modèle en batchs
def train_model(X_train, X_test, y_train, y_test, label_type):
    """Train model and evaluate performance"""
    model = LogisticRegression(solver='saga', max_iter=100, warm_start=True, n_jobs=1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Prédit')
    plt.ylabel('Réel')
    plt.title(f'Matrice de confusion - {label_type}')
    filename_cm = f'outputs/confusion_matrix_{label_type}_{datetime.datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(filename_cm)
    print(f"📊 Matrice de confusion sauvegardée : {filename_cm}")

    print(f"\n📋 Performance pour {label_type} :\n")
    print(classification_report(y_test, y_pred))

    # Add evaluation after training
    print(f"\nEvaluating {label_type} model...")
    report = evaluate_model(model, X_test, y_test, label_type)
    print(f"\n{label_type} Model Performance:")
    print(report)
    
    # Save evaluation report
    report_path = save_evaluation_report(y_test, y_pred, label_type)
    print(f"\nEvaluation report saved to: {report_path}")
    
    return model, vectorizer

# 💾 Sauvegarde du modèle
def save_model(model, vectorizer, label_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"models/logistic_regression_{label_name}_{timestamp}.pkl"
    
    with open(filename, 'wb') as f:
        pickle.dump({'model': model, 'vectorizer': vectorizer}, f)

    print(f"💾 Modèle sauvegardé : {filename}")

def train_and_evaluate():
    # 📥 Charger les données depuis la base MySQL
    df = get_data_from_db()
    
    # 🛑 Vérifier si des données ont été récupérées
    if df is None or df.empty:
        print("⚠ Aucune donnée disponible. Arrêt du processus.")
        return 

    X, y_positive, y_negative, vectorizer = preprocess_data(df)
    
    #  Séparation des données en ensembles d'entraînement et de test
    X_train, X_test, y_pos_train, y_pos_test = train_test_split(X, y_positive, test_size=0.2, random_state=42)
    X_train, X_test, y_neg_train, y_neg_test = train_test_split(X, y_negative, test_size=0.2, random_state=42)
    
    # 🚀 Entraînement des modèles
    pos_model = train_model(X_train, X_test, y_pos_train, y_pos_test, "positive")
    neg_model = train_model(X_train, X_test, y_neg_train, y_neg_test, "negative")
    
    # 💾 Sauvegarde des modèles
    save_model(pos_model, vectorizer, "positive")
    save_model(neg_model, vectorizer, "negative")

    # 📝 Évaluation des modèles
    pos_report = evaluate_model(pos_model, X_test, y_pos_test, "Positive")
    neg_report = evaluate_model(neg_model, X_test, y_neg_test, "Negative")
    
    print("\n📊 Positive Sentiment Model Report:")
    print(pos_report)
    print("\n📊 Negative Sentiment Model Report:")
    print(neg_report)

if __name__ == "__main__":
    train_and_evaluate()
    
    # Génération du rapport uniquement si des données ont été traitées
    from app.generate_report import generate_full_report
    try:
        generate_full_report(pos_model, X_test, y_pos_test, "Positive")
        generate_full_report(neg_model, X_test, y_neg_test, "Negative")
    except NameError:
        print("⚠ Aucun modèle généré, le rapport ne sera pas créé.")
