CREATE TABLE IF NOT EXISTS public.registros_fuente
(
    fuente character varying(256) NOT NULL,
    cantidad_registros integer NOT NULL,
    fecha_carga date NOT NULL DEFAULT NOW(),
    PRIMARY KEY (fuente)
);

ALTER TABLE IF EXISTS public.registros_fuente
    OWNER to postgres;