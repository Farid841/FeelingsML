from app.evaluate_model import evaluate_model
from app.save_evaluation import save_evaluation_report
from app.analyze_results import analyze_results


def generate_full_report():
    """Generate comprehensive model evaluation report"""
    # Generate evaluations
    evaluate_model()

    # Save detailed metrics
    save_evaluation_report()

    # Analyze results
    analysis_path = analyze_results()

    print(f"Full analysis report generated at: {analysis_path}")
