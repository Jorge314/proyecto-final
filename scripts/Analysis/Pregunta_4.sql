SET search_path TO clima_izta_dwh;

WITH radiacion_continua AS (
    SELECT 
        t.fecha_hora,
        t.anio,
        t.estacion, 
        f.radiacion_solar,
        f.humedad_relativa,
        -- El promedio móvil 
        AVG(f.radiacion_solar) OVER (
            ORDER BY t.fecha_hora 
            ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
        ) as radiacion_movil_24h,
        AVG(f.humedad_relativa) OVER (
            ORDER BY t.fecha_hora 
            ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
        ) as humedad_movil_24h
    FROM fact_clima f
    JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
),
picos_verano AS (
    SELECT 
        anio,
        ROUND(MAX(radiacion_movil_24h), 2) as pico_radiacion_sostenida,
        ROUND(MIN(humedad_movil_24h), 2) as sequedad_extrema
    FROM radiacion_continua
    WHERE estacion = 'Verano' 
    GROUP BY anio
)
SELECT * FROM picos_verano
ORDER BY anio DESC;
-- ORDER BY sequedad_extrema ASC;
