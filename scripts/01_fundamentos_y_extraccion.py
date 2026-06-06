import requests
import pandas as pd
import numpy as np


def extraer_clima_izta():

    # Coordenadas aproximadas de El Pecho del Iztaccíhuatl
    latitud = 19.1785
    longitud = -98.6418

    #Rango de tiempo
    fecha_inicio = "1980-01-01"
    fecha_fin = "2025-12-31"

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio,
        "end_date": fecha_fin,

        # Variables climáticas
        "hourly": ",".join([
            "temperature_2m",
            "precipitation",
            "snowfall",
            "snow_depth",
            "wind_speed_10m",
            "relative_humidity_2m",
            "shortwave_radiation"
        ]),

        "timezone": "America/Mexico_City"
    }

    print("Extrayendo datos climáticos históricos de la Iztaccíhuatl...")

    try:
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status()

        datos_json = respuesta.json()
        datos_horarios = datos_json.get("hourly", {})

        # Construcción del DataFrame
        df = pd.DataFrame({
            "fecha_hora": pd.to_datetime(datos_horarios.get("time")),

            "temperatura_c":
                datos_horarios.get("temperature_2m"),

            "precipitacion_mm":
                datos_horarios.get("precipitation"),

            "nieve_mm":
                datos_horarios.get("snowfall"),

            "profundidad_nieve_m":
                datos_horarios.get("snow_depth"),

            "viento_kmh":
                datos_horarios.get("wind_speed_10m"),

            "humedad_relativa":
                datos_horarios.get("relative_humidity_2m"),

            "radiacion_solar":
                datos_horarios.get("shortwave_radiation")
        })

        # ==========================
        # VARIABLES DERIVADAS
        # ==========================

        df["año"] = df["fecha_hora"].dt.year
        df["mes"] = df["fecha_hora"].dt.month
        df["dia"] = df["fecha_hora"].dt.day
        df["hora"] = df["fecha_hora"].dt.hour

        # Década
        df["decada"] = (df["año"] // 10) * 10

        # Indicador de congelación
        df["sobre_congelacion"] = np.where(
            df["temperatura_c"] > 0,
            1,
            0
        )

        # Estaciones del año
        estaciones = {
            12: "Invierno",
            1: "Invierno",
            2: "Invierno",
            3: "Primavera",
            4: "Primavera",
            5: "Primavera",
            6: "Verano",
            7: "Verano",
            8: "Verano",
            9: "Otoño",
            10: "Otoño",
            11: "Otoño"
        }

        df["estacion"] = df["mes"].map(estaciones)

        print(f"\nDatos extraídos correctamente.")
        print(f"Total de filas: {len(df):,}")

        print("\nPrimeros registros:")
        print(df.head(3))

        print("\nÚltimos registros:")
        print(df.tail(3))

        # Guardar CSV
        nombre_archivo = "clima_izta_1980_2025.csv"

        df.to_csv(nombre_archivo, index=False)

        print(f"\nArchivo guardado: {nombre_archivo}")

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")


if __name__ == "__main__":
    extraer_clima_izta()



