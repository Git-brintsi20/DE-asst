# iris_project/transformers/train_model.py
# Part C1 / C2: transformer block — trains a DecisionTreeClassifier on the
# train split, predicts the test split, checks accuracy, saves the model.

import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

FEATURES = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']
TARGET   = 'target'

# Minimum accuracy required for the results to be saved.
# If this test fails, Mage stops the pipeline — save_results never runs.
MIN_ACCURACY = 0.85


@transformer
def transform(df, *args, **kwargs):
    """Train a DecisionTreeClassifier and return test predictions.

    Runtime variable: max_depth (int, default 3).
    Pass via: mage run iris_project iris_classifier --runtime-vars '{"max_depth": 3}'
    """
    max_depth = int(kwargs.get('max_depth', 3))
    print(f"Training DecisionTree with max_depth={max_depth}")

    train = df[df['split'] == 'train']
    test  = df[df['split'] == 'test']

    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(train[FEATURES], train[TARGET])

    predictions = model.predict(test[FEATURES])
    accuracy    = accuracy_score(test[TARGET], predictions)
    print(f"Test accuracy: {accuracy:.4f}")

    # Save the model so it can be loaded later (not committed — .pkl is gitignored)
    joblib.dump(model, 'iris_model.pkl')

    result = test[FEATURES + [TARGET]].copy()
    result['predicted'] = predictions
    result['correct']   = (result[TARGET] == result['predicted'])
    result['max_depth'] = max_depth
    result['test_accuracy'] = round(accuracy, 4)
    return result


@test
def test_accuracy(output, *args) -> None:
    """Gate: accuracy must be >= MIN_ACCURACY.
    
    If this @test raises, Mage stops here and save_results never runs.
    That prevents bad models from being saved — better than saving first
    and checking afterwards, because a bad CSV would already exist.
    """
    acc = output['test_accuracy'].iloc[0]
    assert acc >= MIN_ACCURACY, (
        f"Accuracy {acc:.4f} is below threshold {MIN_ACCURACY}. "
        f"Pipeline stopped — iris_predictions.csv will NOT be created."
    )
    print(f"train_model @test: OK — accuracy {acc:.4f} >= {MIN_ACCURACY}")
