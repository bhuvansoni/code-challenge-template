from flask_restx import Namespace, Resource, fields
from flask import request
from controllers.weather_controller import get_weather_data
from controllers.stats_controller import get_weather_stats

weather_bp = Namespace("weather", description="Weather data operations")


@weather_bp.route("/")
class Weather(Resource):
    @weather_bp.param("station_id", "Station ID", type=str, required=True)
    @weather_bp.param(
        "date", "Date in ISO format (YYYY-MM-DD)", type=str, required=True
    )
    @weather_bp.param("page", "Page number for pagination", type=int, default=1)
    def get(self):
        """
        Get weather data by station_id and date.
        """
        station_id = request.args.get("station_id")
        date = request.args.get("date")
        page = request.args.get("page", 1, type=int)

        data = get_weather_data(station_id, date, page)
        return data, 200


@weather_bp.route("/stats")
class WeatherStats(Resource):
    @weather_bp.param("station_id", "Station ID", type=str, required=True)
    @weather_bp.param("year", "Year for weather statistics", type=int, required=True)
    @weather_bp.param("page", "Page number for pagination", type=int, default=1)
    def get(self):
        """
        Get weather statistics for a station for a specific year.
        """
        station_id = request.args.get("station_id")
        year = request.args.get("year", type=int)
        page = request.args.get("page", 1, type=int)

        data = get_weather_stats(station_id, year, page)
        return data, 200
