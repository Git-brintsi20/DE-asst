# iris_project/data_exporters/save_results.py
# Part C1: data_exporter block — saves test predictions to CSV.
# This block only runs if train_model's @test passed (accuracy >= 0.85).
# If the @test failed, Mage stopped the pipeline and this file is never written.

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(df, *args, **kwargs):
    """Save the 30 test predictions to iris_predictions.csv.
    
    This only runs if train_model's accuracy @test passed.
    iris_predictions.csv is in .gitignore (*.csv) so it won't be committed.
    """
    df.to_csv('iris_predictions.csv', index=False)
    print(f"Saved {len(df)} predictions to iris_predictions.csv")
    print(f"Accuracy: {df['test_accuracy'].iloc[0]:.4f}")
