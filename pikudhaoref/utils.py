from __future__ import annotations

import json
import urllib.parse
import numpy as np
from typing import Any, Dict, Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pikudhaoref import City

__all__ = (
    "DEFAULT_PUBLIC_MAPBOX_KEY",
    "MIN_ZOOM_LEVEL",
    "MAX_ZOOM_LEVEL",
    "create_map_url",
    "create_marker_dict",
    "determine_zoom_level",
    "create_map_url_from_cities"
)

DEFAULT_PUBLIC_MAPBOX_KEY = "pk.eyJ1IjoiYWRhbTcxMDAiLCJhIjoiY2t2cGVlNGRsNjJoNzJxb2t6Z2U1M3g0aCJ9.3VXThhkllBpccpMfLflN2A"
MAX_ZOOM_LEVEL = 11
MIN_ZOOM_LEVEL = 6


def create_map_url(
    geojson: Dict[str, Any],
    access_token: str,
    center: Tuple[float, float],
    zoom_level: int,
) -> str:
    center = ",".join([str(x) for x in center])
    geojson = urllib.parse.quote(json.dumps(geojson))

    return (
        f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
        f"geojson({geojson})/{center},{zoom_level}/500x500?access_token={access_token}"
    )


def create_marker_dict(
    color: str, marker_size: str, lat: float, lng: float
) -> Dict[str, Any]:
    return {
        "type": "Feature",
        "properties": {
            "marker-color": color,
            "marker-size": marker_size,
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat],
        },
    }


def determine_zoom_level(
    locations: List[Tuple[float, float]]
) -> Tuple[float, Tuple[float, float]]:
    latitudes = [x[0] for x in locations]
    longitudes = [x[1] for x in locations]

    height = max(latitudes) - min(latitudes)
    width = max(longitudes) - min(longitudes)
    center = (float(np.mean(latitudes)), float(np.mean(longitudes)))

    area = height * width

    zoom: float = np.interp(
        area,
        [0, 5 ** -10, 4 ** -10, 3 ** -10, 2 ** -10, 1 ** -10, 1 ** -5],
        [20, 17, 16, 15, 14, 7, 5],
    )

    return zoom - 4, center


def create_map_url_from_cities(cities: List[City], access_token: str = None) -> str:
    access_token = access_token or DEFAULT_PUBLIC_MAPBOX_KEY

    geojson = {"type": "FeatureCollection", "features": []}
    for city in cities:
        geojson["features"].append(
            create_marker_dict(
                color="#ff0000", marker_size="medium", lat=city.lat, lng=city.lng
            )
        )

    locations = [(city.lng, city.lat) for city in cities]
    zoom_level, center = determine_zoom_level(locations)

    return create_map_url(
        geojson,
        access_token,
        center,
        max(min(int(zoom_level), MAX_ZOOM_LEVEL), MIN_ZOOM_LEVEL),
    )
