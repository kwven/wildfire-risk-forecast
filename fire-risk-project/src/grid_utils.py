from __future__ import annotations

from pathlib import Path

import geopandas as gpd
from shapely.geometry import box


def create_bbox_grid(
    west: float,
    south: float,
    east: float,
    north: float,
    grid_size: float,
    crs: str = "EPSG:4326",
) -> gpd.GeoDataFrame:
    """Create a rectangular lon/lat grid covering a bounding box."""
    records = []
    grid_id = 0
    y = south
    while y < north:
        x = west
        y2 = min(y + grid_size, north)
        while x < east:
            x2 = min(x + grid_size, east)
            records.append(
                {
                    "grid_id": grid_id,
                    "west": x,
                    "south": y,
                    "east": x2,
                    "north": y2,
                    "geometry": box(x, y, x2, y2),
                }
            )
            grid_id += 1
            x = round(x + grid_size, 10)
        y = round(y + grid_size, 10)

    return gpd.GeoDataFrame(records, geometry="geometry", crs=crs)


def save_grid(grid: gpd.GeoDataFrame, output_path: str | Path) -> Path:
    """Save a grid to GeoJSON and return the output path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    grid.to_file(output_path, driver="GeoJSON")
    return output_path
