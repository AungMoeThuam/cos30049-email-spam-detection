"""Logistic Regression model training and evaluation."""

import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def create_pipeline(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    stop_words='english',
    random_state=42,
    max_iter=1000
):
    """Create a Logistic Regression pipeline.
    
    Args:
        max_features: Maximum number of TF-IDF features (default: 5000).
        ngram_range: N-gram range for TfidfVectorizer (default: (1, 2)).
        min_df: Minimum document frequency (default: 2).
        stop_words: Stop words to remove (default: 'english').
        random_state: Random seed for reproducibility (default: 42).
        max_iter: Maximum iterations for Logistic Regression (default: 1000).
    
    Returns:
        sklearn.pipeline.Pipeline with TfidfVectorizer and LogisticRegression.
    """
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            stop_words=stop_words,
            dtype='float64'
        )),
        ('logistic_regression', LogisticRegression(
            random_state=random_state,
            max_iter=max_iter,
            verbose=0
        ))
    ])
    
    return pipeline


def train(pipeline, X_train, y_train):
    """Train Logistic Regression pipeline on training data.
    
    Args:
        pipeline: sklearn.pipeline.Pipeline with TfidfVectorizer and LogisticRegression.
        X_train: Training text samples.
        y_train: Training labels.
    
    Returns:
        Trained pipeline.
    """
    pipeline.fit(X_train, y_train)
    return pipeline


def predict(pipeline, X_test):
    """Predict labels for test data.
    
    Args:
        pipeline: Trained sklearn.pipeline.Pipeline.
        X_test: Test text samples.
    
    Returns:
        Array of predicted labels.
    """
    return pipeline.predict(X_test)


def predict_proba(pipeline, X_test):
    """Predict class probabilities for test data.
    
    Args:
        pipeline: Trained sklearn.pipeline.Pipeline.
        X_test: Test text samples.
    
    Returns:
        Array of class probabilities.
    """
    return pipeline.predict_proba(X_test)


def save_model(pipeline, filepath):
    """Save trained model to disk.
    
    Args:
        pipeline: Trained sklearn.pipeline.Pipeline.
        filepath: Path to save the model (.pkl file).
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(pipeline, filepath)


def load_model(filepath):
    """Load trained model from disk.
    
    Args:
        filepath: Path to the saved model (.pkl file).
    
    Returns:
        Trained sklearn.pipeline.Pipeline.
    """
    return joblib.load(filepath)


def get_feature_importance(pipeline, n_terms=15):
    """Extract most important features for each class.
    
    Args:
        pipeline: Trained sklearn.pipeline.Pipeline.
        n_terms: Number of top terms to extract per class (default: 15).
    
    Returns:
        Dictionary mapping class_label to list of (word, coefficient) tuples.
    """
    tfidf = pipeline.named_steps['tfidf']
    lr = pipeline.named_steps['logistic_regression']
    
    feature_names = tfidf.get_feature_names_out()
    
    # Get coefficients for each class
    coefficients = lr.coef_
    
    class_features = {}
    for class_id, coef in enumerate(coefficients):
        # Get indices of top n_terms features
        top_indices = coef.argsort()[-n_terms:][::-1]
        top_words = [(feature_names[i], coef[i]) for i in top_indices]
        class_features[class_id] = top_words
    
    return class_features
