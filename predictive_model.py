from __future__ import annotations

import pickle
from pathlib import Path
from typing import Union

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "ai4i2020.csv"
DEFAULT_MODEL_PATH = BASE_DIR / "model" / "predictive_maintenance_model.pkl"

FEATURE_COLUMNS = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
CATEGORICAL_COLUMNS = ["Type"]
NUMERIC_COLUMNS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]


def _build_model() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLUMNS,
            ),
            (
                "num",
                StandardScaler(),
                NUMERIC_COLUMNS,
            ),
        ]
    )

    classifier = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def train_model(
    model_path: Union[str, Path] = DEFAULT_MODEL_PATH,
    data_path: Union[str, Path] = DEFAULT_DATA_PATH,
):
    df = pd.read_csv(data_path)
    required_columns = [*FEATURE_COLUMNS, "Machine failure"]
    missing_columns = sorted(set(required_columns) - set(df.columns))
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {', '.join(missing_columns)}"
        )
    if df.empty:
        raise ValueError(f"Dataset contains no rows: {data_path}")

    X = df[FEATURE_COLUMNS]
    y = df["Machine failure"]

    model = _build_model()
    model.fit(X, y)

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    with model_path.open("wb") as handle:
        pickle.dump(model, handle)

    return model


def get_model(
    model_path: Union[str, Path] = DEFAULT_MODEL_PATH,
    data_path: Union[str, Path] = DEFAULT_DATA_PATH,
):
    model_path = Path(model_path)
    if model_path.exists():
        try:
            with model_path.open("rb") as handle:
                return pickle.load(handle)
        except Exception:
            pass

    return train_model(model_path=model_path, data_path=data_path)


def predict_failure_risk(
    machine_type: str,
    air_temperature: float,
    process_temperature: float,
    rotational_speed: float,
    torque: float,
    tool_wear: float,
):
    model = get_model()

    row = pd.DataFrame(
        [{
            "Type": machine_type,
            "Air temperature [K]": air_temperature,
            "Process temperature [K]": process_temperature,
            "Rotational speed [rpm]": rotational_speed,
            "Torque [Nm]": torque,
            "Tool wear [min]": tool_wear,
        }]
    )

    probability = float(model.predict_proba(row)[0, 1])
    label = "High Risk" if probability >= 0.5 else "Low Risk"

    return {
        "probability": probability,
        "label": label,
    }
