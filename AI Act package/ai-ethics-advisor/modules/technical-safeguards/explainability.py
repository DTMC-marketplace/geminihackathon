"""
Explainability Module
Tools for generating and evaluating AI model explanations.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class LocalExplanation:
    """Container for a single prediction's explanation."""
    prediction: Any
    confidence: float
    feature_contributions: Dict[str, float]
    counterfactuals: Optional[List[Dict]] = None
    explanation_text: Optional[str] = None


@dataclass  
class GlobalExplanation:
    """Container for model-level explanation."""
    feature_importance: Dict[str, float]
    feature_directions: Dict[str, str]  # positive/negative/mixed
    decision_rules: Optional[List[str]] = None


def compute_feature_importance_permutation(
    model: Callable,
    X: np.ndarray,
    y: np.ndarray,
    feature_names: List[str],
    n_repeats: int = 10,
    scoring: Callable = None
) -> Dict[str, float]:
    """
    Compute permutation feature importance.
    
    Args:
        model: Model with predict method
        X: Feature matrix
        y: True labels
        feature_names: Names of features
        n_repeats: Number of permutation repeats
        scoring: Scoring function (default: accuracy)
    
    Returns:
        Dict of feature -> importance score
    """
    if scoring is None:
        scoring = lambda y_true, y_pred: np.mean(y_true == y_pred)
    
    baseline_score = scoring(y, model(X))
    importances = {}
    
    for i, feature in enumerate(feature_names):
        scores = []
        for _ in range(n_repeats):
            X_permuted = X.copy()
            X_permuted[:, i] = np.random.permutation(X_permuted[:, i])
            score = scoring(y, model(X_permuted))
            scores.append(baseline_score - score)
        
        importances[feature] = np.mean(scores)
    
    return importances


class SimpleLIME:
    """
    Simplified LIME-style local explanation generator.
    
    Generates local linear approximations to explain individual predictions.
    """
    
    def __init__(
        self,
        model: Callable,
        feature_names: List[str],
        num_samples: int = 1000,
        kernel_width: float = 0.75
    ):
        self.model = model
        self.feature_names = feature_names
        self.num_samples = num_samples
        self.kernel_width = kernel_width
    
    def explain(self, instance: np.ndarray) -> LocalExplanation:
        """Generate explanation for a single instance."""
        # Generate perturbed samples
        perturbations = self._generate_perturbations(instance)
        
        # Get model predictions on perturbations
        predictions = self.model(perturbations)
        
        # Compute weights based on distance to original
        weights = self._compute_weights(instance, perturbations)
        
        # Fit weighted linear model
        contributions = self._fit_linear(perturbations, predictions, weights)
        
        # Original prediction
        pred = self.model(instance.reshape(1, -1))[0]
        
        return LocalExplanation(
            prediction=pred,
            confidence=1.0,  # Would need probability for proper confidence
            feature_contributions=dict(zip(self.feature_names, contributions)),
            explanation_text=self._generate_text(contributions, pred)
        )
    
    def _generate_perturbations(self, instance: np.ndarray) -> np.ndarray:
        """Generate perturbed samples around the instance."""
        # Simple Gaussian perturbation
        perturbations = np.random.normal(
            loc=instance,
            scale=0.1 * np.abs(instance) + 0.01,
            size=(self.num_samples, len(instance))
        )
        return perturbations
    
    def _compute_weights(
        self, 
        instance: np.ndarray, 
        perturbations: np.ndarray
    ) -> np.ndarray:
        """Compute kernel weights based on distance."""
        distances = np.sqrt(np.sum((perturbations - instance) ** 2, axis=1))
        weights = np.exp(-distances ** 2 / (self.kernel_width ** 2))
        return weights
    
    def _fit_linear(
        self,
        X: np.ndarray,
        y: np.ndarray,
        weights: np.ndarray
    ) -> np.ndarray:
        """Fit weighted linear regression."""
        # Add intercept
        X_aug = np.column_stack([np.ones(len(X)), X])
        
        # Weighted least squares
        W = np.diag(weights)
        try:
            coeffs = np.linalg.lstsq(
                X_aug.T @ W @ X_aug,
                X_aug.T @ W @ y,
                rcond=None
            )[0]
            return coeffs[1:]  # Exclude intercept
        except np.linalg.LinAlgError:
            return np.zeros(X.shape[1])
    
    def _generate_text(
        self, 
        contributions: np.ndarray, 
        prediction: Any
    ) -> str:
        """Generate human-readable explanation text."""
        sorted_idx = np.argsort(np.abs(contributions))[::-1]
        
        lines = [f"Prediction: {prediction}", "", "Key factors:"]
        
        for i in sorted_idx[:5]:  # Top 5 features
            feature = self.feature_names[i]
            contrib = contributions[i]
            direction = "increased" if contrib > 0 else "decreased"
            lines.append(f"- {feature}: {direction} prediction by {abs(contrib):.3f}")
        
        return "\n".join(lines)


class CounterfactualGenerator:
    """
    Generate counterfactual explanations ("what would need to change?").
    """
    
    def __init__(
        self,
        model: Callable,
        feature_names: List[str],
        feature_ranges: Dict[str, Tuple[float, float]],
        immutable_features: Optional[List[str]] = None,
        max_changes: int = 3
    ):
        self.model = model
        self.feature_names = feature_names
        self.feature_ranges = feature_ranges
        self.immutable_features = immutable_features or []
        self.max_changes = max_changes
    
    def generate(
        self,
        instance: np.ndarray,
        desired_outcome: int,
        n_counterfactuals: int = 3
    ) -> List[Dict]:
        """Generate counterfactual explanations."""
        counterfactuals = []
        
        current_pred = self.model(instance.reshape(1, -1))[0]
        if current_pred == desired_outcome:
            return [{"message": "Already has desired outcome"}]
        
        # Find mutable features
        mutable_idx = [
            i for i, f in enumerate(self.feature_names)
            if f not in self.immutable_features
        ]
        
        # Simple greedy search
        for _ in range(n_counterfactuals * 10):  # Try many times
            cf = self._generate_candidate(instance, mutable_idx)
            pred = self.model(cf.reshape(1, -1))[0]
            
            if pred == desired_outcome:
                changes = self._get_changes(instance, cf)
                if len(changes) <= self.max_changes:
                    counterfactuals.append({
                        'changes': changes,
                        'new_prediction': pred
                    })
                    if len(counterfactuals) >= n_counterfactuals:
                        break
        
        # Sort by number of changes
        counterfactuals.sort(key=lambda x: len(x['changes']))
        
        return counterfactuals[:n_counterfactuals]
    
    def _generate_candidate(
        self,
        instance: np.ndarray,
        mutable_idx: List[int]
    ) -> np.ndarray:
        """Generate a candidate counterfactual."""
        cf = instance.copy()
        
        # Randomly modify 1-3 features
        n_changes = np.random.randint(1, min(4, len(mutable_idx) + 1))
        features_to_change = np.random.choice(
            mutable_idx, size=n_changes, replace=False
        )
        
        for idx in features_to_change:
            feature = self.feature_names[idx]
            if feature in self.feature_ranges:
                low, high = self.feature_ranges[feature]
                cf[idx] = np.random.uniform(low, high)
        
        return cf
    
    def _get_changes(
        self,
        original: np.ndarray,
        counterfactual: np.ndarray
    ) -> Dict[str, Dict[str, float]]:
        """Get the changes between original and counterfactual."""
        changes = {}
        for i, feature in enumerate(self.feature_names):
            if not np.isclose(original[i], counterfactual[i]):
                changes[feature] = {
                    'from': float(original[i]),
                    'to': float(counterfactual[i])
                }
        return changes


def format_explanation_for_user(
    explanation: LocalExplanation,
    feature_descriptions: Optional[Dict[str, str]] = None,
    top_k: int = 5
) -> str:
    """
    Format an explanation for end-user consumption.
    
    Args:
        explanation: LocalExplanation object
        feature_descriptions: Human-readable feature descriptions
        top_k: Number of top features to show
    
    Returns:
        User-friendly explanation string
    """
    feature_descriptions = feature_descriptions or {}
    
    # Sort features by absolute contribution
    sorted_features = sorted(
        explanation.feature_contributions.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:top_k]
    
    lines = [
        "This decision was made based on the following factors:",
        ""
    ]
    
    for feature, contribution in sorted_features:
        desc = feature_descriptions.get(feature, feature)
        direction = "contributed positively" if contribution > 0 else "contributed negatively"
        lines.append(f"• {desc}: {direction}")
    
    if explanation.counterfactuals:
        lines.extend(["", "To potentially change this decision:"])
        for cf in explanation.counterfactuals[:2]:
            if 'changes' in cf:
                for feature, change in cf['changes'].items():
                    desc = feature_descriptions.get(feature, feature)
                    lines.append(
                        f"• Change {desc} from {change['from']:.2f} to {change['to']:.2f}"
                    )
    
    return "\n".join(lines)


class ExplanationValidator:
    """
    Validate explanation quality and consistency.
    """
    
    def __init__(self, model: Callable, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
    
    def check_fidelity(
        self,
        explanation: LocalExplanation,
        instance: np.ndarray,
        n_samples: int = 100
    ) -> float:
        """
        Check how well the explanation predicts model behavior locally.
        
        Returns correlation between linear approximation and model predictions.
        """
        # Generate local samples
        perturbations = np.random.normal(
            loc=instance,
            scale=0.1 * np.abs(instance) + 0.01,
            size=(n_samples, len(instance))
        )
        
        # Model predictions
        model_preds = self.model(perturbations)
        
        # Linear approximation predictions
        contributions = np.array([
            explanation.feature_contributions.get(f, 0)
            for f in self.feature_names
        ])
        linear_preds = perturbations @ contributions
        
        # Correlation
        if np.std(model_preds) == 0 or np.std(linear_preds) == 0:
            return 0.0
        
        return np.corrcoef(model_preds, linear_preds)[0, 1]
    
    def check_stability(
        self,
        explainer,
        instance: np.ndarray,
        n_runs: int = 10
    ) -> Dict[str, float]:
        """
        Check explanation stability across multiple runs.
        
        Returns variance of feature contributions.
        """
        all_contributions = defaultdict(list)
        
        for _ in range(n_runs):
            explanation = explainer.explain(instance)
            for feature, contrib in explanation.feature_contributions.items():
                all_contributions[feature].append(contrib)
        
        variances = {
            feature: np.var(contribs)
            for feature, contribs in all_contributions.items()
        }
        
        return variances


# Example usage
if __name__ == "__main__":
    # Create a simple model
    np.random.seed(42)
    
    # Simple logistic-like decision
    def simple_model(X):
        if X.ndim == 1:
            X = X.reshape(1, -1)
        scores = X[:, 0] * 0.5 + X[:, 1] * 0.3 - X[:, 2] * 0.2
        return (scores > 0).astype(int)
    
    feature_names = ['income', 'credit_score', 'debt_ratio']
    
    # Create explainer
    explainer = SimpleLIME(simple_model, feature_names)
    
    # Explain a prediction
    instance = np.array([50000, 700, 0.3])
    explanation = explainer.explain(instance)
    
    print("Explanation:")
    print(explanation.explanation_text)
    print("\nFeature contributions:")
    for feature, contrib in explanation.feature_contributions.items():
        print(f"  {feature}: {contrib:.4f}")
