# iris_project/transformers/evaluate_model.py
# Part C3: downstream transformer from train_model — confusion matrix + metrics.

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

if 'transformer' not in dir():
    try:
        from mage_ai.data_preparation.decorators import transformer, test
    except ImportError:
        def transformer(fn): return fn  # noqa
        def test(fn): return fn  # noqa

CLASSES = ['setosa', 'versicolor', 'virginica']


@transformer
def transform(df, *args, **kwargs):
    """Build confusion matrix and metrics table from train_model output."""
    y_true = df['target']
    y_pred = df['predicted']

    cm = pd.DataFrame(
        confusion_matrix(y_true, y_pred),
        index=[f'actual_{c}' for c in CLASSES],
        columns=[f'pred_{c}' for c in CLASSES]
    )
    report  = classification_report(y_true, y_pred, target_names=CLASSES,
                                    output_dict=True)
    metrics = pd.DataFrame(report).transpose()

    print("\n--- Confusion Matrix ---")
    print(cm.to_string())
    print("\n--- Classification Report ---")
    print(metrics.round(3).to_string())

    return {'confusion_matrix': cm, 'metrics': metrics}


@test
def test_output(output, *args) -> None:
    """Check: 3×3 confusion matrix and macro F1 >= 0.80."""
    cm      = output['confusion_matrix']
    metrics = output['metrics']
    assert cm.shape == (3, 3), f"Expected 3×3 confusion matrix, got {cm.shape}"
    # Reset index in case Mage serialised it, then filter for the macro avg row
    m = metrics.reset_index()
    idx_col = m.columns[0]  # usually 'index' or the original index name
    macro_rows = m[m[idx_col].astype(str).str.strip() == 'macro avg']
    if len(macro_rows) == 0:
        # Fallback: re-derive from raw classification report
        macro_f1 = float(metrics['f1-score'].iloc[-2])  # macro avg is second-to-last
    else:
        macro_f1 = float(macro_rows['f1-score'].values[0])
    assert macro_f1 >= 0.80, f"Macro F1 {macro_f1:.3f} < 0.80"
    print(f"evaluate_model @test: OK — 3×3 matrix, macro F1={macro_f1:.3f}")
