"""Utility functions for data processing and model training."""

from sklearn.model_selection import train_test_split


def split_data(texts, labels, test_size=0.2, random_state=42):
    """Split text and labels into training and testing sets.
    
    Args:
        texts: Array-like of text samples.
        labels: Array-like of corresponding labels.
        test_size: Proportion of data to use for testing (default: 0.2).
        random_state: Random seed for reproducibility (default: 42).
    
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=test_size,
        random_state=random_state,
        stratify=labels if labels is not None else None
    )
    
    return X_train, X_test, y_train, y_test
