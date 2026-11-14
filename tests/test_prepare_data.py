# tests/test_prepare_data.py
# Assignment Part A3: CI test for the Mage prepare_data block.
# The block imports its decorators only when Mage is not running,
# so the file works both inside Mage and in plain pytest.

from sklearn.datasets import load_iris
from iris_project.transformers.prepare_data import transform


def test_split_is_80_20():
    df = load_iris(as_frame=True).frame
    out = transform(df)
    assert (out["split"] == "train").sum() == 120
    assert (out["split"] == "test").sum() == 30
