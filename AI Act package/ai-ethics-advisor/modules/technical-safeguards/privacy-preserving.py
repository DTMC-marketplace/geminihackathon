"""
Privacy-Preserving Module
Tools for implementing privacy-preserving techniques in AI systems.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import hashlib
from collections import Counter


@dataclass
class PrivacyMetrics:
    """Container for privacy analysis results."""
    k_anonymity: int
    l_diversity: Dict[str, int]
    quasi_identifiers: List[str]
    sensitive_attributes: List[str]
    unique_combinations: int
    reidentification_risk: float


def compute_k_anonymity(
    data: np.ndarray,
    quasi_identifier_cols: List[int]
) -> int:
    """
    Compute k-anonymity of a dataset.
    
    k-anonymity: every record is indistinguishable from at least k-1 other records
    with respect to quasi-identifiers.
    
    Args:
        data: Dataset as numpy array
        quasi_identifier_cols: Indices of quasi-identifier columns
    
    Returns:
        k value (minimum group size)
    """
    # Extract quasi-identifiers
    qi_data = data[:, quasi_identifier_cols]
    
    # Count occurrences of each combination
    qi_tuples = [tuple(row) for row in qi_data]
    counts = Counter(qi_tuples)
    
    # k is the minimum count
    return min(counts.values()) if counts else 0


def compute_l_diversity(
    data: np.ndarray,
    quasi_identifier_cols: List[int],
    sensitive_col: int
) -> Dict[str, int]:
    """
    Compute l-diversity for a sensitive attribute.
    
    l-diversity: every equivalence class has at least l distinct sensitive values.
    
    Args:
        data: Dataset as numpy array
        quasi_identifier_cols: Indices of quasi-identifier columns
        sensitive_col: Index of sensitive attribute column
    
    Returns:
        Dict with l value and statistics
    """
    qi_data = data[:, quasi_identifier_cols]
    sensitive_data = data[:, sensitive_col]
    
    # Group by quasi-identifiers
    groups = {}
    for i, qi in enumerate(qi_data):
        key = tuple(qi)
        if key not in groups:
            groups[key] = set()
        groups[key].add(sensitive_data[i])
    
    # l is the minimum number of distinct sensitive values
    diversities = [len(values) for values in groups.values()]
    
    return {
        'l': min(diversities) if diversities else 0,
        'mean_diversity': np.mean(diversities) if diversities else 0,
        'num_groups': len(groups)
    }


class DifferentialPrivacy:
    """
    Differential privacy mechanisms for aggregate queries.
    
    Provides epsilon-differential privacy guarantees.
    """
    
    def __init__(self, epsilon: float):
        """
        Initialize with privacy budget.
        
        Args:
            epsilon: Privacy parameter (smaller = more private)
        """
        self.epsilon = epsilon
        self.queries_answered = 0
        self.total_epsilon_spent = 0.0
    
    def laplace_mechanism(
        self,
        true_value: float,
        sensitivity: float
    ) -> float:
        """
        Add Laplace noise for epsilon-differential privacy.
        
        Args:
            true_value: True query result
            sensitivity: Query sensitivity (max change from one record)
        
        Returns:
            Noisy result satisfying differential privacy
        """
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        
        self.queries_answered += 1
        self.total_epsilon_spent += self.epsilon
        
        return true_value + noise
    
    def gaussian_mechanism(
        self,
        true_value: float,
        sensitivity: float,
        delta: float = 1e-5
    ) -> float:
        """
        Add Gaussian noise for (epsilon, delta)-differential privacy.
        
        Args:
            true_value: True query result
            sensitivity: Query sensitivity
            delta: Probability of privacy breach
        
        Returns:
            Noisy result
        """
        sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / self.epsilon
        noise = np.random.normal(0, sigma)
        
        self.queries_answered += 1
        self.total_epsilon_spent += self.epsilon
        
        return true_value + noise
    
    def private_count(self, data: np.ndarray, condition: np.ndarray) -> float:
        """
        Differentially private count query.
        
        Args:
            data: Dataset
            condition: Boolean array indicating which records to count
        
        Returns:
            Noisy count
        """
        true_count = np.sum(condition)
        return self.laplace_mechanism(true_count, sensitivity=1.0)
    
    def private_mean(
        self,
        values: np.ndarray,
        lower_bound: float,
        upper_bound: float
    ) -> float:
        """
        Differentially private mean query.
        
        Args:
            values: Values to average
            lower_bound: Minimum possible value
            upper_bound: Maximum possible value
        
        Returns:
            Noisy mean
        """
        # Clip values to bounds
        clipped = np.clip(values, lower_bound, upper_bound)
        
        # Sensitivity of mean is range / n
        n = len(values)
        sensitivity = (upper_bound - lower_bound) / n
        
        true_mean = np.mean(clipped)
        return self.laplace_mechanism(true_mean, sensitivity)
    
    def private_histogram(
        self,
        data: np.ndarray,
        bins: List[Tuple[float, float]]
    ) -> List[float]:
        """
        Differentially private histogram.
        
        Args:
            data: Values to bin
            bins: List of (lower, upper) bin boundaries
        
        Returns:
            Noisy bin counts
        """
        noisy_counts = []
        for lower, upper in bins:
            count = np.sum((data >= lower) & (data < upper))
            noisy_counts.append(self.laplace_mechanism(count, sensitivity=1.0))
        
        return noisy_counts
    
    def get_privacy_budget_status(self) -> Dict[str, float]:
        """Get current privacy budget usage."""
        return {
            'epsilon_per_query': self.epsilon,
            'queries_answered': self.queries_answered,
            'total_epsilon_spent': self.total_epsilon_spent
        }


class DataAnonymizer:
    """
    Data anonymization utilities.
    """
    
    @staticmethod
    def generalize_numeric(
        values: np.ndarray,
        bin_size: float
    ) -> np.ndarray:
        """
        Generalize numeric values into bins.
        
        Args:
            values: Numeric values
            bin_size: Size of generalization bins
        
        Returns:
            Generalized values (bin labels)
        """
        return np.floor(values / bin_size) * bin_size
    
    @staticmethod
    def generalize_categorical(
        values: np.ndarray,
        hierarchy: Dict[str, str]
    ) -> np.ndarray:
        """
        Generalize categorical values using a hierarchy.
        
        Args:
            values: Categorical values
            hierarchy: Mapping from specific to general values
        
        Returns:
            Generalized values
        """
        return np.array([hierarchy.get(v, v) for v in values])
    
    @staticmethod
    def suppress_rare(
        values: np.ndarray,
        min_count: int,
        replacement: str = '*'
    ) -> np.ndarray:
        """
        Suppress values that appear fewer than min_count times.
        
        Args:
            values: Values to process
            min_count: Minimum count to keep
            replacement: Replacement for suppressed values
        
        Returns:
            Values with rare entries suppressed
        """
        counts = Counter(values)
        return np.array([
            v if counts[v] >= min_count else replacement
            for v in values
        ])
    
    @staticmethod
    def hash_identifier(
        value: str,
        salt: str = ''
    ) -> str:
        """
        Create a one-way hash of an identifier.
        
        Args:
            value: Value to hash
            salt: Salt for the hash
        
        Returns:
            Hashed value
        """
        return hashlib.sha256((salt + value).encode()).hexdigest()[:16]
    
    @staticmethod
    def add_noise_to_location(
        lat: float,
        lon: float,
        radius_km: float
    ) -> Tuple[float, float]:
        """
        Add random noise to location data.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius_km: Maximum displacement in km
        
        Returns:
            (noisy_lat, noisy_lon)
        """
        # Approximate degrees per km
        lat_per_km = 1 / 111
        lon_per_km = 1 / (111 * np.cos(np.radians(lat)))
        
        # Random displacement
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, radius_km)
        
        new_lat = lat + distance * lat_per_km * np.sin(angle)
        new_lon = lon + distance * lon_per_km * np.cos(angle)
        
        return new_lat, new_lon


def assess_reidentification_risk(
    data: np.ndarray,
    quasi_identifier_cols: List[int],
    population_size: Optional[int] = None
) -> Dict[str, float]:
    """
    Assess the risk of reidentification from quasi-identifiers.
    
    Args:
        data: Dataset as numpy array
        quasi_identifier_cols: Indices of quasi-identifier columns
        population_size: Size of the population (if known)
    
    Returns:
        Risk assessment metrics
    """
    k = compute_k_anonymity(data, quasi_identifier_cols)
    n = len(data)
    
    # Unique combinations
    qi_data = data[:, quasi_identifier_cols]
    qi_tuples = [tuple(row) for row in qi_data]
    unique_combos = len(set(qi_tuples))
    
    # Proportion of unique records
    counts = Counter(qi_tuples)
    unique_records = sum(1 for c in counts.values() if c == 1)
    unique_proportion = unique_records / n
    
    # Prosecutor risk (probability of unique match)
    prosecutor_risk = unique_proportion
    
    # Journalist risk (expected match probability)
    journalist_risk = 1 / k if k > 0 else 1.0
    
    # Marketer risk (proportion identifiable)
    marketer_risk = unique_proportion
    
    return {
        'k_anonymity': k,
        'unique_combinations': unique_combos,
        'unique_records': unique_records,
        'unique_proportion': unique_proportion,
        'prosecutor_risk': prosecutor_risk,
        'journalist_risk': journalist_risk,
        'marketer_risk': marketer_risk,
        'risk_level': 'HIGH' if k < 5 else ('MEDIUM' if k < 10 else 'LOW')
    }


class PrivacyAuditLog:
    """
    Log data access and processing for privacy auditing.
    """
    
    def __init__(self):
        self.logs = []
    
    def log_access(
        self,
        user: str,
        purpose: str,
        data_type: str,
        operation: str,
        record_count: int,
        privacy_mechanism: Optional[str] = None
    ):
        """Log a data access event."""
        import datetime
        
        self.logs.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user': user,
            'purpose': purpose,
            'data_type': data_type,
            'operation': operation,
            'record_count': record_count,
            'privacy_mechanism': privacy_mechanism
        })
    
    def get_audit_report(self) -> str:
        """Generate audit report."""
        lines = ["=" * 60, "PRIVACY AUDIT LOG", "=" * 60, ""]
        
        for entry in self.logs[-50:]:  # Last 50 entries
            lines.append(f"[{entry['timestamp']}]")
            lines.append(f"  User: {entry['user']}")
            lines.append(f"  Purpose: {entry['purpose']}")
            lines.append(f"  Data: {entry['data_type']}")
            lines.append(f"  Operation: {entry['operation']}")
            lines.append(f"  Records: {entry['record_count']}")
            if entry['privacy_mechanism']:
                lines.append(f"  Privacy: {entry['privacy_mechanism']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def summarize(self) -> Dict[str, Any]:
        """Summarize audit log."""
        return {
            'total_accesses': len(self.logs),
            'unique_users': len(set(e['user'] for e in self.logs)),
            'operations': Counter(e['operation'] for e in self.logs),
            'total_records_accessed': sum(e['record_count'] for e in self.logs)
        }


# Example usage
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    n = 1000
    
    data = np.column_stack([
        np.random.randint(20, 80, n),  # Age
        np.random.choice(['M', 'F'], n),  # Gender
        np.random.randint(10000, 99999, n),  # Zip code
        np.random.choice(['A', 'B', 'C', 'D'], n),  # Condition (sensitive)
    ])
    
    # Compute k-anonymity (age, gender, zip as QIs)
    k = compute_k_anonymity(data, [0, 1, 2])
    print(f"k-anonymity: {k}")
    
    # Compute l-diversity
    l_div = compute_l_diversity(data, [0, 1, 2], 3)
    print(f"l-diversity: {l_div}")
    
    # Differential privacy example
    dp = DifferentialPrivacy(epsilon=0.1)
    ages = data[:, 0].astype(float)
    private_mean_age = dp.private_mean(ages, 20, 80)
    print(f"Private mean age: {private_mean_age:.1f} (true: {np.mean(ages):.1f})")
    
    # Reidentification risk
    risk = assess_reidentification_risk(data, [0, 1, 2])
    print(f"Reidentification risk: {risk['risk_level']}")
