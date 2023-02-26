from unittest.mock import MagicMock

import pytest

from .util import BerryData, PokeAPI, _calculate_growth_statistics, fetch_all_berry_data


@pytest.fixture()
def mock_session(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr("berries.util.requests.Session", lambda: mock_session)
    return mock_session


@pytest.fixture()
def pokeapi(mock_session):
    return PokeAPI()


def test_pokeapi_get_all_berries(pokeapi, mock_session):
    mock_session.get.return_value.json.return_value = {
        "results": [{"name": "berry1", "url": "url1"}]
    }
    berries = pokeapi.get_all_berries()
    assert len(berries) == 1
    assert berries[0]["name"] == "berry1"
    assert berries[0]["url"] == "url1"


def test_pokeapi_get_berry_growth_time(pokeapi, mock_session):
    mock_session.get.return_value.json.return_value = {"growth_time": 10}
    growth_time = pokeapi.get_berry_growth_time("url1")
    assert growth_time == 10


def test_calculate_growth_statistics():
    growth_times = [1, 2, 3, 4, 5]
    stats = _calculate_growth_statistics(growth_times)
    assert stats["min_growth_time"] == 1
    assert stats["max_growth_time"] == 5
    assert stats["median_growth_time"] == 3
    assert stats["mean_growth_time"] == 3
    assert stats["mode_growth_time"] is None
    assert stats["variance_growth_time"] == 2.5
    assert stats["standard_deviation_growth_time"] == pytest.approx(1.5811, abs=1e-4)


def test_fetch_all_berry_data(pokeapi, mock_session):
    mock_session.get.return_value.json.side_effect = [
        {
            "results": [
                {"name": "berry1", "url": "url1"},
                {"name": "berry2", "url": "url2"},
            ]
        },
        {"growth_time": 10},
        {"growth_time": 20},
    ]
    data = fetch_all_berry_data()
    assert isinstance(data, BerryData)
    assert data.names == ["berry1", "berry2"]
    assert data.growth_times == [10, 20]
    assert data.growth_statistics["min_growth_time"] == 10
    assert data.growth_statistics["max_growth_time"] == 20
    assert data.growth_statistics["median_growth_time"] == 15
    assert data.growth_statistics["mean_growth_time"] == 15
    assert data.growth_statistics["mode_growth_time"] is None
    assert data.growth_statistics["variance_growth_time"] == pytest.approx(50, abs=1e-3)
    assert data.growth_statistics["standard_deviation_growth_time"] == pytest.approx(
        7.03, rel=0.01
    )
