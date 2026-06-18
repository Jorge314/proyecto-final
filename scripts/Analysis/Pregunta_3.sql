SET search_path TO clima_izta_dwh;

WITH nevadas_diarias AS (
    SELECT 
        t.decada,
        t.fecha,
        SUM(f.nieve_mm) as total_nieve_dia,
        ROUND(AVG(f.temperatura_c),2) as temp_promedio,
        MAX(f.viento_kmh) as racha_viento_max
    FROM fact_clima f
    JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
    GROUP BY t.decada, t.fecha
    HAVING SUM(f.nieve_mm) > 0 -- Días que sí nevó
),
ranking_decadal AS (
    SELECT 
        decada,
        fecha,
        total_nieve_dia,
        temp_promedio,
        racha_viento_max,
        RANK() OVER (PARTITION BY decada ORDER BY total_nieve_dia DESC) as rank_nevada
    FROM nevadas_diarias
)

SELECT * FROM ranking_decadal
WHERE rank_nevada <= 3
ORDER BY decada DESC, rank_nevada ASC;
