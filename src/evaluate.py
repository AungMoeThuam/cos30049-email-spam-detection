"""Evaluation metrics for classification models."""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


def evaluate_model(y_true, y_pred, y_proba=None, average='weighted'):
    """Evaluate classification model performance.
    
    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        y_proba: Predicted probabilities (optional, needed for ROC-AUC).
        average: Averaging strategy for multi-class metrics (default: 'weighted').
    
    Returns:
        Dictionary with evaluation metrics.
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
        'f1': f1_score(y_true, y_pred, average=average, zero_division=0),
    }
    
    # ROC-AUC only for binary classification
    if y_proba is not None and len(set(y_true)) == 2:
        try:
            if y_proba.ndim == 2:
                # Use probabilities of the positive class
                metrics['roc_auc'] = roc_auc_score(y_true, y_proba[:, 1])
            else:
                metrics['roc_auc'] = roc_auc_score(y_true, y_proba)
        except Exception as e:
            metrics['roc_auc'] = None
    else:
        metrics['roc_auc'] = None
    
    return metrics


def print_evaluation_results(metrics):
    """Print model evaluation metrics.
    
    Args:
        metrics: Dictionary of metrics from evaluate_model().
    """
    print("\n" + "="*50)
    print("Classification Model Evaluation Results")
    print("="*50)
    for metric_name, metric_value in metrics.items():
        if metric_value is not None:
            print(f"{metric_name:.<30} {metric_value:.4f}")
        else:
            print(f"{metric_name:.<30} N/A")
    print("="*50 + "\n")


def print_confusion_matrix(y_true, y_pred, labels=None):
    """Print confusion matrix.
    
    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        labels: Labels to display (default: None).
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    print("\n" + "="*50)
    print("Confusion Matrix")
    print("="*50)
    print(cm)
    print("="*50 + "\n")


def print_classification_report(y_true, y_pred, target_names=None):
    """Print detailed classification report.
    
    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        target_names: Names of target classes (default: None).
    """
    report = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
    print("\n" + "="*50)
    print("Classification Report")
    print("="*50)
    print(report)
    print("="*50 + "\n")
