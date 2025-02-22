import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def save_evaluation_report(y_true, y_pred, label_type):
    """Generate and save detailed evaluation report"""
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Generate classification report
    report = classification_report(y_true, y_pred)
    
    # Generate confusion matrix values
    cm = confusion_matrix(y_true, y_pred)
    
    # Create timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d")
    
    # Save text report
    report_path = f'outputs/evaluation_report_{label_type.lower()}_{timestamp}.txt'
    with open(report_path, 'w') as f:
        f.write(f"Evaluation Report for {label_type} - {datetime.now()}\n")
        f.write("="*50 + "\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\n\nConfusion Matrix:\n")
        f.write(str(cm))
        f.write("\n\nMatrix Format:\n")
        f.write("[[TN, FP]\n [FN, TP]]\n\n")
        
        # Calculate additional metrics
        tn, fp, fn, tp = cm.ravel()
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        f.write("\nDetailed Metrics:\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1-Score: {f1:.4f}\n")

    return report_path