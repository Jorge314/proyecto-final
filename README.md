# Proyecto Final — Análisis Climático del Iztaccíhuatl: Evolución de la Ventana de Congelación (1980-2025)

## :clipboard: Resumen ejecutivo

| Campo | Valor |
|---|---|
| **Pregunta analítica** | ¿Cómo ha evolucionado la "ventana de congelación" (horas consecutivas bajo 0°C) y la frecuencia de anomalías térmicas en El Pecho del Iztaccíhuatl durante los últimos 45 años? |
| **Dataset** | Mediciones históricas horarias (1980-2025) de variables meteorológicas en El Pecho (5,230 msnm) — pública, ~400,000 registros. |
| **Fuente** | [Archive API Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) (Modelo de Reanálisis ERA5). |
| **Modelo** | Estrella con 1 fact table (clima horario) y 2 dimensiones (tiempo y ubicación). |
| **Infraestructura** | Base de Datos Relacional: AWS Aurora PostgreSQL. |
| **ETL** | Pipeline en Python (`04_carga_y_orquestacion.ipynb`) con Pandas y SQLAlchemy para inyección de datos. |
| **SQL avanzado** | Window functions (`ROW_NUMBER`, `LAG`, `LEAD`) y CTEs para cálculo del problema "Gaps and Islands" (rachas de horas bajo cero). |

## :dart: Problema y motivación

La alta montaña mexicana está sufriendo un cambio geomorfológico acelerado. Entender con datos duros a nivel horario cómo la temperatura y la radiación solar han impactado la zona de los glaciares no solo es un ejercicio estadístico, sino una herramienta de planeación vital para el montañismo y rescate alpino. 

Este proyecto responde:
1. **¿Cuál ha sido la racha más larga de horas consecutivas bajo 0°C (ventana de consolidación de nieve)?**
2. **¿Cómo se ha reducido esta ventana comparando la década de los 80s con la década actual?**

## :package: Arquitectura y Flujo de Datos

Se optó por una arquitectura de Data Warehouse centralizado en AWS Aurora, realizando la transformación pesada en memoria (Pandas) antes de la inyección a la base de datos para asegurar la integridad referencial y optimizar las consultas analíticas. 

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
        │  • Clean: Imputación de nulos        │
        │  • Transform: Modelado Estrella      │
        │  • Load: SQLAlchemy to_sql()         │
        └──────────────────┬───────────────────┘
                           │  INSERT (Batch)
                           ▼
        ┌──────────────────────────────────────┐
        │  AWS Aurora PostgreSQL               │
        │  Schema: clima_izta_dwh              │
        │  • dim_tiempo                        │
        │  • dim_ubicacion                     │
        │  • fact_clima                        │
        └──────────────────┬───────────────────┘
                           │  SELECT
                           ▼
        ┌──────────────────────────────────────┐
        │  DBeaver (Cliente Analítico)         │
        │  Ejecución de queries avanzadas (CTE)│
        └──────────────────────────────────────┘
