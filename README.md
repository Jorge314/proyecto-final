# Proyecto Final — Evolución de las Condiciones Climáticas Asociadas al Retroceso Glaciar en el Iztaccíhuatl (1980–2025)

## 📋 Resumen Ejecutivo

| Campo                         | Valor                                                                                                                                                                                                                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pregunta de investigación** | ¿Cómo han evolucionado las condiciones climáticas asociadas a la conservación glaciar en El Pecho del Iztaccíhuatl durante los últimos 45 años?                                                                                                                              |
| **Hipótesis**                 | Si las condiciones favorables para la permanencia del hielo han disminuido, entonces deberían observarse cambios en la duración de las ventanas de congelación, una mayor frecuencia de ciclos hielo-deshielo y condiciones atmosféricas más favorables para la sublimación. |
| **Dataset**                   | Registros meteorológicos horarios (1980–2025), aproximadamente 400,000 observaciones.                                                                                                                                                                                        |
| **Ubicación**                 | El Pecho del Iztaccíhuatl (5,230 msnm).                                                                                                                                                                                                                                      |
| **Fuente**                    | Open-Meteo Archive API (ERA5 Reanalysis).                                                                                                                                                                                                                                    |
| **Infraestructura**           | AWS Aurora PostgreSQL.                                                                                                                                                                                                                                                       |
| **Procesamiento**             | Python, Pandas, SQLAlchemy.                                                                                                                                                                                                                                                  |
| **Análisis**                  | SQL avanzado mediante CTEs, Window Functions y técnicas de Gaps and Islands.                                                                                                                                                                                                 |

---


## :dart: Problema y motivación

La alta montaña mexicana está sufriendo un cambio geomorfológico acelerado. Entender con datos duros a nivel horario cómo la temperatura, la precipitación y la radiación solar han impactado la zona de los glaciares no solo es un ejercicio estadístico, sino una herramienta de planeación vital para el montañismo técnico y la evaluación de riesgos en ruta. 

Este proyecto responde a cuatro interrogantes clave:
1. **Consolidación:** ¿Cuál ha sido la racha más larga de horas consecutivas bajo 0°C y cómo se ha comportado esta ventana en la década actual?
2. **Gelifracción:** ¿Se está acelerando la pérdida de estabilidad térmica y la fractura de la roca por ciclos de hielo-deshielo?
3. **Alimentación:** ¿Cuál ha sido la evolución decadal en la magnitud de los eventos extremos de precipitación sólida (súper nevadas)?
4. **Sublimación:** ¿Cuál es la tendencia histórica de los picos de radiación solar y humedad relativa, y cómo fomentan la creación de un "desierto de altura"?

## :package: Arquitectura y Flujo de Datos

Se optó por una arquitectura de Data Warehouse centralizado en AWS Aurora, realizando la transformación pesada en memoria (Pandas) antes de la inyección a la base de datos para asegurar la integridad referencial y optimizar las consultas analíticas. 

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

### 1. Evolución de la Ventana de Congelación
Tras ejecutar el análisis de *Gaps and Islands* sobre los más de 400,000 registros horarios, se identificaron las ventanas históricas más largas de congelación ininterrumpida (temperatura <= 0°C):
* **El récord histórico (2010):** La racha más larga ocurrió del 2 al 17 de enero de 2010, sumando **359 horas consecutivas** bajo cero con una temperatura promedio de -7.28°C.
* **Resiliencia reciente (2022):** Contrario a la hipótesis de que las grandes heladas son cosa del pasado, la segunda racha más larga ocurrió recientemente (9 al 23 de enero de 2022) con **334 horas**, aunque con una temperatura promedio ligeramente más cálida (-6.32°C).
* **Estacionalidad estricta:** El Top 3 histórico se concentra exclusivamente en el mes de **Enero**, demostrando que sigue siendo el ancla de consolidación del glaciar.

### 2. Aceleración de la Fractura Glaciar (Gelifracción)
Para evaluar la pérdida de estabilidad térmica, se analizó la frecuencia de cruces de la barrera de los 0°C (ciclos de hielo-deshielo que fracturan la roca y el hielo). Los datos revelan una aceleración crítica en el estrés mecánico sobre el terreno:
* **Concentración de anomalías:** La distribución muestra un sesgo severo hacia la actualidad. Los años 2024 (766 ciclos), 2025 (750 ciclos) y 2023 (740 ciclos) ocupan tres de los primeros cinco lugares con mayor cantidad de choques térmicos desde 1980.
* **El pico histórico:** El año 2024 registró el máximo histórico, lo que equivale a un promedio de más de dos cruces de congelación/descongelación diarios. 
* **Impacto geomorfológico:** Este incremento exponencial indica que el proceso de crioclastia está en su punto más agresivo, acelerando la degradación física de la zona por encima de los 5,200 msnm.

### 3. Volatilidad Extrema en Precipitación Sólida (Súper Nevadas)
Al analizar las tormentas de nieve más intensas mediante rankings decadales, los datos revelaron un patrón de alta volatilidad y eventos atípicos:
* **La Gran Anomalía de 2024:** El 17 de febrero de 2024 registró la nevada en 24 horas más masiva de los últimos 45 años (12.04 mm), superando por casi el doble al récord histórico de la década de 1980 (6.51 mm).
* **El "Desierto Blanco":** Las décadas de 1990 y 2000 carecieron casi por completo de tormentas de nieve de gran magnitud, evidenciando periodos prolongados de sequía de acumulación.
* **Impacto en el glaciar:** El régimen de alimentación ha mutado. Ahora depende de tormentas masivas, erráticas y violentas que, combinadas con fuertes vientos, generan acumulaciones desiguales y aumentan el riesgo de placas inestables.

### 4. El Enemigo Silencioso: Aceleración de la Sublimación
Para evaluar el estrés atmosférico en su temporada más vulnerable (verano), se calcularon los promedios móviles de 24 horas de radiación solar y humedad relativa, confirmando la creación de un "desierto de altura":
* **Desplome histórico de humedad:** Los veranos de 2023 y 2024 registraron los niveles de sequedad extrema más severos registrados, cayendo a 21.46% y 22.67% respectivamente, destruyendo el promedio histórico (45%-55%).
* **Máxima energía retenida:** Estos mínimos históricos coincidieron con picos de radiación solar sostenida superiores a los 361 W/m².
* **Impacto físico:** Esta combinación acelera drásticamente la sublimación del hielo. La transición directa a vapor debilita la cohesión de la capa de acumulación, generando superficies de nieve suelta ("azucarada") que comprometen severamente el avance técnico en la ruta.






