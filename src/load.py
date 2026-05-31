import os
import json


def save_bronze(data):
    os.makedirs("data/bronze/weather_raw", exist_ok=True)

    with open(
        "data/bronze/weather_raw/open_meteo_raw.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def save_silver(df_silver):
    df_silver.write.mode("overwrite").option("header", True).csv(
        "data/silver/weather_silver"
    )


def save_gold(df_gold):
    df_gold.write.mode("overwrite").option("header", True).csv(
        "data/gold/weather_daily"
    )


def save_to_postgres(df, table_name):
    jdbc_url = os.getenv(
        "POSTGRES_JDBC_URL",
        "jdbc:postgresql://localhost:5432/clima_db?sslmode=disable"
    )

    connection_properties = {
        "user": os.getenv("POSTGRES_USER", "admin"),
        "password": os.getenv("POSTGRES_PASSWORD", "123456"),
        "driver": "org.postgresql.Driver"
    }

    df.write.mode("append").jdbc(
        url=jdbc_url,
        table=table_name,
        properties=connection_properties
    )