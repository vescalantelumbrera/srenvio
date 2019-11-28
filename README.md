# srenvio

**srenvio** Proyecto prueba para entrevista

## Contenidos

- [Dependencias](#dependencias)
- [Configuración](#configuración)


---

## Dependencias

![Python +3.6](https://img.shields.io/badge/python-+3.6-blue.svg)

---

### Archivo de variables de entorno

Es necesario crear un **archivo de entorno** (**.env**) para la ejecución del sistema. Éste deberá estar colocado en la capreta raiz del proyecto:

``` bash
touch .env
```



A continuación se enlistan las variables necesarias con valores de ejemplo


#### POSTGRES

Variables de entorno para la conexión a las bases de datos.

| Variable | Valor  |
|----------|--------|
| [DB_NAME]          | srenvioDB   |
| [DB_USER]      | root        |
| [DB_PASSWORD]           | password          |
| [DB_HOST]| localhost |
| [DB_PORT]| 5432             |

#### FEDEX

Variables de entorno para las credenciales de FEDEX.

| Variable | Valor  |
|----------|--------|
| [FEDEX_KEY]          | key0000000   |
| [FEDEX_PASSWORD]      | asdijsidjadisj        |
| [ACCOUNTNUMBER]           | 4564556655          |
| [METERNUMBER]| 12121212121 |





