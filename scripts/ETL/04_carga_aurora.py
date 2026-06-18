import pandas as pd
from sqlalchemy import create_engine
import time

# 1. Credenciales del clúster AWS Aurora
AURORA_HOST = "aurora-mod4.cluster-c3meyaew2z97.us-east-1.rds.amazonaws.com"
AURORA_USER = "postgres"
AURORA_PASSWORD = "CEwXrsjk3cP17q2KIGodJbEk"
AURORA_DB = "northwind"

engine = create_engine(f"postgresql+psycopg2://{AURORA_USER}:{AURORA_PASSWORD}@{AURORA_HOST}:5432/{AURORA_DB}")

# 2. Lectura de archivos locales

print("Leyendo archivos CSV")
df_ubicacion = pd.read_csv("dim_ubicacion.csv")
df_tiempo = pd.read_csv("dim_tiempo.csv")
df_clima = pd.read_csv("fact_clima.csv")


# 3. Cargando a la Base de Datos

start_time = time.time()

print(f"Cargando dim_ubicacion ({len(df_ubicacion)} filas)...")
df_ubicacion.to_sql('dim_ubicacion', con=engine, schema='clima_izta_dwh', if_exists='append', index=False)

print(f"Cargando dim_tiempo ({len(df_tiempo)} filas)...")
df_tiempo.to_sql('dim_tiempo', con=engine, schema='clima_izta_dwh', if_exists='append', index=False, method='multi', chunksize=1000)

print(f"Cargando fact_clima ({len(df_clima)} filas)...")
df_clima.to_sql('fact_clima', con=engine, schema='clima_izta_dwh', if_exists='append', index=False, method='multi', chunksize=5000)

end_time = time.time()
minutos_totales = round((end_time - start_time) / 60, 2)
print(f"Toda la data de El Pecho está en Aurora. Tiempo total: {minutos_totales} minutos.")