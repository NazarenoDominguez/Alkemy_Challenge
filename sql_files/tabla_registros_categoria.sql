CREATE TABLE IF NOT EXISTS public.registros_categoria
(
    categoria character varying(256) NOT NULL,
    cantidad_registros integer NOT NULL,
    fecha_carga date NOT NULL DEFAULT NOW(),
    PRIMARY KEY (categoria)
);

ALTER TABLE IF EXISTS public.registros_categoria
    OWNER to postgres;