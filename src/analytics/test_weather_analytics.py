import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from weather_analytics import WeatherStatsCalculator 

@pytest.fixture
def mock_engine():
    """Fixture to mock SQLAlchemy engine."""
    with patch("weather_analytics.create_engine") as mock_engine:
        yield mock_engine

@pytest.fixture
def calculator(mock_engine):
    """Fixture to initialize WeatherStatsCalculator with a mock engine."""
    return WeatherStatsCalculator(db_url="mock_db_url", stats_table="weather_stats")

def test_fetch_weather_data_success(calculator, mock_engine):
    """Test fetching weather data successfully."""
    mock_df = pd.DataFrame({
        "station_id": [1, 2],
        "year": [2023, 2023],
        "avg_max_temp": [30.5, 29.5],
        "avg_min_temp": [15.2, 14.8],
        "total_precipitation": [120.0, 85.0],
    })
    mock_engine.return_value.connect.return_value.execute.return_value.fetchall.return_value = mock_df

    with patch("pandas.read_sql", return_value=mock_df) as mock_read_sql:
        result = calculator.fetch_weather_data()
        mock_read_sql.assert_called_once()
        pd.testing.assert_frame_equal(result, mock_df)

def test_store_weather_stats_success(calculator, mock_engine):
    """Test storing weather stats successfully."""
    mock_df = pd.DataFrame({
        "station_id": [1, 2],
        "year": [2023, 2023],
        "avg_max_temp": [30.5, 29.5],
        "avg_min_temp": [15.2, 14.8],
        "total_precipitation": [120.0, 85.0],
    })
    mock_engine.return_value.begin.return_value.__enter__.return_value = MagicMock()

    with patch.object(mock_df, "to_sql") as mock_to_sql:
        calculator.store_weather_stats(mock_df)
        mock_to_sql.assert_called_once_with(
            "weather_stats", mock_engine.return_value.begin.return_value.__enter__.return_value, if_exists="append", index=False
        )

def test_store_weather_stats_failure(calculator, mock_engine):
    """Test failure during storing weather stats."""
    mock_df = pd.DataFrame({
        "station_id": [1, 2],
        "year": [2023, 2023],
        "avg_max_temp": [30.5, 29.5],
        "avg_min_temp": [15.2, 14.8],
        "total_precipitation": [120.0, 85.0],
    })
    mock_engine.return_value.begin.side_effect = SQLAlchemyError("DB Error")

    with pytest.raises(SQLAlchemyError):
        calculator.store_weather_stats(mock_df)

def test_calculate_and_store_stats_success(calculator):
    """Test calculate and store stats end-to-end."""
    mock_df = pd.DataFrame({
        "station_id": [1, 2],
        "year": [2023, 2023],
        "avg_max_temp": [30.5, 29.5],
        "avg_min_temp": [15.2, 14.8],
        "total_precipitation": [120.0, 85.0],
    })

    with patch.object(calculator, "fetch_weather_data", return_value=mock_df) as mock_fetch, \
         patch.object(calculator, "store_weather_stats") as mock_store:
        calculator.calculate_and_store_stats()
        mock_fetch.assert_called_once()
        mock_store.assert_called_once_with(mock_df)

def test_calculate_and_store_stats_no_data(calculator):
    """Test calculate and store stats with no data."""
    mock_df = pd.DataFrame()

    with patch.object(calculator, "fetch_weather_data", return_value=mock_df) as mock_fetch, \
         patch.object(calculator, "store_weather_stats") as mock_store:
        calculator.calculate_and_store_stats()
        mock_fetch.assert_called_once()
        mock_store.assert_not_called()

def test_calculate_and_store_stats_failure(calculator):
    """Test calculate and store stats with failure during fetch."""
    with patch.object(calculator, "fetch_weather_data", side_effect=Exception("Fetch error")) as mock_fetch:
        with pytest.raises(Exception):
            calculator.calculate_and_store_stats()
        mock_fetch.assert_called_once()
