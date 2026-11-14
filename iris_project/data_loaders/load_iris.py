# iris_project/data_loaders/load_iris.py
# Part C1: data_loader block — brings the Iris dataset into the pipeline.

import pandas as pd
from sklearn.datasets import load_iris as _load_iris

if 'data_loader' not in dir():
    try:
        from mage_ai.data_preparation.decorators import data_loader, test
    except ImportError:
        def data_loader(fn): return fn  # noqa
        def test(fn): return fn  # noqa


@data_loader
def load_data(*args, **kwargs):
    """Load the built-in Iris dataset as a pandas DataFrame (150 rows × 5 cols)."""
    iris = _load_iris(as_frame=True)
    df = iris.frame
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns")
    return df


@test
def test_output(output, *args) -> None:
    """Check: 150 rows, 5 columns, no missing values, 3 classes."""
    assert output is not None, "Output is None"
    assert len(output) == 150, f"Expected 150 rows, got {len(output)}"
    assert output.shape[1] == 5, f"Expected 5 columns, got {output.shape[1]}"
    assert output.isnull().sum().sum() == 0, "Dataset has missing values"
    assert output['target'].nunique() == 3, "Expected exactly 3 target classes"
    print("load_iris @test: OK — 150 rows, 5 cols, 0 nulls, 3 classes")
