CREATE TABLE IF NOT EXISTS public.registros_provincia_categoria
(
    id_provincia_categoria serial NOT NULL,
    provincia character varying(256) NOT NULL,
    categoria character varying(256) NOT NULL,
    cantidad_registros integer NOT NULL,
    fecha_carga date NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id_provincia_categoria)
);

ALTER TABLE IF EXISTS public.registros_provincia_categoria
    OWNER to postgres;