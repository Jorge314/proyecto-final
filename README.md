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

El Iztaccíhuatl alberga algunos de los últimos remanentes glaciares de México. Durante las últimas décadas, diversos estudios han documentado un retroceso acelerado de estas masas de hielo, asociado a cambios en la temperatura, los patrones de precipitación y las condiciones atmosféricas de alta montaña.

Comprender la evolución de estas variables resulta relevante no sólo desde una perspectiva climática, sino también para la evaluación de riesgos geomorfológicos, la conservación de ecosistemas de alta montaña y la práctica del montañismo técnico.

Este proyecto utiliza registros meteorológicos horarios para analizar cuatro procesos climáticos estrechamente relacionados con la estabilidad glaciar:

1. **Consolidación:** duración de las ventanas continuas de congelación.
2. **Estabilidad térmica:** frecuencia de ciclos hielo-deshielo.
3. **Alimentación glaciar:** intensidad de eventos extremos de precipitación sólida.
4. **Ablación atmosférica:** condiciones favorables para sublimación.


## :package: Arquitectura y Flujo de Datos

Se implementó una arquitectura de Data Warehouse basada en un modelo dimensional tipo estrella.

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

### Modelo Dimensional

* **fact_clima**

  * temperatura
  * precipitación sólida
  * humedad relativa
  * radiación solar
  * variables atmosféricas horarias

* **dim_tiempo**

  * fecha
  * año
  * mes
  * estación

* **dim_ubicacion**

  * coordenadas
  * altitud

El análisis se realizó principalmente mediante CTEs y Window Functions para identificar patrones temporales complejos sobre más de cuatro décadas de observaciones.

---

# 🔍 Hallazgos Principales

## 1. Evolución de la Ventana de Congelación

Las ventanas prolongadas bajo 0°C representan periodos potencialmente favorables para la conservación y consolidación de nieve y hielo.

El análisis mediante la técnica de Gaps and Islands permitió identificar las secuencias históricas más largas de congelación continua.

### Resultados relevantes

* La racha más extensa ocurrió entre el 2 y el 17 de enero de 2010, con **359 horas consecutivas bajo cero** y una temperatura promedio de **−7.28°C**.
* La segunda racha más larga se registró recientemente, entre el 9 y el 23 de enero de 2022, acumulando **334 horas continuas**.
* Las principales ventanas de congelación se concentran en enero, evidenciando una marcada estacionalidad del proceso.

### Interpretación

Aunque las condiciones climáticas han cambiado significativamente durante las últimas décadas, continúan ocurriendo episodios de congelación prolongada. Sin embargo, estos eventos parecen cada vez más aislados dentro de un entorno caracterizado por una mayor variabilidad térmica.

---

## 2. Incremento de los Ciclos Hielo-Deshielo

Para evaluar cambios en la estabilidad térmica se contabilizaron las transiciones a través de la barrera de 0°C.

Estos ciclos favorecen procesos de meteorización física, fragmentación de roca y degradación de superficies glaciares expuestas.

### Resultados relevantes

* 2024 registró el máximo histórico con **766 ciclos**.
* 2025 y 2023 ocuparon el segundo y tercer lugar con **750** y **740 ciclos**, respectivamente.
* Los máximos históricos se concentran en los años más recientes de la serie.

### Interpretación

Los resultados sugieren una disminución progresiva de la estabilidad térmica en la alta montaña. La creciente frecuencia de ciclos hielo-deshielo indica condiciones más variables y potencialmente más agresivas para la conservación de hielo permanente.

---

## 3. Cambios en la Alimentación por Precipitación Sólida

La acumulación de nieve constituye uno de los principales mecanismos de alimentación glaciar.

Se analizaron los eventos de precipitación sólida más intensos registrados durante cada década.

### Resultados relevantes

* El 17 de febrero de 2024 se registró el evento más intenso de toda la serie histórica con **12.04 mm equivalentes de nieve en 24 horas**.
* Durante las décadas de 1990 y 2000 se observó una notable ausencia de eventos extremos comparables.
* La magnitud de los eventos recientes supera ampliamente los máximos observados en décadas anteriores.

### Interpretación

La acumulación parece depender cada vez más de eventos aislados de gran intensidad en lugar de aportes frecuentes y sostenidos. Este comportamiento sugiere una mayor irregularidad en los mecanismos de alimentación glaciar.

---

## 4. Condiciones Atmosféricas Favorables para la Sublimación

La sublimación representa una forma importante de pérdida de masa glaciar en ambientes de alta montaña, especialmente bajo condiciones de baja humedad y elevada radiación solar.

Para evaluar este fenómeno se analizaron promedios móviles de radiación y humedad relativa durante la temporada cálida.

### Resultados relevantes

* Los veranos de 2023 y 2024 registraron mínimos históricos de humedad relativa con valores de **21.46%** y **22.67%**.
* Estos episodios coincidieron con periodos de radiación solar sostenida superiores a **361 W/m²**.
* Ambos años presentan desviaciones importantes respecto al rango histórico observado entre 45% y 55%.

### Interpretación

Las condiciones observadas son consistentes con una atmósfera más seca y energéticamente más activa, favoreciendo procesos de sublimación y pérdida de masa de nieve y hielo.

---

## ⚠️ Limitaciones

Los datos utilizados provienen del modelo de reanálisis ERA5 y no de mediciones directas realizadas sobre la superficie glaciar.

Por esta razón, los resultados deben interpretarse como una reconstrucción climática de alta resolución útil para identificar tendencias atmosféricas de largo plazo, pero no como una medición directa de la evolución física del glaciar.

Asimismo, el estudio identifica asociaciones climáticas compatibles con procesos de degradación glaciar, sin establecer relaciones causales directas.

---

## 📌 Conclusiones

El análisis de 45 años de registros meteorológicos horarios muestra una transformación significativa en las condiciones climáticas de la alta montaña del Iztaccíhuatl.

Aunque continúan registrándose eventos excepcionales de congelación y precipitación sólida, estos coexisten con máximos históricos en la frecuencia de ciclos hielo-deshielo, mínimos históricos de humedad relativa y condiciones favorables para la sublimación.

En conjunto, la evidencia sugiere un entorno climático progresivamente más variable y potencialmente menos favorable para la permanencia de masas de hielo permanentes, un patrón consistente con el retroceso glaciar documentado en la alta montaña mexicana durante las últimas décadas.

Más allá de los hallazgos climáticos, este proyecto demuestra la aplicación de técnicas de ingeniería de datos, modelado dimensional y análisis SQL avanzado para transformar grandes volúmenes de datos meteorológicos en información útil para la comprensión de procesos ambientales complejos.







