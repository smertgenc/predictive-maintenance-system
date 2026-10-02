import pytest

from predictive_model import (
    DEFAULT_DATA_PATH,
    predict_failure_risk,
    train_model,
)


def test_default_dataset_path_uses_data_directory():
    assert DEFAULT_DATA_PATH.name == "ai4i2020.csv"
    assert DEFAULT_DATA_PATH.parent.name == "data"


def test_predict_failure_risk_returns_probability():
    result = predict_failure_risk(
        machine_type="M",
        air_temperature=298.1,
        process_temperature=308.6,
        rotational_speed=1551,
        torque=42.8,
        tool_wear=0,
    )

    assert 0.0 <= result["probability"] <= 1.0
    assert result["label"] in {"Low Risk", "High Risk"}


def test_train_model_creates_model_file(tmp_path):
    model_path = tmp_path / "trained_model.pkl"
    model = train_model(model_path=model_path)

    assert model is not None
    assert model_path.exists()


def test_train_model_rejects_dataset_without_required_columns(tmp_path):
    data_path = tmp_path / "invalid.csv"
    data_path.write_text("some column\nvalue\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        train_model(model_path=tmp_path / "model.pkl", data_path=data_path)
