import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pathlib import Path

def train_and_score(input_parquet, output_parquet):
    
    print(f"Loading features from {input_parquet.name}...")
    df = pd.read_parquet(input_parquet)

    # These lines convert time features into sine and cosine transformations.
    # This is to prevent the forest from assuming that 23:00 and 00:00 are far apart instead of just an hour.
    df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7.0)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7.0)


    # For scaling purposes we are isolating numerical features
    numeric_features = ["subject_length", "body_length", "has_bcc", "recipient_count", "hour_of_day", "day_of_week"] 
    X = df[numeric_features]

    # This portion here prevents features such as body length from being weighted too much compared to other features.
    print("Scaling features...")
    scalar = StandardScaler()
    X_scaled = scalar.fit_transform(X)

    # n_estimators = 200 ensures that our anomaly scores remain consistant across multiple runs
    print("Training Isolation Forest...")
    clf = IsolationForest(
        n_estimators=200,
        max_samples='auto',
        random_state=42
    )
    

    clf.fit(X_scaled)
    df['anomaly_score'] = clf.decision_function(X_scaled) # Lower the number, the more notable the anomaly is; higher scores is normal behaviour or what is considered the status quo of the business.

    df.to_parquet(output_parquet)
    print(f"Scoring Done. File saved to {output_parquet.name}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    input_file = BASE_DIR / "deliverables" / "enron_raw_features.parquet"
    output_file = BASE_DIR / "deliverables" / "enron_scored_features.parquet"

    train_and_score(input_file, output_file)