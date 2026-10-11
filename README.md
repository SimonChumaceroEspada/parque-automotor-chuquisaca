# Parque automotor de Chuquisaca, 2003-2025

Tablero interactivo del parque automotor registrado del departamento de Chuquisaca,
construido con datos oficiales del Instituto Nacional de Estadística (INE) y el
Registro Único para la Administración Tributaria Municipal (RUAT).

Trabajo de grado del Diplomado en Ciencia de Datos.

## Qué contiene

- `app.py` — tablero interactivo en Streamlit.
- `data_processed/` — datos ya limpios y consolidados que alimentan el tablero.
- `.streamlit/config.toml` — tema visual del tablero.

## Qué muestra el tablero

Tres pasos encadenados, más una comparación normativa.

1. Cuánto creció el parque entre 2003 y 2025.
2. Qué creció, es decir la composición por clase de vehículo.
3. Qué tan viejo es, es decir la antigüedad del parque por tramo de modelo.
4. Comparación de los criterios de restricción vehicular de España con la situación boliviana.

El panel lateral filtra por rango de años y por clase de vehículo, y el interruptor
cambia entre modo oscuro y modo claro.

## Datos

La fuente es la operación estadística del parque automotor del INE, de base censal y no
muestral, con series departamentales de 2003 a 2025. El conjunto de origen tiene 38.669
registros; el tablero trabaja sobre la serie consolidada en 898 filas agregadas por año,
clase de vehículo y clase de servicio.

Nota de limpieza: en la consolidación original, dos filas por año venían etiquetadas como
Vagoneta cuando en realidad eran los totales de servicio del departamento entero. Sumarlas
duplicaba 6.044 vehículos y hacía que las clases sumaran 105.136 en vez de 99.092. Esas
filas se retiraron del archivo `data_processed/tidy_chuquisaca.csv`.

Cifras de referencia del departamento.

| Año | Vehículos |
|---|---|
| 2003 | 19.290 |
| 2025 | 99.092 |

Y la composición de 2025 por clase, que suma exactamente el total departamental.

| Clase | Vehículos | Participación |
|---|---|---|
| Moto | 30.692 | 31,0 % |
| Vagoneta | 25.029 | 25,3 % |
| Automóvil | 18.985 | 19,2 % |

La comparación normativa se respalda en la Dirección General de Tráfico de España (2025),
el Decreto Supremo N.º 2232 (2014) y la Ley N.º 165 (2011).

## Cómo correrlo localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura de los datos

Los archivos de `data_processed/` están en formato largo, con una fila por combinación
de año, categoría, subcategoría y valor.

| Columna | Contenido |
|---|---|
| `anio` | Año del registro, de 2003 a 2025 |
| `categoria` | Clase de vehículo |
| `subcategoria` | Clase de servicio |
| `valor` | Cantidad de vehículos |
