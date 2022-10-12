CREATE TABLE IF NOT EXISTS public.museos_cines_bibliotecas
(
    id_centro_recreativo serial NOT NULL,
    cod_localidad integer NOT NULL,
    fecha_carga date NOT NULL DEFAULT NOW(),
    id_provincia integer NOT NULL,
    id_departamento integer NOT NULL,
    categoria character varying(256) NOT NULL,
    provincia character varying(256) NOT NULL,
    localidad character varying(256) NOT NULL,
    nombre character varying(256) NOT NULL,
    direccion character varying(256),
    codigo_postal character varying(256),
    telefono character varying(256),
    mail character varying(256),
    web character varying(256),
    PRIMARY KEY (id_centro_recreativo)
);

ALTER TABLE IF EXISTS public.museos_cines_bibliotecas
    OWNER to postgres;