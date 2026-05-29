from itertools import chain

from pyspark.sql.functions import col, to_date, avg, max, min, create_map, lit


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
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    80: "Pancadas de chuva leves",
    81: "Pancadas de chuva moderadas",
    82: "Pancadas de chuva violentas",
    95: "Tempestade com trovoadas leve ou moderada",
}


def create_silver(spark, data):
    df = spark.createDataFrame([
        (t, temp, w)
        for t, temp, w in zip(
            data["hourly"]["time"],
            data["hourly"]["temperature_2m"],
            data["hourly"]["weather_code"]
        )
    ], ["timestamp", "temperature", "weather_code"])

    mapping_expr = create_map(
        [lit(x) for x in chain(*weather_codes.items())]
    )

    df_silver = df.withColumn(
        "weather_description",
        mapping_expr[col("weather_code")]
    )

    return df_silver


def create_gold(df_silver):
    df_gold = df_silver.withColumn(
        "date",
        to_date(col("timestamp"))
    ).groupBy("date").agg(
        avg("temperature").alias("avg_temperature"),
        max("temperature").alias("max_temperature"),
        min("temperature").alias("min_temperature")
    )

    return df_gold