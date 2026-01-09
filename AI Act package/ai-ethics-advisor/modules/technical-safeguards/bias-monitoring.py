"""
Bias Monitoring Module
Tools for detecting and monitoring algorithmic bias in AI systems.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class FairnessMetrics:
    """Container for fairness metrics across groups."""
    demographic_parity: Dict[str, float]
    equalized_odds: Dict[str, Tuple[float, float]]  # (TPR, FPR) per group
    predictive_parity: Dict[str, float]
    calibration: Dict[str, float]
    selection_rates: Dict[str, float]


def calculate_selection_rate(predictions: np.ndarray, group_mask: np.ndarray) -> float:
    """Calculate positive prediction rate for a group."""
    group_preds = predictions[group_mask]
    if len(group_preds) == 0:
        return 0.0
    return np.mean(group_preds)


def calculate_tpr(y_true: np.ndarray, y_pred: np.ndarray, group_mask: np.ndarray) -> float:
    """Calculate True Positive Rate for a group."""
    group_true = y_true[group_mask]
    group_pred = y_pred[group_mask]
    positives = group_true == 1
    if np.sum(positives) == 0:
        return 0.0
    return np.mean(group_pred[positives])


def calculate_fpr(y_true: np.ndarray, y_pred: np.ndarray, group_mask: np.ndarray) -> float:
    """Calculate False Positive Rate for a group."""
    group_true = y_true[group_mask]
    group_pred = y_pred[group_mask]
    negatives = group_true == 0
    if np.sum(negatives) == 0:
        return 0.0
    return np.mean(group_pred[negatives])


def calculate_precision(y_true: np.ndarray, y_pred: np.ndarray, group_mask: np.ndarray) -> float:
    """Calculate Precision for a group."""
    group_true = y_true[group_mask]
    group_pred = y_pred[group_mask]
    predicted_positive = group_pred == 1
    if np.sum(predicted_positive) == 0:
        return 0.0
    return np.mean(group_true[predicted_positive])


def compute_fairness_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    protected_attribute: np.ndarray,
    group_names: Optional[Dict[int, str]] = None
) -> FairnessMetrics:
    """
    Compute comprehensive fairness metrics across protected groups.
    
    Args:
        y_true: Ground truth labels (0/1)
        y_pred: Predicted labels (0/1)
        protected_attribute: Group membership for each sample
        group_names: Optional mapping from group ID to name
    
    Returns:
        FairnessMetrics object with all computed metrics
    """
    unique_groups = np.unique(protected_attribute)
    
    if group_names is None:
        group_names = {g: f"Group_{g}" for g in unique_groups}
    
    selection_rates = {}
    tpr_by_group = {}
    fpr_by_group = {}
    precision_by_group = {}
    
    for group in unique_groups:
        group_mask = protected_attribute == group
        name = group_names.get(group, f"Group_{group}")
        
        selection_rates[name] = calculate_selection_rate(y_pred, group_mask)
        tpr_by_group[name] = calculate_tpr(y_true, y_pred, group_mask)
        fpr_by_group[name] = calculate_fpr(y_true, y_pred, group_mask)
        precision_by_group[name] = calculate_precision(y_true, y_pred, group_mask)
    
    # Demographic parity: normalized by max selection rate
    max_rate = max(selection_rates.values()) if selection_rates.values() else 1.0
    demographic_parity = {
        k: v / max_rate if max_rate > 0 else 0.0 
        for k, v in selection_rates.items()
    }
    
    # Equalized odds: (TPR, FPR) tuples
    equalized_odds = {
        k: (tpr_by_group[k], fpr_by_group[k]) 
        for k in tpr_by_group.keys()
    }
    
    return FairnessMetrics(
        demographic_parity=demographic_parity,
        equalized_odds=equalized_odds,
        predictive_parity=precision_by_group,
        calibration={},  # Would need probability scores
        selection_rates=selection_rates
    )


def check_four_fifths_rule(selection_rates: Dict[str, float]) -> Dict[str, bool]:
    """
    Check if selection rates satisfy the 4/5ths (80%) rule.
    
    Returns dict of group -> passes_rule
    """
    if not selection_rates:
        return {}
    
    max_rate = max(selection_rates.values())
    threshold = 0.8 * max_rate
    
    return {
        group: rate >= threshold 
        for group, rate in selection_rates.items()
    }


def compute_disparity(metrics: Dict[str, float], reference_group: Optional[str] = None) -> Dict[str, float]:
    """
    Compute disparity ratios relative to reference group (or max).
    
    Returns dict of group -> disparity_ratio
    """
    if not metrics:
        return {}
    
    if reference_group and reference_group in metrics:
        reference = metrics[reference_group]
    else:
        reference = max(metrics.values())
    
    if reference == 0:
        return {k: 0.0 for k in metrics.keys()}
    
    return {k: v / reference for k, v in metrics.items()}


class BiasMonitor:
    """
    Continuous bias monitoring for production systems.
    
    Usage:
        monitor = BiasMonitor(
            protected_attributes=['gender', 'race'],
            alert_thresholds={'demographic_parity': 0.8, 'fpr_disparity': 0.05}
        )
        
        # Log each prediction
        monitor.log_prediction(
            prediction=1,
            ground_truth=1,  # when available
            attributes={'gender': 'female', 'race': 'black'}
        )
        
        # Check for alerts
        alerts = monitor.check_alerts()
    """
    
    def __init__(
        self,
        protected_attributes: List[str],
        alert_thresholds: Optional[Dict[str, float]] = None,
        window_size: int = 1000
    ):
        self.protected_attributes = protected_attributes
        self.alert_thresholds = alert_thresholds or {
            'demographic_parity': 0.8,  # 4/5ths rule
            'tpr_disparity': 0.05,
            'fpr_disparity': 0.05
        }
        self.window_size = window_size
        
        # Rolling windows per attribute
        self.predictions = defaultdict(list)
        self.ground_truths = defaultdict(list)
        self.attribute_values = defaultdict(lambda: defaultdict(list))
    
    def log_prediction(
        self,
        prediction: int,
        ground_truth: Optional[int] = None,
        attributes: Dict[str, str] = None
    ):
        """Log a single prediction for monitoring."""
        attributes = attributes or {}
        
        for attr in self.protected_attributes:
            if attr in attributes:
                key = attr
                self.predictions[key].append(prediction)
                if ground_truth is not None:
                    self.ground_truths[key].append(ground_truth)
                self.attribute_values[key][attributes[attr]].append(
                    len(self.predictions[key]) - 1
                )
                
                # Maintain window size
                if len(self.predictions[key]) > self.window_size:
                    self._trim_window(key)
    
    def _trim_window(self, attr: str):
        """Remove oldest entries to maintain window size."""
        excess = len(self.predictions[attr]) - self.window_size
        self.predictions[attr] = self.predictions[attr][excess:]
        if self.ground_truths[attr]:
            self.ground_truths[attr] = self.ground_truths[attr][excess:]
        
        # Update indices
        for group in self.attribute_values[attr]:
            self.attribute_values[attr][group] = [
                i - excess for i in self.attribute_values[attr][group]
                if i >= excess
            ]
    
    def compute_current_metrics(self, attribute: str) -> Dict[str, Dict[str, float]]:
        """Compute current fairness metrics for an attribute."""
        if attribute not in self.predictions:
            return {}
        
        preds = np.array(self.predictions[attribute])
        
        metrics = {'selection_rates': {}}
        
        for group, indices in self.attribute_values[attribute].items():
            if indices:
                group_preds = preds[indices]
                metrics['selection_rates'][group] = np.mean(group_preds)
        
        # If we have ground truth, compute more metrics
        if self.ground_truths[attribute]:
            truths = np.array(self.ground_truths[attribute])
            metrics['tpr'] = {}
            metrics['fpr'] = {}
            
            for group, indices in self.attribute_values[attribute].items():
                if indices:
                    group_preds = preds[indices]
                    group_truths = truths[indices]
                    
                    pos_mask = group_truths == 1
                    neg_mask = group_truths == 0
                    
                    if np.sum(pos_mask) > 0:
                        metrics['tpr'][group] = np.mean(group_preds[pos_mask])
                    if np.sum(neg_mask) > 0:
                        metrics['fpr'][group] = np.mean(group_preds[neg_mask])
        
        return metrics
    
    def check_alerts(self) -> List[Dict]:
        """Check all thresholds and return any alerts."""
        alerts = []
        
        for attr in self.protected_attributes:
            metrics = self.compute_current_metrics(attr)
            
            if not metrics:
                continue
            
            # Check 4/5ths rule
            if 'selection_rates' in metrics:
                passes = check_four_fifths_rule(metrics['selection_rates'])
                for group, passed in passes.items():
                    if not passed:
                        alerts.append({
                            'type': 'demographic_parity',
                            'attribute': attr,
                            'group': group,
                            'value': metrics['selection_rates'][group],
                            'threshold': self.alert_thresholds.get('demographic_parity', 0.8),
                            'message': f"Selection rate for {group} violates 4/5ths rule"
                        })
            
            # Check TPR disparity
            if 'tpr' in metrics and len(metrics['tpr']) > 1:
                max_tpr = max(metrics['tpr'].values())
                for group, tpr in metrics['tpr'].items():
                    disparity = max_tpr - tpr
                    threshold = self.alert_thresholds.get('tpr_disparity', 0.05)
                    if disparity > threshold:
                        alerts.append({
                            'type': 'tpr_disparity',
                            'attribute': attr,
                            'group': group,
                            'value': disparity,
                            'threshold': threshold,
                            'message': f"TPR disparity for {group} exceeds threshold"
                        })
            
            # Check FPR disparity
            if 'fpr' in metrics and len(metrics['fpr']) > 1:
                min_fpr = min(metrics['fpr'].values())
                for group, fpr in metrics['fpr'].items():
                    disparity = fpr - min_fpr
                    threshold = self.alert_thresholds.get('fpr_disparity', 0.05)
                    if disparity > threshold:
                        alerts.append({
                            'type': 'fpr_disparity',
                            'attribute': attr,
                            'group': group,
                            'value': disparity,
                            'threshold': threshold,
                            'message': f"FPR disparity for {group} exceeds threshold"
                        })
        
        return alerts
    
    def get_summary_report(self) -> str:
        """Generate a summary report of current bias metrics."""
        lines = ["=" * 60, "BIAS MONITORING REPORT", "=" * 60, ""]
        
        for attr in self.protected_attributes:
            metrics = self.compute_current_metrics(attr)
            if not metrics:
                continue
            
            lines.append(f"Attribute: {attr}")
            lines.append("-" * 40)
            
            if 'selection_rates' in metrics:
                lines.append("Selection Rates:")
                for group, rate in metrics['selection_rates'].items():
                    lines.append(f"  {group}: {rate:.3f}")
                
                # Check 4/5ths
                passes = check_four_fifths_rule(metrics['selection_rates'])
                failing = [g for g, p in passes.items() if not p]
                if failing:
                    lines.append(f"  ⚠️ 4/5ths rule violated for: {', '.join(failing)}")
            
            lines.append("")
        
        alerts = self.check_alerts()
        if alerts:
            lines.append("ACTIVE ALERTS:")
            lines.append("-" * 40)
            for alert in alerts:
                lines.append(f"⚠️ {alert['message']}")
        else:
            lines.append("✓ No active alerts")
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Simulate predictions with bias
    np.random.seed(42)
    n = 1000
    
    # Create groups
    gender = np.random.choice([0, 1], n)  # 0=male, 1=female
    
    # Biased predictions (lower positive rate for group 1)
    y_true = np.random.choice([0, 1], n, p=[0.5, 0.5])
    y_pred = np.where(
        gender == 0,
        (np.random.random(n) < 0.6).astype(int),
        (np.random.random(n) < 0.4).astype(int)
    )
    
    # Compute metrics
    metrics = compute_fairness_metrics(
        y_true, y_pred, gender,
        group_names={0: 'male', 1: 'female'}
    )
    
    print("Fairness Metrics:")
    print(f"Selection Rates: {metrics.selection_rates}")
    print(f"Demographic Parity: {metrics.demographic_parity}")
    print(f"4/5ths Rule: {check_four_fifths_rule(metrics.selection_rates)}")
