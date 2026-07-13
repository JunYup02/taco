"""Train the listing-text scam model on synthetic data and save the artifact.

Run from backend/: python -m ml.train_listing_model
"""
from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score

from ml.synthetic_data import generate_listing_dataset

ARTIFACT_PATH = Path(__file__).parent / "artifacts" / "listing_model.joblib"


def main():
    X, y = generate_listing_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(X_train, y_train)

    probs = pipeline.predict_proba(X_test)[:, 1]
    preds = pipeline.predict(X_test)
    print(f"listing model  AUC={roc_auc_score(y_test, probs):.3f}  "
          f"accuracy={accuracy_score(y_test, preds):.3f}")

    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, ARTIFACT_PATH)
    print(f"saved {ARTIFACT_PATH}")


if __name__ == "__main__":
    main()
