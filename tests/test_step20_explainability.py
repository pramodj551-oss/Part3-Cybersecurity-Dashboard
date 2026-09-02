"""STEP 20 consolidated validation for model explainability."""

from pathlib import Path
import warnings

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from src.explainability import ExplainabilityError, extract_feature_importance, save_feature_importance


def test_step20_explainability_contract(tmp_path: Path):
    """Validate tree importance, linear fallback, ordering, and CSV contract in one test."""
    rng = np.random.RandomState(42)
    x = rng.normal(size=(40, 3))
    y = (x[:, 0] + 0.5 * x[:, 1] > 0).astype(int)
    names = ["feature_a", "feature_b", "feature_c"]

    tree = RandomForestClassifier(n_estimators=8, random_state=42).fit(x, y)
    tree_result = extract_feature_importance(tree, names)
    assert list(tree_result.columns) == ["feature", "importance"]
    assert len(tree_result) == len(names)
    assert tree_result["importance"].ge(0).all()
    assert tree_result["importance"].is_monotonic_decreasing

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            module=r"sklearn\.linear_model\._logistic",
        )
        linear = LogisticRegression(random_state=42, max_iter=500).fit(x, y)
    linear_result = extract_feature_importance(linear, names)
    assert len(linear_result) == len(names)
    assert linear_result["importance"].ge(0).all()
    assert linear_result["importance"].is_monotonic_decreasing

    output = tmp_path / "feature_importance.csv"
    saved = save_feature_importance(tree, names, output)
    assert output.is_file()
    assert saved.equals(tree_result)

    try:
        extract_feature_importance(object(), names)
    except ExplainabilityError:
        pass
    else:
        raise AssertionError("Unsupported estimator must raise ExplainabilityError")
