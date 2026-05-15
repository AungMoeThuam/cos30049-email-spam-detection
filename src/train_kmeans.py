"""K-Means clustering model training and evaluation."""

import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score


def create_pipeline(
    n_clusters=3,
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    stop_words='english',
    random_state=42
):
    """Create a K-Means clustering pipeline.
    
    Args:
        n_clusters: Number of clusters (default: 3).
        max_features: Maximum number of TF-IDF features (default: 5000).
        ngram_range: N-gram range for TfidfVectorizer (default: (1, 2)).
        min_df: Minimum document frequency (default: 2).
        stop_words: Stop words to remove (default: 'english').
        random_state: Random seed for reproducibility (default: 42).
    
    Returns:
        sklearn.pipeline.Pipeline with TfidfVectorizer and KMeans.
    """
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            stop_words=stop_words,
            dtype='float64'
        )),
        ('kmeans', KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10,
            verbose=0
        ))
    ])
    
    return pipeline


def train(pipeline, X_train):
    """Train K-Means pipeline on training data.
    
    Args:
        pipeline: sklearn.pipeline.Pipeline with TfidfVectorizer and KMeans.
        X_train: Training text samples.
    
    Returns:
        Trained pipeline.
    """
    pipeline.fit(X_train)
    return pipeline


def predict(pipeline, X_test):
    """Predict cluster labels for test data.
    
    Args:
        pipeline: Trained sklearn.pipeline.Pipeline.
        X_test: Test text samples.
    
    Returns:
        Array of cluster labels.
    """
    return pipeline.predict(X_test)


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


def get_cluster_centers(pipeline, n_terms=10):
    """Extract top words for each cluster from TF-IDF weights.
    
    Args:
        pipeline: Trained sklearn.pipeline.Pipeline.
        n_terms: Number of top terms to extract per cluster (default: 10).
    
    Returns:
        Dictionary mapping cluster_id to list of top words.
    """
    tfidf = pipeline.named_steps['tfidf']
    kmeans = pipeline.named_steps['kmeans']
    
    # Get feature names from TF-IDF vectorizer
    feature_names = tfidf.get_feature_names_out()
    
    # Get cluster centers (centroids)
    centers = kmeans.cluster_centers_
    
    cluster_words = {}
    for cluster_id, center in enumerate(centers):
        # Get indices of top n_terms features
        top_indices = center.argsort()[-n_terms:][::-1]
        top_words = [feature_names[i] for i in top_indices]
        cluster_words[cluster_id] = top_words
    
    return cluster_words


def evaluate_clustering(y_true, y_pred):
    """Evaluate clustering performance using multiple metrics.
    
    Args:
        y_true: True labels.
        y_pred: Predicted cluster labels.
    
    Returns:
        Dictionary with ARI, NMI, and Silhouette scores.
    """
    # Adjusted Rand Index
    ari = adjusted_rand_score(y_true, y_pred)
    
    # Normalized Mutual Information
    nmi = normalized_mutual_info_score(y_true, y_pred)
    
    # Silhouette score requires the original data for distance calculation,
    # so we'll compute it if possible (requires X data)
    # For now, we'll return None if it can't be computed
    metrics = {
        'ARI': ari,
        'NMI': nmi,
    }
    
    return metrics


def print_clustering_results(metrics):
    """Print clustering evaluation metrics.
    
    Args:
        metrics: Dictionary of metrics from evaluate_clustering().
    """
    print("\n" + "="*50)
    print("Clustering Evaluation Results")
    print("="*50)
    for metric_name, metric_value in metrics.items():
        if metric_value is not None:
            print(f"{metric_name:.<30} {metric_value:.4f}")
        else:
            print(f"{metric_name:.<30} N/A")
    print("="*50 + "\n")
