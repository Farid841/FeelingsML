def analyze_results():
    """Analyze model performance from evaluation reports"""
    timestamp = datetime.now().strftime("%Y%m%d")

    # Read evaluation reports
    with open(f'outputs/classification_report_positive_{timestamp}.txt') as f:
        pos_report = f.read()
    with open(f'outputs/classification_report_negative_{timestamp}.txt') as f:
        neg_report = f.read()

    # Generate summary report
    with open(f'outputs/analysis_summary_{timestamp}.txt', 'w') as f:
        f.write("Model Performance Analysis\n")
        f.write("========================\n\n")
        f.write("Positive Sentiment Model:\n")
        f.write(pos_report)
        f.write("\nNegative Sentiment Model:\n")
        f.write(neg_report)
