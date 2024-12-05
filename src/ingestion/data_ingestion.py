import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Optional

load_dotenv()


class WeatherDataIngestor:
    """
    Class for ingesting weather data files into a database.
    """

    def __init__(self, db_url: str, table_name: str, file_extension: str = ".txt"):
        """
        :param db_url: Database connection URL
        :param table_name: Name of the database table
        :param file_extension: Extension of the weather data files
        """
        self.db_url = db_url
        self.table_name = table_name
        self.file_extension = file_extension
        self.engine = create_engine(db_url)

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def read_weather_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        :param file_path: Path to the weather data file
        :return: Cleaned DataFrame or None if an error occurs
        """
        try:
            self.logger.info(f"Reading file: {file_path}")
            df = pd.read_csv(
                file_path,
                sep="\t",
                header=None,
                names=["date", "max_temp", "min_temp", "precipitation"],
            )
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
            df["station_id"] = os.path.basename(file_path).split(".")[0]
            df = df.replace(-9999, pd.NA)

            # Drop rows with invalid dates
            df = df.dropna(subset=["date"])
            self.logger.info(
                f"Successfully processed file: {file_path} with {len(df)} valid records."
            )
            return df
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None

    def ingest_data_to_db(self, df: pd.DataFrame):
        """
        :param df: DataFrame to ingest
        """
        try:
            self.logger.info(
                f"Starting ingestion of {len(df)} records into table {self.table_name}."
            )
            with self.engine.begin() as conn:
                df.to_sql(
                    self.table_name,
                    conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                )
            self.logger.info(
                f"Successfully ingested {len(df)} records into table {self.table_name}."
            )
        except SQLAlchemyError as e:
            self.logger.error(f"Database ingestion failed: {e}")

    def process_file(self, file_path: str):
        """
        :param file_path: Path to the file
        """
        df = self.read_weather_file(file_path)
        if df is not None and not df.empty:
            self.ingest_data_to_db(df)
        else:
            self.logger.warning(f"No valid data found in file: {file_path}")

    def process_directory(self, directory_path: str):
        """
        :param directory_path: Path to the directory
        """
        self.logger.info(f"Processing directory: {directory_path}")
        if not os.path.isdir(directory_path):
            self.logger.error(f"Provided path is not a directory: {directory_path}")
            return

        files = [
            f for f in os.listdir(directory_path) if f.endswith(self.file_extension)
        ]
        if not files:
            self.logger.warning(
                f"No files with extension {self.file_extension} found in directory: {directory_path}"
            )
            return

        for file in files:
            self.process_file(os.path.join(directory_path, file))


if __name__ == "__main__":
    DB_URL = os.getenv(
        "DATABASE_URL", "postgresql://postgres:bhuvan@localhost:5432/assignment"
    )
    DATA_DIRECTORY = os.getenv("DATA_DIRECTORY", "/path/to/data/directory")
    TABLE_NAME = "weather_data"

    ingestor = WeatherDataIngestor(db_url=DB_URL, table_name=TABLE_NAME)
    ingestor.process_directory(DATA_DIRECTORY)
