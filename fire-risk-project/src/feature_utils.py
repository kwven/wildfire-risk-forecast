from __future__ import annotations

import pandas as pd


def build_daily_panel(grid_ids, start_date: str, end_date: str) -> pd.DataFrame:
    """Create all grid_id and daily date combinations."""
    dates = pd.date_range(start_date, end_date, freq="D")
    return pd.MultiIndex.from_product(
        [grid_ids, dates],
        names=["grid_id", "date"],
    ).to_frame(index=False)


def future_fire_count(series: pd.Series, horizon_days: int = 7) -> pd.Series:
    """Sum future fire counts from tomorrow through the forecast horizon."""
    shifted = [series.shift(-offset) for offset in range(1, horizon_days + 1)]
    return pd.concat(shifted, axis=1).sum(axis=1, min_count=horizon_days)


def add_no_leakage_features(panel: pd.DataFrame) -> pd.DataFrame:
    """Add calendar, lag, and rolling features that only use past information."""
    panel = panel.sort_values(["grid_id", "date"]).copy()
    grouped_fire = panel.groupby("grid_id")["fire_count"]
    grouped_ndvi = panel.groupby("grid_id")["ndvi"]

    panel["month"] = panel["date"].dt.month
    panel["dayofyear"] = panel["date"].dt.dayofyear
    panel["fire_count_lag_1d"] = grouped_fire.shift(1)
    panel["fire_count_past_7d"] = grouped_fire.transform(
        lambda s: s.shift(1).rolling(7, min_periods=1).sum()
    )
    panel["fire_count_past_30d"] = grouped_fire.transform(
        lambda s: s.shift(1).rolling(30, min_periods=1).sum()
    )
    panel["ndvi_lag_16d"] = grouped_ndvi.shift(16)
    panel["ndvi_change_16d"] = panel["ndvi"] - panel["ndvi_lag_16d"]

    return panel


def add_next_7d_target(panel: pd.DataFrame) -> pd.DataFrame:
    """Add next-7-day fire count and binary fire risk target."""
    panel = panel.sort_values(["grid_id", "date"]).copy()
    panel["fire_next_7d_count"] = panel.groupby("grid_id")["fire_count"].transform(
        lambda s: future_fire_count(s, horizon_days=7)
    )
    panel["fire_risk_label"] = (panel["fire_next_7d_count"] > 0).astype("Int64")
    panel.loc[panel["fire_next_7d_count"].isna(), "fire_risk_label"] = pd.NA
    return panel
