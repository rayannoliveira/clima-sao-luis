import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

from extract import extract_weather_data
from transform import create_silver, create_gold
from load import save_bronze, save_silver, save_gold, save_to_postgres


def create_spark_session():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("clima_sao_luis") \
        .config("spark.python.worker.reuse", "false") \
        .config("spark.driver.host", "127.0.0.1") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
        .getOrCreate()

    return spark


def main():
    spark = create_spark_session()

    data = extract_weather_data()

    save_bronze(data)

    df_silver = create_silver(spark, data)

    print("SILVER")
    df_silver.show(truncate=False)

    df_gold = create_gold(df_silver)

    print("GOLD")
    df_gold.show(truncate=False)

    save_silver(df_silver)
    save_gold(df_gold)

    save_to_postgres(df_silver, "silver_weather")
    save_to_postgres(df_gold, "gold_weather_daily")

    print("Pipeline executada com sucesso!")

    spark.stop()


if __name__ == "__main__":
    main()