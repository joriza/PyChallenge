# Challenge Backend con Python y Flask

## Detalle de archivos

| Nombre Archivo     | Detalle                        |
| ------------------ | ------------------------------ |
| app.py             | Aplicación                     |
| config.py          | Configuracion de la aplicación |
| init.script.sql    | Script Base de Datos           |
| docker-compose.yml | Iniciar Contenedor             |
|                    |                                |


## URLs

- Carga de datos

http://127.0.0.1:5000/registrar

Los datos deben enviarse en formato json.

Ejemplo
```json
{
    "id_emp": 25,
    "id_usu": 125,
    "cnt_ha": 325
}
```

- Balance Por Empresa

  http://127.0.0.1:5000/balance1

- Balance Por Empresa Usuario

  http://127.0.0.1:5000/balance2
### URL Adicional
- Detalle de los datos cargados

  http://127.0.0.1:5000/detalle