CREATE DATABASE base_de_datos;
USE base_de_datos;
CREATE TABLE IF NOT EXISTS datos (
    id_emp int(6) NOT NULL,
    id_usu int(6) NOT NULL,
    cnt_ha int(6) NOT NULL
);
    PRIMARY KEY (id_emp,)
INSERT INTO datos ( id_emp, id_usu, ha ) VALUES ( 99, 99, 9999 );

CREATE TABLE IF NOT EXISTS empresas (
    id_emp int(6) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usu int(6) NOT NULL
);
