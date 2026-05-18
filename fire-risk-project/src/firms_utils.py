from __future__ import annotations

import io
import time
from datetime import date, timedelta
from typing import Iterable

import pandas as pd
import requests
from tqdm.auto import tqdm


def chunk_start_dates(year: int, chunk_days: int = 5) -> Iterable[date]:
    """Yield start dates for short FIRMS area API requests."""
    current = date(year, 1, 1)
    end = date(year, 12, 31)
    while current <= end:
        yield current
        current += timedelta(days=chunk_days)


def build_firms_area_url(
    map_key: str,
    source: str,
    bbox: str,
    day_range: int,
    start_date: date,
) -> str:
    """Build a NASA FIRMS area API CSV URL."""
    return (
        "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{map_key}/{source}/{bbox}/{day_range}/{start_date:%Y-%m-%d}"
    )


def download_firms_year(
    year: int,
    map_key: str,
    source: str,
    bbox: str,
    day_range: int = 5,
    sleep_seconds: float = 0.5,
    timeout_seconds: int = 60,
) -> pd.DataFrame:
    """Download one year of FIRMS area API records in short chunks."""
    frames: list[pd.DataFrame] = []
    starts = list(chunk_start_dates(year, day_range))

    for start_date in tqdm(starts, desc=f"FIRMS {year}"):
        url = build_firms_area_url(map_key, source, bbox, day_range, start_date)
        try:
            response = requests.get(url, timeout=timeout_seconds)
            response.raise_for_status()
            text = response.text.strip()
            if not text or text.lower().startswith("no"):
                continue
            chunk = pd.read_csv(io.StringIO(text))
            chunk["request_start_date"] = pd.Timestamp(start_date)
            frames.append(chunk)
        except Exception as exc:
            print(f"Skipped FIRMS chunk starting {start_date:%Y-%m-%d}: {exc}")
        time.sleep(sleep_seconds)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True).drop_duplicates()
