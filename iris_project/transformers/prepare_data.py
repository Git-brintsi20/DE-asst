# iris_project/transformers/prepare_data.py
# Part C1 / A3: transformer block — splits Iris into train (80%) and test (20%).
#
# HOW THE DUAL-MODE IMPORT WORKS:
# - Inside Mage: `mage run` pre-injects `transformer` and `test` into the exec()
#   namespace before running this file. So 'transformer' IS in globals() already.
#   The if-guard is False, no import runs, Mage's collector picks up @transformer.
# - Outside Mage (pytest): 'transformer' is NOT in globals(), so we import from
#   mage_ai (or fall back to pass-through). pytest can call transform() directly.

import pandas as pd
from sklearn.model_selection import train_test_split

if 'transformer' not in dir():
    try:
        from mage_ai.data_preparation.decorators import transformer, test
    except ImportError:
        def transformer(fn): return fn  # noqa
        def test(fn): return fn  # noqa


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
