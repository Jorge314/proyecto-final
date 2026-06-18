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

Las ventanas prolongadas bajo 0°C representan periodos potencialmente favorables para la conservación de nieve acumulada y la permanencia temporal de superficies congeladas en ambientes de alta montaña.

Mediante la técnica de *Gaps and Islands* se identificaron las secuencias históricas más largas de congelación continua dentro de los más de 400,000 registros horarios analizados.

### Resultados relevantes

* La racha más extensa ocurrió entre el 2 y el 17 de enero de 2010, acumulando **359 horas consecutivas bajo 0°C** con una temperatura promedio de **−7.28°C**.
* La segunda racha más larga se registró recientemente, entre el 9 y el 23 de enero de 2022, alcanzando **334 horas continuas de congelación**.
* Cuatro de las diez ventanas de congelación más largas de toda la serie histórica ocurrieron durante la década de 2020.
* La totalidad de los eventos del Top 10 se concentró entre diciembre, enero y febrero, evidenciando una marcada estacionalidad invernal.

### Interpretación

Los resultados muestran que la capacidad del sistema atmosférico para generar episodios prolongados de congelación no ha desaparecido durante las últimas décadas. De hecho, varios de los eventos más extensos registrados desde 1980 ocurrieron recientemente, particularmente entre 2022 y 2023.

Sin embargo, algunas de estas rachas recientes presentan temperaturas promedio menos extremas que las observadas en eventos históricos de las décadas de 1980 y 1990. Esto sugiere que, aunque continúan ocurriendo periodos prolongados de congelación, el contexto térmico en el que se desarrollan podría estar experimentando modificaciones.

En conjunto, la evidencia indica que los episodios de congelación prolongada siguen formando parte del régimen climático de alta montaña del Iztaccíhuatl, aunque su relación con otros factores climáticos deberá evaluarse junto con indicadores de estabilidad térmica, precipitación sólida y sublimación.


## 2. Incremento de los Ciclos Hielo-Deshielo

Para evaluar la estabilidad térmica del entorno glaciar se contabilizaron los cruces anuales de la barrera de congelación (0°C), definidos como transiciones entre estados de congelación y descongelación detectadas mediante funciones de ventana SQL.

Estos ciclos representan episodios de variación térmica que pueden favorecer procesos de meteorización física, fragmentación de roca y degradación de superficies congeladas en ambientes de alta montaña.

### Resultados relevantes

* El máximo histórico se registró en 2024 con **766 cruces de la barrera de congelación**.
* Los años 2025 y 2023 ocuparon el segundo y cuarto lugar con **750** y **740 cruces**, respectivamente.
* El promedio anual de cruces aumentó de **690.4 eventos por año durante la década de 1980** a **731 eventos por año en la década de 2020**.
* La década de 2020 presentó además la mayor variabilidad interanual de toda la serie histórica, con una desviación estándar de **29.79**, superando ampliamente los valores observados en décadas anteriores.

### Interpretación

Los resultados muestran una tendencia ascendente en la frecuencia de ciclos hielo-deshielo durante los últimos 45 años. Aunque las diferencias entre décadas son graduales, la década de 2020 concentra tanto los máximos históricos como el promedio más elevado de toda la serie.

Asimismo, el incremento en la variabilidad interanual sugiere un sistema térmico menos estable y más propenso a alternar entre condiciones de congelación y descongelación.

En conjunto, la evidencia es consistente con un aumento progresivo de la inestabilidad térmica en la alta montaña del Iztaccíhuatl, una condición potencialmente favorable para procesos de meteorización física y degradación de superficies expuestas.

## 3. Cambios en la Alimentación por Precipitación Sólida

La precipitación sólida constituye uno de los principales mecanismos de aporte de nieve en la zona glaciar. Para evaluar su comportamiento se identificaron los días con mayor acumulación de nieve registrada en cada década de la serie histórica.

### Resultados relevantes

* El evento de nevada más intenso de toda la serie ocurrió el **17 de febrero de 2024**, acumulando **12.04 unidades de nieve registradas en 24 horas**.
* El segundo evento más significativo correspondió al **13 de marzo de 1983**, con **6.51 unidades**, aproximadamente la mitad del máximo observado en 2024.
* La década de 2020 concentra los eventos de precipitación sólida más intensos de todo el periodo analizado.
* Los máximos observados presentan una elevada variabilidad entre décadas, evidenciando un comportamiento no uniforme de los eventos extremos de nieve.

### Interpretación

Los resultados sugieren que los episodios de precipitación sólida continúan ocurriendo en la alta montaña del Iztaccíhuatl y que, en años recientes, pueden alcanzar magnitudes superiores a las registradas en gran parte de la serie histórica.

Más que mostrar una tendencia lineal de aumento o disminución, la distribución observada refleja una elevada variabilidad temporal, donde décadas con escasa actividad son seguidas por eventos extremos de gran intensidad.

En conjunto, la evidencia indica que la alimentación por nieve permanece presente dentro del sistema climático de alta montaña, aunque con una distribución temporal irregular y dominada por eventos puntuales de gran magnitud.


## 4. Condiciones Atmosféricas Favorables para la Sublimación

La sublimación constituye un mecanismo importante de pérdida de nieve y hielo en ambientes de alta montaña. Para identificar condiciones potencialmente favorables para este proceso, se analizaron promedios móviles de 24 horas de radiación solar y humedad relativa durante la temporada de verano.

A diferencia de los valores horarios instantáneos, los promedios móviles permiten identificar periodos prolongados de estrés atmosférico asociados a una mayor disponibilidad energética y una menor humedad ambiental.

### Resultados relevantes

* Los veranos de **2023** y **2024** registraron los niveles de humedad relativa sostenida más bajos de toda la serie histórica, alcanzando mínimos de **21.46%** y **22.67%**, respectivamente.
* Estos dos años representan los valores más extremos observados desde 1980.
* Ambos episodios coincidieron con niveles elevados de radiación solar sostenida, superiores a **361 W/m²**.
* Los máximos de radiación observados en años recientes se encuentran entre los más altos de toda la serie, aunque sin mostrar una tendencia creciente clara a largo plazo.

### Interpretación

Los resultados muestran que los años recientes han experimentado episodios excepcionalmente secos durante la temporada cálida, combinados con una elevada disponibilidad de energía solar.

Esta combinación de baja humedad relativa y alta radiación constituye un entorno atmosférico potencialmente favorable para procesos de sublimación y pérdida de nieve superficial.

Aunque el análisis no permite cuantificar directamente la sublimación ni el balance de masa glaciar, la ocurrencia simultánea de mínimos históricos de humedad y elevados niveles de radiación sugiere condiciones ambientales cada vez más propicias para la remoción de nieve y hielo mediante procesos atmosféricos.


## ⚠️ Limitaciones

Los datos utilizados provienen del modelo de reanálisis ERA5 y no de mediciones directas realizadas sobre la superficie glaciar.

Por esta razón, los resultados deben interpretarse como una reconstrucción climática de alta resolución útil para identificar tendencias atmosféricas de largo plazo, pero no como una medición directa de la evolución física del glaciar.

Asimismo, el estudio identifica asociaciones climáticas compatibles con procesos de degradación glaciar, sin establecer relaciones causales directas.

---

## 📌 Conclusiones

El análisis de más de **400,000 registros meteorológicos horarios** correspondientes al periodo **1980–2025** permitió identificar cambios relevantes en las condiciones climáticas de la alta montaña del Iztaccíhuatl.

Los resultados muestran que las grandes ventanas de congelación continúan ocurriendo en la actualidad; sin embargo, coexisten con una mayor frecuencia de ciclos hielo-deshielo y con una variabilidad térmica superior a la observada en décadas anteriores. La década de 2020 registró el promedio anual más alto de transiciones a través del punto de congelación, así como la mayor variabilidad interanual de toda la serie.

Asimismo, los años recientes concentraron algunos de los eventos más intensos de precipitación sólida y los niveles más bajos de humedad relativa registrados durante el verano. La combinación de sequedad extrema y elevada radiación solar sostenida sugiere condiciones atmosféricas potencialmente favorables para procesos de sublimación y pérdida de nieve superficial.

En conjunto, la evidencia apunta a un sistema climático de alta montaña cada vez más variable, donde episodios prolongados de congelación siguen ocurriendo, pero conviven con señales de inestabilidad térmica y estrés atmosférico que podrían dificultar la permanencia de nieve y hielo a largo plazo.

---

## 🛠️ Aprendizajes Técnicos

Durante el desarrollo del proyecto se aplicaron conceptos y herramientas de:

- **Modelado dimensional** mediante un esquema estrella.
- **Procesos ETL** desarrollados en Python con Pandas y SQLAlchemy.
- **Diseño e implementación de un Data Warehouse** en PostgreSQL sobre AWS Aurora.
- **Consultas analíticas avanzadas** utilizando CTEs y Window Functions.
- **Análisis temporal** mediante técnicas de *Gaps and Islands*, `LAG()`, `RANK()` y promedios móviles.
- **Transformación de datos meteorológicos históricos** en indicadores climáticos interpretables.

Este proyecto demuestra cómo las herramientas de **Ingeniería de Datos**, **Business Intelligence** y **SQL Avanzado** pueden emplearse para transformar grandes volúmenes de datos ambientales en información útil para la comprensión de fenómenos climáticos complejos.






