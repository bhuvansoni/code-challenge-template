import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging


class WeatherStatsCalculator:

    def __init__(self, db_url: str, stats_table: str = "weather_stats"):
        """
        :param db_url: Database connection URL
        :param stats_table: Name of the table to store calculated statistics
        """
        self.db_url = db_url
        self.stats_table = stats_table
        self.engine = create_engine(db_url)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def fetch_weather_data(self) -> pd.DataFrame:
        """
        Fetch aggregated weather statistics from the database.
        :return: DataFrame containing weather statistics
        """
        query = """
            SELECT station_id, 
                   EXTRACT(YEAR FROM date) AS year, 
                   AVG(max_temp) / 10.0 AS avg_max_temp,
                   AVG(min_temp) / 10.0 AS avg_min_temp,
                   SUM(precipitation) / 100.0 AS total_precipitation
            FROM weather_data
            GROUP BY station_id, year
        """
        try:
            self.logger.info("Fetching weather data from the database.")
            return pd.read_sql(query, self.engine)
        except SQLAlchemyError as e:
            self.logger.error(f"Error fetching weather data: {e}")
            raise

    def store_weather_stats(self, stats_df: pd.DataFrame):
        """
        :param stats_df: DataFrame containing weather statistics
        """
        try:
            self.logger.info(
                f"Storing weather statistics into table: {self.stats_table}."
            )
            with self.engine.begin() as conn:
                stats_df.to_sql(self.stats_table, conn, if_exists="append", index=False)
            self.logger.info("Weather statistics stored successfully.")
        except SQLAlchemyError as e:
            self.logger.error(f"Error storing weather statistics: {e}")
            raise

    def calculate_and_store_stats(self):
        try:
            self.logger.info("Starting weather statistics calculation.")
            stats_df = self.fetch_weather_data()
            if stats_df.empty:
                self.logger.warning("No data available for statistics calculation.")
            else:
                self.store_weather_stats(stats_df)
                self.logger.info(
                    "Weather statistics calculation and storage completed."
                )
        except Exception as e:
            self.logger.error(f"Error during statistics calculation: {e}")
            raise


if __name__ == "__main__":
    load_dotenv()

    DB_URL = os.getenv(
        "DATABASE_URL", "postgresql://postgres:bhuvan@localhost:5432/assignment"
    )
    STATS_TABLE = "weather_stats"

    calculator = WeatherStatsCalculator(db_url=DB_URL, stats_table=STATS_TABLE)
    calculator.calculate_and_store_stats()
