SET search_path TO clima_izta_dwh;

WITH rachas_clima AS (
    SELECT 
        t.fecha_hora,
        t.decada,
        f.temperatura_c,
        f.sobre_congelacion,
       
        ROW_NUMBER() OVER (ORDER BY t.fecha_hora) - 
        ROW_NUMBER() OVER (PARTITION BY f.sobre_congelacion ORDER BY t.fecha_hora) AS id_racha
    FROM fact_clima f
    JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
),
ventanas_congelacion AS (
    SELECT 
        MIN(fecha_hora) AS inicio_racha,
        MAX(fecha_hora) AS fin_racha,
        decada,
        COUNT(*) AS horas_consecutivas,
        ROUND(AVG(temperatura_c), 2) AS temp_promedio_c
    FROM rachas_clima
    WHERE sobre_congelacion = 0  -- Filtramos donde la temperatura fue <= 0°C
    GROUP BY id_racha, decada
)
-- Extraemos el Top 10 histórico
SELECT * FROM ventanas_congelacion
ORDER BY horas_consecutivas DESC
LIMIT 10;