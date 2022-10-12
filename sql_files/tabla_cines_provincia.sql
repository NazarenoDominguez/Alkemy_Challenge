CREATE TABLE IF NOT EXISTS public.cines_provincia
(
    provincia character varying(256) NOT NULL,
    pantallas integer NOT NULL,
    butacas integer NOT NULL,
    espacio_incaa integer NOT NULL,
    fecha_carga date NOT NULL DEFAULT NOW(),
    PRIMARY KEY (provincia)
);

ALTER TABLE IF EXISTS public.cines_provincia
    OWNER to postgres;