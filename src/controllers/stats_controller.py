from models.weather_stats import WeatherStats


def get_weather_stats(station_id=None, year=None, page=1, per_page=10):
    query = WeatherStats.query
    if station_id:
        query = query.filter_by(station_id=station_id)
    if year:
        query = query.filter_by(year=year)

    data = query.paginate(page=page, per_page=per_page).items
    return [
        {
            "station_id": s.station_id,
            "year": s.year,
            "avg_max_temp": s.avg_max_temp,
            "avg_min_temp": s.avg_min_temp,
            "total_precipitation": s.total_precipitation,
        }
        for s in data
    ]
