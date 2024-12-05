# Weather Data API - Developer Documentation

## Introduction

This repository contains the code for a weather data processing solution, which includes:
- **Data ingestion**: Ingesting raw weather data into a PostgreSQL database.
- **Data analysis**: Calculating weather statistics (average temperatures, total precipitation) for each weather station.
- **REST API**: Exposing weather data and statistics via a RESTful API.
- **Swagger Documentation**: Automatically generated API documentation for easy testing and usage.

This document provides instructions on how to set up, run, and navigate through the codebase.

---

## 1. Prerequisites

Before you begin, make sure you have the following installed:
- **Python 3.7+** (The project is compatible with Python 3.7 and above)
- **PostgreSQL** (For the database)
- **pip** (Python package installer)

--

## 2. Running the Data Ingestion

The data ingestion process is handled by the `data_ingestion.py` script. This script reads weather data files, processes them, and inserts them into the database.

To run the ingestion process:
1. Ensure that the `weather_data` directory containing the raw weather files is in place.
2. Run the following command:
   ```bash
   python data_ingestion.py
   ```
   This will process the files and insert the data into the database.

---

## 3. Testing the API

You can test the API using Swagger UI. The available endpoints are:

1. **GET `/api/weather`**:
   - **Query Parameters**:
     - `station_id` (Optional): Filter by weather station ID.
     - `date` (Optional): Filter by date (format: `YYYY-MM-DD`).
     - `page` (Optional): Page number for pagination.
     - `per_page` (Optional): Number of items per page.

2. **GET `/api/weather/stats`**:
   - **Query Parameters**:
     - `station_id` (Optional): Filter by weather station ID.
     - `year` (Optional): Filter by year.

Both endpoints return data in JSON format, with pagination support.

---

## 4. Running the Application with Swagger

- **Swagger UI**: The API documentation is automatically generated and can be accessed via `http://localhost:5000/swagger`.
- This UI allows you to interact with the API and test the available endpoints directly.

---

## 5. Deployment Considerations

For production deployment, consider using the following:
- **Database**: Amazon RDS for PostgreSQL for scalability and reliability.
- **API Hosting**: AWS Elastic Beanstalk, AWS Lambda, or Heroku for hosting the Flask application.
- **Containerization**: Use Docker for containerizing the application for portability.
- **Continuous Integration/Continuous Deployment (CI/CD)**: Implement CI/CD pipelines using tools like GitHub Actions, CircleCI, or Jenkins.

---

## 6. Extra Features and Enhancements

- **Data Ingestion Scheduling**: You can schedule the data ingestion process using AWS Lambda and CloudWatch for periodic execution.
- **API Rate Limiting**: Implement rate limiting in the API to prevent abuse using Flask-Limiter or similar packages.
- **Authentication**: Add authentication (e.g., API key or OAuth2) to secure the API.

