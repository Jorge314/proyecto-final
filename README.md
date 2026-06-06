# Proyecto Final — Análisis Climático del Iztaccíhuatl y Retroceso Glaciar (1980-2025)

## :clipboard: Resumen ejecutivo

| Campo | Valor |
|---|---|
| **Pregunta analítica** | ¿Cómo ha evolucionado la "ventana de congelación" (horas consecutivas bajo 0°C) en la cumbre del Iztaccíhuatl en la última década, y cómo este aumento térmico se correlaciona con la desaparición de la superficie del glaciar de El Pecho? |
| **Dataset** | Mediciones históricas horarias (1980-2025) de variables meteorológicas en El Pecho (5,230 msnm) — pública, ~400,000 registros. |
| **Fuente** | [Archive API Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) (Modelo de Reanálisis ERA5) y datos de investigación glaciológica (UNAM). |
| **Modelo** | Estrella con 2 fact tables (clima horario y mediciones anuales del glaciar) + 2 dimensiones (tiempo y ubicación). |
| **Infraestructura** | Aurora PostgreSQL en AWS. |
| **ETL** | Pipeline modular en Python (Pandas + SQLAlchemy) ejecutado en Jupyter Notebooks. |
| **SQL avanzado** | Window functions y CTEs para cálculo de rachas de horas sobre punto de congelación y anomalías térmicas. |

## 🎯 Justificación del Problema y Dataset
La alta montaña mexicana está sufriendo un cambio geomorfológico acelerado. Entender con datos duros a nivel horario cómo la temperatura y la radiación solar han impactado la zona de los glaciares no solo es un ejercicio estadístico, sino una herramienta de planeación vital para expediciones de montañismo. El dataset de Open-Meteo fue seleccionado por su volumen (cumpliendo y superando con creces la métrica de >10k filas) y por basarse en el modelo ERA5, permitiendo aplicar análisis temporales avanzados.

## 📁 Estructura del Repositorio
* `/datasets`: Archivos crudos extraídos de la API.
* `/scripts`: Notebooks con el flujo de ETL (Extracción, Limpieza, Transformación, Carga) y scripts DDL.
* `/docs`: Diagrama del modelo dimensional.
* `/dashboard`: (Próximamente) Visualización en Power BI.

## ⚙️ Ejecución
*(Se actualizará en los próximos hitos)*
