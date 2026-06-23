import pandas as pd
import numpy as np


# ── Hilfsfunktionen (spiegeln Notebook-Logik) ────────────────────────────────

def compute_mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean(np.abs(actual - predicted)))


def compute_rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((actual - predicted) ** 2)))


def resample_to_monthly(df: pd.DataFrame, col: str) -> pd.Series:
    return df[col].resample("ME").mean()


def load_prediction_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df.set_index("date")


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestMetrics:
    def test_mae_perfect(self):
        a = np.array([1.0, 2.0, 3.0])
        assert compute_mae(a, a) == 0.0

    def test_mae_known_value(self):
        actual = np.array([10.0, 20.0, 30.0])
        predicted = np.array([12.0, 18.0, 33.0])
        assert abs(compute_mae(actual, predicted) - 7 / 3) < 1e-9

    def test_rmse_perfect(self):
        a = np.array([5.0, 10.0, 15.0])
        assert compute_rmse(a, a) == 0.0

    def test_rmse_greater_than_mae(self):
        actual = np.array([1.0, 1.0, 1.0, 10.0])
        predicted = np.array([1.0, 1.0, 1.0, 0.0])
        assert compute_rmse(actual, predicted) > compute_mae(actual, predicted)


class TestResampling:
    def test_monthly_reduces_rows(self):
        idx = pd.date_range("2010-01-01", "2020-12-31", freq="D")
        df = pd.DataFrame({"value": np.random.rand(len(idx))}, index=idx)
        assert len(resample_to_monthly(df, "value")) < len(df)

    def test_monthly_no_nan(self):
        idx = pd.date_range("2015-01-01", "2015-12-31", freq="D")
        df = pd.DataFrame({"value": np.ones(len(idx))}, index=idx)
        assert not resample_to_monthly(df, "value").isna().any()


class TestDataLoading:
    def test_waterlevel_loads(self):
        df = load_prediction_csv("data/prediction/prediction_waterlevel.csv")
        assert isinstance(df.index, pd.DatetimeIndex)
        assert len(df) > 0

    def test_rain_loads(self):
        df = load_prediction_csv("data/prediction/prediction_rain.csv")
        assert isinstance(df.index, pd.DatetimeIndex)

    def test_temperature_loads(self):
        df = load_prediction_csv("data/prediction/prediction_temperature_mean.csv")
        assert isinstance(df.index, pd.DatetimeIndex)

    def test_discharge_loads(self):
        df = load_prediction_csv("data/prediction/prediction_discharge_vol.csv")
        assert isinstance(df.index, pd.DatetimeIndex)
