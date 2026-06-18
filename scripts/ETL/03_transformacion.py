import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

#Lectura de datos
df_clean = pd.read_csv("clima_izta_clean.csv")

#Revisamos que la fecha sea tipo datetime
df_clean["fecha_hora"] = pd.to_datetime(df_clean["fecha_hora"])
print(f"Filas listas para transformar: {len(df_clean):,}")

#Se contruye la tabla dim_ubicación
datos_ubicacion = {
    "id_ubicacion": [1],
    "nombre_montana": ["Iztaccíhuatl"],
    "zona_glaciar": ["El Pecho"],
    "latitud": [19.1785],
    "longitud": [-98.6418],
    "elevacion_msnm": [5230]
}

dim_ubicacion = pd.DataFrame(datos_ubicacion)

print(dim_ubicacion)

#Se contruye la tabla dim_tiempo
dim_tiempo = df_clean[["fecha_hora"]].copy()

#Llave Primaria en formato AAAAMMDDHH
dim_tiempo["id_tiempo"] = dim_tiempo["fecha_hora"].dt.strftime('%Y%m%d%H').astype(int)

#Se construye la estructura de la dimensión
dim_tiempo["fecha"] = dim_tiempo["fecha_hora"].dt.date
dim_tiempo["hora"] = dim_tiempo["fecha_hora"].dt.hour
dim_tiempo["dia"] = dim_tiempo["fecha_hora"].dt.day
dim_tiempo["mes"] = dim_tiempo["fecha_hora"].dt.month
dim_tiempo["anio"] = dim_tiempo["fecha_hora"].dt.year
dim_tiempo["decada"] = (dim_tiempo["anio"] // 10) * 10

#Estaciones del anio
estaciones = {
    12: "Invierno", 1: "Invierno", 2: "Invierno",
    3: "Primavera", 4: "Primavera", 5: "Primavera",
    6: "Verano", 7: "Verano", 8: "Verano",
    9: "Otoño", 10: "Otoño", 11: "Otoño"
}
dim_tiempo["estacion"] = dim_tiempo["mes"].map(estaciones)

#Se reordenan las columnas
cols_tiempo = ["id_tiempo", "fecha_hora", "fecha", "hora", "dia", "mes", "anio", "decada", "estacion"]
dim_tiempo = dim_tiempo[cols_tiempo]

print(f"Dimensión de tiempo creada con {len(dim_tiempo):,} registros.")
print(dim_tiempo.head(3))

#Se construye la tabla de hechos
fact_clima = df_clean.copy()

# Se crea la llave foranea de tiempo
fact_clima["id_tiempo"] = fact_clima["fecha_hora"].dt.strftime('%Y%m%d%H').astype(int)

# Se crea la llave foranea de ubicación (ya que solo estamos hablando del pecho del izta solo se usa 1)
fact_clima["id_ubicacion"] = 1

# Se seleccionan los ID y métricas numéricas
cols_hechos = [
    "id_tiempo",
    "id_ubicacion",
    "temperatura_c",
    "precipitacion_mm",
    "nieve_mm",
    "profundidad_nieve_m",
    "viento_kmh",
    "humedad_relativa",
    "radiacion_solar",
    "sobre_congelacion"
]

fact_clima = fact_clima[cols_hechos]

print(f"Tabla de hechos creada con {len(fact_clima):,} registros.")
print(fact_clima.head(3))

#Se guarda el modelo

dim_ubicacion.to_csv("dim_ubicacion.csv", index=False)
dim_tiempo.to_csv("dim_tiempo.csv", index=False)
fact_clima.to_csv("fact_clima.csv", index=False)
