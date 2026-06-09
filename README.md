# Proyecto Final — Análisis Climático del Iztaccíhuatl: Evolución de la Ventana de Congelación (1980-2025)

## :clipboard: Resumen ejecutivo

| Campo | Valor |
|---|---|
| **Pregunta analítica** | ¿Cómo ha evolucionado la "ventana de congelación" (horas consecutivas bajo 0°C) y la frecuencia de anomalías térmicas en El Pecho del Iztaccíhuatl durante los últimos 45 años? |
| **Dataset** | Mediciones históricas horarias (1980-2025) de variables meteorológicas en El Pecho (5,230 msnm) — pública, ~400,000 registros. |
| **Fuente** | [Archive API Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) (Modelo de Reanálisis ERA5). |
| **Modelo** | Estrella con 1 fact table (clima horario) y 2 dimensiones (tiempo y ubicación). |
| **Infraestructura** | Aurora PostgreSQL en AWS. |
| **ETL** | Pipeline modular en Python (Pandas + SQLAlchemy) ejecutado en Jupyter Notebooks. |
| **SQL avanzado** | Window functions y CTEs para cálculo de rachas de horas sobre el punto de congelación. |

## 🎯 Justificación del Problema y Dataset
La alta montaña mexicana está sufriendo un cambio geomorfológico acelerado. Entender con datos duros a nivel horario cómo la temperatura y la radiación solar han impactado la zona de los glaciares no solo es un ejercicio estadístico, sino una herramienta de planeación vital para expediciones de montañismo. El dataset de Open-Meteo fue seleccionado por su volumen (cumpliendo y superando con creces la métrica de >10k filas) y por basarse en el modelo ERA5, permitiendo aplicar análisis temporales avanzados.

## 🏗️ Decisiones de Diseño (Modelo Dimensional)
Se optó por un **Esquema Estrella** aplanando la dimensión temporal. Aunque un modelo Copo de Nieve habría normalizado los atributos de año, mes y estación, el volumen del dataset (~400,000 filas) permite priorizar la velocidad de lectura (menos JOINs) en el motor de bases de datos y optimizar la ingesta en herramientas de visualización. 

## 📖 Diccionario de Datos (Capa Oro)
**`fact_clima`**
* `temperatura_c`: Temperatura a 2 metros del suelo (°C).
* `radiacion_solar`: Radiación de onda corta entrante.
* `sobre_congelacion`: Variable booleana calculada (1 si Temp > 0°C, 0 si Temp <= 0°C).

**`dim_tiempo`**
* `id_tiempo`: Llave primaria generada en formato `YYYYMMDDHH`.
* `estacion`: Clasificación derivada del mes (Primavera, Verano, Otoño, Invierno).

## 📁 Estructura del Repositorio
* `/datasets`: Archivos crudos extraídos de la API y versión limpia (Capa Plata).
* `/scripts`: Notebooks con el flujo de ETL (Extracción, Limpieza, Transformación, Carga) y script DDL de creación de tablas.
* `/docs`: Diagrama del modelo estrella (`diagrama_modelo.png`).
* `/dashboard`: (Próximamente) Visualización en Power BI.

## ⚙️ Ejecución
*(Se actualizará en los próximos hitos)*
