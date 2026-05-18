from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


def chronological_split(
    df: pd.DataFrame,
    split_date: str = "2023-10-01",
    date_col: str = "date",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a temporal dataset into train rows before split_date and test rows after."""
    dates = pd.to_datetime(df[date_col])
    train_df = df.loc[dates < pd.Timestamp(split_date)].copy()
    test_df = df.loc[dates >= pd.Timestamp(split_date)].copy()
    return train_df, test_df


def evaluate_binary_classifier(model, x_test, y_test) -> dict:
    """Return common binary classification metrics."""
    y_pred = model.predict(x_test)
    metrics = {
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }

    if hasattr(model, "predict_proba") and pd.Series(y_test).nunique() == 2:
        y_score = model.predict_proba(x_test)[:, 1]
        metrics["roc_auc"] = roc_auc_score(y_test, y_score)
    else:
        metrics["roc_auc"] = None

    return metrics


def save_model(model, output_path: str | Path) -> Path:
    """Save a fitted model with joblib."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path
