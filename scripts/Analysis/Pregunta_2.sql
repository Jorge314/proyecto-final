SET search_path TO clima_izta_dwh;

WITH cambios_estado AS (
    SELECT 
        t.anio,
        t.decada,
        t.fecha_hora,
        f.sobre_congelacion,
        LAG(f.sobre_congelacion) OVER (ORDER BY t.fecha_hora) AS estado_anterior
    FROM fact_clima f
    JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
),
ciclos_anuales AS (
    SELECT 
        anio,
        decada,
        COUNT(*) AS cruces_cero_grados
    FROM cambios_estado
    WHERE sobre_congelacion != estado_anterior
    GROUP BY anio, decada
)
SELECT
    decada,
    ROUND(AVG(cruces_cero_grados),2) AS promedio_anual_cruces,
    MIN(cruces_cero_grados) AS minimo,
    MAX(cruces_cero_grados) AS maximo,
    ROUND(STDDEV(cruces_cero_grados),2) AS desviacion
FROM ciclos_anuales
GROUP BY decada
ORDER BY decada;
