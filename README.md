# Proyecto Final — Análisis Climático del Iztaccíhuatl: Evolución de la Ventana de Congelación (1980-2025)

## :clipboard: Resumen ejecutivo

| Campo | Valor |
|---|---|
| **Pregunta analítica** | ¿Cómo ha evolucionado la "ventana de congelación" (horas consecutivas bajo 0°C) y la frecuencia de anomalías térmicas en El Pecho del Iztaccíhuatl durante los últimos 45 años? |
| **Dataset** | Mediciones históricas horarias (1980-2025) de variables meteorológicas en El Pecho (5,230 msnm) — pública, ~400,000 registros. |
| **Fuente** | [Archive API Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) (Modelo de Reanálisis ERA5). |
| **Modelo** | Estrella con 1 fact table (clima horario) y 2 dimensiones (tiempo y ubicación). |
| **Infraestructura** | Data Lake Serverless: AWS S3 + AWS Athena. |
| **ETL** | Pipeline en Python (Pandas) para extracción y limpieza; carga directa a S3. |
| **SQL avanzado** | Window functions (`ROW_NUMBER`, `LAG`, `LEAD`) y CTEs para cálculo del problema "Gaps and Islands" (rachas de horas bajo cero). |

## :dart: Problema y motivación

La alta montaña mexicana está sufriendo un cambio geomorfológico acelerado. Entender con datos duros a nivel horario cómo la temperatura y la radiación solar han impactado la zona de los glaciares no solo es un ejercicio estadístico, sino una herramienta de planeación vital para el montañismo y rescate alpino. 

Este proyecto responde:
1. **¿Cuál ha sido la racha más larga de horas consecutivas bajo 0°C (ventana de consolidación de nieve)?**
2. **¿Cómo se ha reducido esta ventana comparando la década de los 80s con la década actual?**

## :package: Arquitectura y Flujo de Datos

Se optó por una arquitectura **Serverless Data Lake** para optimizar costos y velocidad de consulta sobre series de tiempo masivas, separando el almacenamiento del cómputo.

```text
        ┌──────────────────────────────────────┐
        │  Open-Meteo Archive API              │
        │  (Modelo ERA5 - 5,230 msnm)          │
        └──────────────────┬───────────────────┘
                           │  HTTP GET
                           ▼
        ┌──────────────────────────────────────┐
        │  ETL Python — Jupyter Notebooks      │
        │  • Extract: requests.get()           │
        │  • Clean: Imputación de nulos (Pandas)│
        │  • Transform: Modelado Estrella      │
        └──────────────────┬───────────────────┘
                           │  Archivos CSV
                           ▼
        ┌──────────────────────────────────────┐
        │  AWS S3 (Capa Oro / Almacenamiento)  │
        │  • /dim_tiempo/dim_tiempo.csv        │
        │  • /dim_ubicacion/dim_ubicacion.csv  │
        │  • /fact_clima/fact_clima.csv        │
        └──────────────────┬───────────────────┘
                           │  CREATE EXTERNAL TABLE
                           ▼
        ┌──────────────────────────────────────┐
        │  AWS Athena (Motor de Cómputo)       │
        │  Consultas distribuidas usando       │
        │  Presto/Trino SQL.                   │
        └──────────────────┬───────────────────┘
                           │  JDBC / ODBC
                           ▼
        ┌──────────────────────────────────────┐
        │  DBeaver (Cliente Analítico)         │
        │  Ejecución de queries avanzadas (CTE)│
        └──────────────────────────────────────┘
