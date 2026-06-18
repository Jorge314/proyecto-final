-- =========================================================
-- DDL: ESQUEMA ESTRELLA (PROYECTO IZTACCÍHUATL)
-- =========================================================

-- 1. DIMENSIÓN TIEMPO 
CREATE TABLE dim_tiempo (
    id_tiempo INT PRIMARY KEY,
    fecha_hora TIMESTAMP NOT NULL,
    fecha DATE NOT NULL,
    hora INT NOT NULL,
    dia INT NOT NULL,
    mes INT NOT NULL,
    anio INT NOT NULL,
    decada INT NOT NULL,
    estacion VARCHAR(20)
);

-- 2. DIMENSIÓN UBICACIÓN
CREATE TABLE dim_ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    nombre_montana VARCHAR(100) NOT NULL,
    zona_glaciar VARCHAR(100) NOT NULL,  
    latitud NUMERIC(10, 6) NOT NULL,
    longitud NUMERIC(10, 6) NOT NULL,
    elevacion_msnm INT
);

-- 3. CREACIÓN TABLA DE HECHOS PRINCIPAL
CREATE TABLE fact_clima (
    id_lectura SERIAL PRIMARY KEY,
    id_tiempo INT REFERENCES dim_tiempo(id_tiempo),
    id_ubicacion INT REFERENCES dim_ubicacion(id_ubicacion),
    temperatura_c NUMERIC(5, 2),
    precipitacion_mm NUMERIC(6, 2),
    nieve_mm NUMERIC(6, 2),
    profundidad_nieve_m NUMERIC(5, 2),
    viento_kmh NUMERIC(6, 2),
    humedad_relativa NUMERIC(5, 2),
    radiacion_solar NUMERIC(8, 2),
    sobre_congelacion SMALLINT          
);

-- 4. SEGUNDA TABLA DE HECHOS
CREATE TABLE fact_glaciar (
    id_medicion SERIAL PRIMARY KEY,
    anio INT NOT NULL,                  
    id_ubicacion INT REFERENCES dim_ubicacion(id_ubicacion),
    superficie_m2 NUMERIC(10, 2),       
    fuente_cientifica VARCHAR(255)      
);

-- Indices
CREATE INDEX idx_fact_clima_tiempo ON fact_clima(id_tiempo);
CREATE INDEX idx_fact_clima_ubicacion ON fact_clima(id_ubicacion);