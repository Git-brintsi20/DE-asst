# iris_project/transformers/evaluate_model.py
# Part C3: downstream block from train_model — produces a confusion matrix
# and a metrics table. Runs in parallel with save_results after train_model.

import pandas as pd
from sklearn.metrics import (
    confusion_matrix, classification_report, accuracy_score
)

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

CLASSES = ['setosa', 'versicolor', 'virginica']


@transformer
def transform(df, *args, **kwargs):
    """Build a confusion matrix and a metrics table from train_model's output.

    Args:
        df: 30-row test prediction DataFrame from train_model.
    Returns:
        Dict with 'confusion_matrix' (DataFrame) and 'metrics' (DataFrame).
    """
    y_true = df['target']
    y_pred = df['predicted']

    cm = confusion_matrix(y_true, y_pred)
    cm_df = pd.DataFrame(cm,
                         index=[f'actual_{c}' for c in CLASSES],
                         columns=[f'pred_{c}' for c in CLASSES])

    report = classification_report(y_true, y_pred,
                                   target_names=CLASSES, output_dict=True)
    metrics_df = pd.DataFrame(report).transpose()

    print("\n--- Confusion Matrix ---")
    print(cm_df.to_string())
    print("\n--- Classification Report ---")
    print(metrics_df.round(3).to_string())

    return {'confusion_matrix': cm_df, 'metrics': metrics_df}


@test
def test_output(output, *args) -> None:
    """Check: confusion matrix is 3×3 and macro F1 is reasonable."""
    cm = output['confusion_matrix']
    metrics = output['metrics']
    assert cm.shape == (3, 3), f"Confusion matrix should be 3×3, got {cm.shape}"
    macro_f1 = metrics.loc['macro avg', 'f1-score']
    assert macro_f1 >= 0.80, f"Macro F1 {macro_f1:.3f} < 0.80"
    print(f"evaluate_model @test: OK — 3×3 matrix, macro F1={macro_f1:.3f}")
