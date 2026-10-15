# Datos de origen

Los diez cuadros que el Instituto Nacional de Estadística (INE) publica para el parque
automotor, con la serie 2003-2025. Se descargan de la página de publicación del INE y se
guardan acá con un nombre en ASCII, porque los nombres originales traen acentos que se
corrompen al viajar entre sistemas.

Cada cuadro es **un cruce de variables distinto**. Ninguno, solo, reúne todas las
dimensiones del análisis; esa es la razón por la que el trabajo los consolida en un único
archivo.

| Archivo | Cobertura | Cruce |
|---|---|---|
| `1.1_bolivia_departamento_servicio.xlsx` | Bolivia | Departamento y tipo de servicio |
| `1.2_bolivia_servicio_clase.xlsx` | Bolivia | Tipo de servicio y clase de vehículo |
| `1.3_bolivia_servicio_clase_capacidad.xlsx` | Bolivia | Servicio, clase y capacidad de carga |
| `1.4_bolivia_servicio_clase_modelo.xlsx` | Bolivia | Servicio, clase y modelo |
| `1.5_bolivia_servicio_clase_cilindrada.xlsx` | Bolivia | Servicio, clase y cilindrada |
| `2.1_chuquisaca_servicio_clase.xlsx` | Chuquisaca | Tipo de servicio y clase de vehículo |
| `3.1_chuquisaca_servicio_clase_capacidad.xlsx` | Chuquisaca | Servicio, clase y capacidad de carga |
| `4.1_chuquisaca_servicio_clase_modelo.xlsx` | Chuquisaca | Servicio, clase y modelo |
| `5.1_chuquisaca_servicio_clase_cilindrada.xlsx` | Chuquisaca | Servicio, clase y cilindrada |
| `6.1_chuquisaca_municipio_clase.xlsx` | Chuquisaca | Municipio y clase de vehículo |

## Estructura de cada archivo

Los diez comparten la misma forma de publicación: los títulos ocupan las primeras filas,
**los años están en la fila 6** y **los datos arrancan en la fila 8**, en las **columnas 2
a 24**. El código de consolidación lee exactamente eso.

## Qué produce la consolidación

`data_processed/parque_clasificadores.csv` — 1.633 filas, seis dimensiones, 23 años, una
fila por observación. Los totales del archivo consolidado coinciden exactamente con las
cifras publicadas: Bolivia 2.672.176 y Chuquisaca 99.092 vehículos en 2025.

Fuente: Instituto Nacional de Estadística. (2026). *Estadísticas del parque automotor
2003-2025*. https://www.ine.gob.bo/index.php/estadisticas-del-parque-automotor-2003-2025/
