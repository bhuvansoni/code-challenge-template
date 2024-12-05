import unittest
from unittest.mock import MagicMock
from models.weather_stats import WeatherStats
from controllers.stats_controller import get_weather_stats  # Import your function

class TestGetWeatherStats(unittest.TestCase):

    def test_get_weather_stats_with_station_id(self):
        mock_data = [
            MagicMock(
                station_id="ST001",
                year=2024,
                avg_max_temp=300,
                avg_min_temp=290,
                total_precipitation=50
            ),
            MagicMock(
                station_id="ST001",
                year=2025,
                avg_max_temp=305,
                avg_min_temp=295,
                total_precipitation=40
            )
        ]
        
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_query
        mock_query.paginate.return_value.items = mock_data
        
        WeatherStats.query = mock_query
        
        result = get_weather_stats(station_id="ST001", year=2024, page=1, per_page=10)
        
        self.assertEqual(result[0]["station_id"], "ST001")
        self.assertEqual(result[0]["year"], 2024)
        self.assertEqual(result[0]["avg_max_temp"], 300)
        self.assertEqual(result[0]["avg_min_temp"], 290)
        self.assertEqual(result[0]["total_precipitation"], 50)

    def test_get_weather_stats_without_station_id(self):
        mock_data = [
            MagicMock(
                station_id="ST001",
                year=2024,
                avg_max_temp=300,
                avg_min_temp=290,
                total_precipitation=50
            )
        ]
        
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_query
        mock_query.paginate.return_value.items = mock_data
        
        WeatherStats.query = mock_query
        
        result = get_weather_stats(page=1, per_page=10)
        
        self.assertEqual(result[0]["station_id"], "ST001")
        self.assertEqual(result[0]["year"], 2024)
        self.assertEqual(result[0]["avg_max_temp"], 300)
        self.assertEqual(result[0]["avg_min_temp"], 290)
        self.assertEqual(result[0]["total_precipitation"], 50)

    def test_get_weather_stats_with_year_filter(self):
        mock_data = [
            MagicMock(
                station_id="ST001",
                year=2024,
                avg_max_temp=300,
                avg_min_temp=290,
                total_precipitation=50
            )
        ]
        
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_query
        mock_query.paginate.return_value.items = mock_data
        
        WeatherStats.query = mock_query
        
        result = get_weather_stats(year=2024, page=1, per_page=10)
        
        self.assertEqual(result[0]["station_id"], "ST001")
        self.assertEqual(result[0]["year"], 2024)
        self.assertEqual(result[0]["avg_max_temp"], 300)
        self.assertEqual(result[0]["avg_min_temp"], 290)
        self.assertEqual(result[0]["total_precipitation"], 50)

if __name__ == "__main__":
    unittest.main()
