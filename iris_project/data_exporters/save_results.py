# iris_project/data_exporters/save_results.py
# Part C1: data_exporter — saves test predictions to CSV.
# Only runs if train_model's @test passed (accuracy >= 0.85).

if 'data_exporter' not in dir():
    try:
        from mage_ai.data_preparation.decorators import data_exporter
    except ImportError:
        def data_exporter(fn): return fn  # noqa


@data_exporter
def export_data(df, *args, **kwargs):
    """Save 30 test predictions to iris_predictions.csv."""
    df.to_csv('iris_predictions.csv', index=False)
    print(f"Saved {len(df)} predictions to iris_predictions.csv")
    print(f"Accuracy: {df['test_accuracy'].iloc[0]:.4f}")
