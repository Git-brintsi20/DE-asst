# iris_project/transformers/prepare_data.py
# Part C1 / A3: transformer block — splits Iris into train (80%) and test (20%).
# This file is imported directly by tests/test_prepare_data.py in the CI run,
# so it must work outside Mage. The 'if not in globals()' guard makes that safe.

import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    # Running outside Mage (e.g. in pytest): provide no-op decorators
    def transformer(fn):
        return fn
    def test(fn):
        return fn


@transformer
def transform(df, *args, **kwargs):
    """Split the Iris DataFrame 80 / 20 and label each row.

    Args:
        df: 150-row DataFrame from load_iris.
    Returns:
        Combined DataFrame with a new 'split' column ('train' or 'test').
    """
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    train_df = train_df.copy()
    test_df  = test_df.copy()
    train_df['split'] = 'train'
    test_df['split']  = 'test'

    out = pd.concat([train_df, test_df], ignore_index=True)
    print(f"Train rows: {(out['split']=='train').sum()}, "
          f"Test rows: {(out['split']=='test').sum()}")
    return out


@test
def test_output(output, *args) -> None:
    """Check: exactly 120 train rows and 30 test rows."""
    assert output is not None, "Output is None"
    assert (output["split"] == "train").sum() == 120, \
        f"Expected 120 train rows, got {(output['split']=='train').sum()}"
    assert (output["split"] == "test").sum() == 30, \
        f"Expected 30 test rows, got {(output['split']=='test').sum()}"
    print("prepare_data @test: OK — 120 train, 30 test")
