import logging
import statistics
from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List

import requests

from .constants import LIMIT, POKEAPI_URL, TIMEOUT
from .exceptions import PokeAPIError, StatisticsCalculationError

logger = logging.getLogger()


class PokeAPI:
    def __init__(self):
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def _get(self, url: str) -> Dict[str, Any]:
        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception(
                f"Error fetching data from {url}: {e.__class__.__name__}: {e}"
            )
            raise PokeAPIError(
                f"Error fetching data from {url}: {e.__class__.__name__}: {e}"
            ) from e

    def get_all_berries(self) -> List[Dict[str, Any]]:
        url = f"{POKEAPI_URL}?limit={LIMIT}"
        data = self._get(url)
        return data.get("results", [])

    def get_berry_growth_time(self, url: str) -> int:
        data = self._get(url)
        return data.get("growth_time", 0)


@dataclass
class BerryData:
    names: List[str]
    growth_times: List[int]
    growth_statistics: Dict[str, Any]

    def to_json(self) -> str:
        return {
            "berry_names": self.names,
            "growth_times": self.growth_times,
            "growth_statistics": self.growth_statistics,
        }


def _calculate_growth_statistics(growth_times: List[int]) -> Dict[str, Any]:
    try:
        c = Counter(growth_times)
        mode_growth_time = c.most_common(1)[0][0] if c else None
        return {
            "min_growth_time": min(growth_times),
            "max_growth_time": max(growth_times),
            "median_growth_time": statistics.median(growth_times),
            "mean_growth_time": statistics.mean(growth_times),
            "mode_growth_time": mode_growth_time,
            "variance_growth_time": statistics.variance(growth_times),
            "standard_deviation_growth_time": statistics.stdev(growth_times),
        }
    except statistics.StatisticsError as e:
        logger.exception(f"Error calculating statistics: {e.__class__.__name__}: {e}")
        raise StatisticsCalculationError(
            f"Error calculating statistics: {e.__class__.__name__}: {e}"
        ) from e


def fetch_all_berry_data() -> BerryData:
    with PokeAPI() as pokeapi:
        berries = pokeapi.get_all_berries()
        growth_times = [
            pokeapi.get_berry_growth_time(berry["url"]) for berry in berries
        ]
        return BerryData(
            names=[berry["name"] for berry in berries],
            growth_times=growth_times,
            growth_statistics=_calculate_growth_statistics(growth_times),
        )
