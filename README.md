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

## :mag: Hallazgos principales

Tras ejecutar el análisis de *Gaps and Islands* sobre los más de 400,000 registros horarios, se identificaron las ventanas históricas más largas de congelación ininterrumpida (temperatura <= 0°C) en El Pecho (5,230 msnm):

1. **El récord histórico (2010):** La racha más larga ocurrió del 2 al 17 de enero de 2010, sumando **359 horas consecutivas** bajo cero con una temperatura promedio de -7.28°C.
2. **Resiliencia reciente (2022):** Contrario a la hipótesis de que las grandes heladas son cosa del pasado, la segunda racha más larga ocurrió recientemente (9 al 23 de enero de 2022) con **334 horas**, aunque con una temperatura promedio ligeramente más cálida (-6.32°C).
3. **Estacionalidad estricta:** El Top 3 histórico (incluyendo la tercera racha en 1992 de 333 horas) se concentra exclusivamente en el mes de **Enero**. Esto demuestra que, a pesar de las anomalías climáticas, enero sigue siendo el ancla de consolidación del glaciar.

### 2. Aceleración de la Fractura Glaciar (Gelifracción)
Para evaluar la pérdida de estabilidad térmica, se analizó la frecuencia de cruces de la barrera de los 0°C (ciclos de hielo-deshielo que fracturan la roca y el hielo). 

Los datos revelan una aceleración crítica en el estrés mecánico sobre el terreno:
* **Concentración de anomalías:** La distribución de los datos muestra un sesgo severo hacia la actualidad. Los años 2024 (766 ciclos), 2025 (750 ciclos) y 2023 (740 ciclos) ocupan tres de los primeros cinco lugares con mayor cantidad de choques térmicos desde 1980.
* **El pico histórico:** El año 2024 registró el máximo histórico, lo que equivale a un promedio de más de dos cruces de congelación/descongelación diarios. 
* **Impacto geomorfológico:** Este incremento exponencial en la varianza térmica reciente indica que el proceso de crioclastia está en su punto más agresivo, acelerando la degradación física de la zona por encima de los 5,200 msnm.
