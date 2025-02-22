import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from datetime import datetime
import os


def plot_confusion_matrix(y_true, y_pred, label_type):
    """Generate and save confusion matrix plot"""
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {label_type}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')

    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)

    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    plt.savefig(
        f'outputs/confusion_matrix_{label_type.lower()}_{timestamp}.png')
    plt.close()


def evaluate_model(model, X_test, y_test, label_type):
    """Evaluate model and generate metrics"""
    # Make predictions
    y_pred = model.predict(X_test)

    # Generate confusion matrix
    plot_confusion_matrix(y_test, y_pred, label_type)

    # Generate classification report
    report = classification_report(y_test, y_pred)

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d")
    with open(f'outputs/classification_report_{label_type.lower()}_{timestamp}.txt', 'w') as f:
        f.write(report)

    return report
