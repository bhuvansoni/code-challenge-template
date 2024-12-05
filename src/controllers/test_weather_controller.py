import unittest
from unittest.mock import MagicMock
from datetime import datetime
from models.weather_data import WeatherData
from controllers.weather_controller import get_weather_data


class TestGetWeatherData(unittest.TestCase):
    def test_get_weather_data_with_station_id(self):
        mock_data = [
            MagicMock(
                station_id="ST001",
                date=datetime(2024, 12, 5),
                max_temp=300,
                min_temp=290,
                precipitation=50,
            ),
            MagicMock(
                station_id="ST001",
                date=datetime(2024, 12, 6),
                max_temp=305,
                min_temp=295,
                precipitation=40,
            ),
        ]

        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_query
        mock_query.paginate.return_value.items = mock_data

        WeatherData.query = mock_query

        result = get_weather_data(station_id="ST001", page=1, per_page=10)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["station_id"], "ST001")

        # Strip the time part and ensure the date is formatted correctly
        formatted_date = result[0]["date"].split("T")[0]
        self.assertEqual(formatted_date, "2024-12-05")  # Ensure date format matches

        self.assertEqual(result[0]["max_temp"], 30.0)
        self.assertEqual(result[0]["min_temp"], 29.0)
        self.assertEqual(result[0]["precipitation"], 5.0)

    def test_get_weather_data_without_station_id(self):
        mock_data = [
            MagicMock(
                station_id="ST001",
                date=datetime(2024, 12, 5),
                max_temp=300,
                min_temp=290,
                precipitation=50,
            )
        ]

        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_query
        mock_query.paginate.return_value.items = mock_data

        WeatherData.query = mock_query

        result = get_weather_data(page=1, per_page=10)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["station_id"], "ST001")

        # Strip time part from result
        formatted_date = result[0]["date"].split("T")[0]
        self.assertEqual(formatted_date, "2024-12-05")

        self.assertEqual(result[0]["max_temp"], 30.0)
        self.assertEqual(result[0]["min_temp"], 29.0)
        self.assertEqual(result[0]["precipitation"], 5.0)


if __name__ == "__main__":
    unittest.main()
