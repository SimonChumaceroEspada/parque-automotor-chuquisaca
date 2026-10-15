# Parque automotor de Chuquisaca, 2003-2025

Tablero interactivo del parque automotor registrado del departamento de Chuquisaca,
construido con datos oficiales del Instituto Nacional de Estadística (INE) y el
Registro Único para la Administración Tributaria Municipal (RUAT).

Trabajo de grado del Diplomado en Ciencia de Datos.

## Qué contiene

- `app.py` — tablero interactivo en Streamlit.
- `data_processed/parque_clasificadores.csv` — datos consolidados que alimentan el tablero,
  extraídos directamente de los diez cuadros oficiales del INE (1.633 filas, seis
  dimensiones, 23 años).
- `data_processed/tidy_chuquisaca.csv` y `tidy_chuquisaca_modelo.csv` — archivos de la
  primera extracción, que alimentan el cuadernillo de análisis de Google Colab.
- `.streamlit/config.toml` — tema visual del tablero.

## Qué muestra el tablero

Tres pasos encadenados, todos sensibles a los filtros del panel lateral.

1. **Cuánto creció** — el total del rango de años elegido.
2. **Cómo se compone** — la composición por el clasificador elegido, del año final del
   rango, en barras o en anillo.
3. **Qué tan viejo es** — la antigüedad del parque por tramo de modelo.

Los filtros son un rango de años, un clasificador y los valores de ese clasificador.
Los seis clasificadores disponibles son:

| Clasificador | Categorías |
|---|---|
| Tipo de vehículo | 16 |
| Clase de servicio | 3 |
| Modelo (tramo) | 14 |
| Cilindrada | 4 |
| Capacidad de carga (toneladas métricas) | 7 |
| Municipio | 27 |

El interruptor **Barras / Anillo** está disponible para los seis clasificadores. Cuando el
clasificador tiene más de nueve categorías, el anillo muestra las ocho mayores y agrupa el
resto en «Otros», para que las porciones menores no queden ilegibles; las barras muestran
siempre todas las categorías por separado.

El panel lateral también cambia entre modo oscuro y modo claro.

## Datos

La fuente es la operación estadística del parque automotor del INE, de base censal y no
muestral, con series departamentales de 2003 a 2025. El conjunto de origen tiene 38.669
registros repartidos en diez cuadros; cada cuadro responde a un cruce de variables distinto
y ninguno reúne todas las dimensiones del análisis, que es la razón por la que se
consolidaron en un solo archivo.

La consolidación conserva la trazabilidad: cada registro mantiene el archivo y la hoja de
origen, de modo que cualquier cifra se puede volver a comprobar en el cuadro publicado.

Nota de limpieza: en la extracción original, dos filas por año venían etiquetadas como
Vagoneta cuando en realidad eran los totales de servicio del departamento entero. Sumarlas
duplicaba 6.044 vehículos y hacía que las clases sumaran 105.136 en vez de 99.092. La
consolidación actual se hizo leyendo los diez archivos del INE directamente, y la validación
cruzada confirma los totales publicados.

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

`data_processed/parque_clasificadores.csv` está en formato largo, con una fila por
combinación de dimensión, categoría y año.

| Columna | Contenido |
|---|---|
| `dimension` | Clasificador: tipo de vehículo, clase de servicio, modelo, cilindrada, capacidad de carga o municipio |
| `categoria` | Valor dentro de ese clasificador |
| `anio` | Año del registro, de 2003 a 2025 |
| `valor` | Cantidad de vehículos |

## Referencias

- Instituto Nacional de Estadística. (2026). *Estadísticas del parque automotor 2003-2025*.
- Instituto Nacional de Estadística. (2023). *Documento metodológico de estadísticas básicas
  del parque automotor*.
