import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

#Lectura de datos
archivo = "clima_izta_1980_2025.csv"

df = pd.read_csv(archivo)
print(f"Total de filas cargadas: {len(df):,}")
print(f"Total de columnas cargadas: {df.shape[1]}")

#Perfilado
df.info()

print(df.describe())

#Casteo
df_clean = df.copy()

# Convertir la columna de texto a formato datetime real
df_clean["fecha_hora"] = pd.to_datetime(df_clean["fecha_hora"])

print(f"Tipo de dato actualizado: ",df_clean["fecha_hora"].dtype)

# Valores nulos
nulos_por_columna = df_clean.isnull().sum()
print(nulos_por_columna)

# Duplicación
duplicados = df_clean.duplicated(subset=["fecha_hora"]).sum()
print(f"Registros con hora exacta duplicada: {duplicados}")

#Guardado
nombre_archivo_clean = "clima_izta_clean.csv"

df_clean.to_csv(nombre_archivo_clean, index=False)

print(f"Archivo guardado exitosamente como: '{nombre_archivo_clean}'")
print(f"Filas finales listas para transformación: {len(df_clean):,}")
print(f"Columnas finales listas para transformación: {df_clean.shape[1]}")
