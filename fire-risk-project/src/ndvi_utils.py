from __future__ import annotations

import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
from tqdm.auto import tqdm


def list_ndvi_files(ndvi_dir: str | Path) -> list[Path]:
    """Return sorted MODIS NDVI GeoTIFF files, excluding VI quality rasters."""
    return sorted(Path(ndvi_dir).glob("*NDVI*.tif"))


def extract_date_from_ndvi_filename(path: str | Path) -> pd.Timestamp:
    """Parse a MODIS date like 20230101 from a file name."""
    match = re.search(r"(\d{8})T\d{6}", Path(path).name)
    if not match:
        raise ValueError(f"Could not parse NDVI date from {path}")
    return pd.to_datetime(match.group(1), format="%Y%m%d")


def scale_and_clean_ndvi(raw_mean: pd.Series) -> pd.Series:
    """Apply MODIS NDVI scale factor and mask invalid values."""
    ndvi = raw_mean.astype(float) * 0.0001
    return ndvi.mask((ndvi < -0.2) | (ndvi > 1.0), np.nan)


def extract_ndvi_grid_timeseries(
    grid: gpd.GeoDataFrame,
    ndvi_files: list[Path],
    all_touched: bool = True,
) -> pd.DataFrame:
    """Extract mean raw NDVI for each grid cell and NDVI raster date."""
    records = []

    for tif_path in tqdm(ndvi_files, desc="Extracting NDVI"):
        ndvi_date = extract_date_from_ndvi_filename(tif_path)
        with rasterio.open(tif_path) as src:
            raster_crs = src.crs
            nodata = src.nodata

        zones = grid.to_crs(raster_crs) if raster_crs and grid.crs != raster_crs else grid
        stats = zonal_stats(
            zones,
            str(tif_path),
            stats=["mean"],
            nodata=nodata,
            all_touched=all_touched,
        )

        for grid_id, item in zip(grid["grid_id"], stats):
            records.append(
                {
                    "grid_id": grid_id,
                    "date": ndvi_date,
                    "ndvi_raw_mean": item.get("mean"),
                }
            )

    output = pd.DataFrame(records)
    if not output.empty:
        output["ndvi"] = scale_and_clean_ndvi(output["ndvi_raw_mean"])
    return output
