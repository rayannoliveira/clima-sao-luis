import os
import sys
import json
import requests

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, to_date, avg, max, min
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .master("local[1]") \
    .appName("clima_sao_luis") \
    .config("spark.python.worker.reuse", "false") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

weather_codes = {
    0: "Céu limpo",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Encoberto",
    45: "Névoa",
    48: "Névoa com formação de geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa forte",
    56: "Garoa congelante leve",
    57: "Garoa congelante forte",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    66: "Chuva congelante leve",
    67: "Chuva congelante forte",
    71: "Queda de neve leve",
    73: "Queda de neve moderada",
    75: "Queda de neve forte",
    77: "Grãos de neve",
    80: "Pancadas de chuva leves",
    81: "Pancadas de chuva moderadas",
    82: "Pancadas de chuva violentas",
    85: "Pancadas de neve leves",
    86: "Pancadas de neve fortes",
    95: "Tempestade com trovoadas leve ou moderada",
    96: "Tempestade com trovoadas e granizo leve",
    99: "Tempestade com trovoadas e granizo forte"
}

url = "https://api.open-meteo.com/v1/forecast?latitude=-2.5297&longitude=-44.3028&hourly=temperature_2m,weather_code"

data = requests.get(url).json()

# BRONZE - JSON bruto
os.makedirs("data/bronze/weather_raw", exist_ok=True)

with open("data/bronze/weather_raw/open_meteo_raw.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# SILVER - dados estruturados
df = spark.createDataFrame([
    (t, temp, w)
    for t, temp, w in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["weather_code"]
    )
], ["timestamp", "temperature", "weather_code"])

def get_weather_description(code):
    return weather_codes.get(code, "Código desconhecido")

weather_udf = udf(get_weather_description, StringType())

df_silver = df.withColumn(
    "weather_description",
    weather_udf(col("weather_code"))
)

print("SILVER")
df_silver.show(truncate=False)

# GOLD - agregação diária
df_gold = df_silver.withColumn(
    "date",
    to_date(col("timestamp"))
).groupBy("date").agg(
    avg("temperature").alias("avg_temperature"),
    max("temperature").alias("max_temperature"),
    min("temperature").alias("min_temperature")
)

print("GOLD")
df_gold.show(truncate=False)

spark.stop()