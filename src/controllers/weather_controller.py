from models.weather_data import WeatherData


def get_weather_data(station_id=None, date=None, page=1, per_page=10):
    query = WeatherData.query
    if station_id:
        query = query.filter_by(station_id=station_id)
    if date:
        query = query.filter_by(date=date)

    data = query.paginate(page=page, per_page=per_page).items
    return [
        {
            "station_id": d.station_id,
            "date": d.date.isoformat(),
            "max_temp": d.max_temp / 10 if d.max_temp else None,
            "min_temp": d.min_temp / 10 if d.min_temp else None,
            "precipitation": d.precipitation / 10 if d.precipitation else None,
        }
        for d in data
    ]
