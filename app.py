"""Tablero del parque automotor de Chuquisaca — version con los cinco clasificadores.

PROPOSITO DE ESTA VERSION
El tablero anterior mostraba solo las clases de vehiculo y filtraba unicamente por
año y por clase. Con eso el objetivo especifico 2 quedaba a medias, porque pide
caracterizar la composicion "por tipo de vehiculo, clase de servicio, modelo,
cilindrada y antiguedad EN EL PERIODO 2003-2025".

Aqui cada clasificador es una dimension navegable y los tres pasos responden a los
filtros:

  Paso 1  cuanto crecio el total del rango elegido
  Paso 2  como se compone ahora, por el clasificador elegido
  Paso 3  como cambio esa composicion a lo largo del periodo  <- lo que faltaba

Fuente: parque_clasificadores.csv (1.633 filas), extraido directo de los diez
cuadros del INE y verificado contra las cifras publicadas en el documento.
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Parque automotor Chuquisaca", page_icon="🚗", layout="wide")

RUTA = "data_processed/parque_clasificadores.csv"

DIMENSIONES = {
    "tipo_vehiculo": "Tipo de vehículo",
    "clase_servicio": "Clase de servicio",
    "modelo": "Modelo (tramo de años)",
    "cilindrada": "Cilindrada",
    "capacidad_carga": "Capacidad de carga",
    "municipio": "Municipio",
}

# orden logico de los tramos que lo tienen
ORDEN = {
    "modelo": ["≤ 1969", "1970 - 1975", "1976 - 1980", "1981 - 1985", "1986 - 1990",
               "1991 - 1995", "1996 - 2000", "2001 - 2005", "2006 - 2010",
               "2011 - 2015", "2016 - 2020", "2021 - 2025", "2026 - 2030",
               "Sin especificar"],
    "cilindrada": ["< a 850", "850 - 1400", "1401 - 2500", "> a 2500"],
    "capacidad_carga": ["Menor o igual a 1,4", "Mayores a 1,4 hasta 3", "Mayores a 3 hasta 5",
                        "Mayores a 5 hasta 11", "Mayores a 11 hasta 13", "Mayores a 13",
                        "Sin especificar"],
}


@st.cache_data
def cargar():
    df = pd.read_csv(RUTA)
    df["categoria"] = df["categoria"].astype(str).str.strip()
    return df


df = cargar()
ANIOS = sorted(df.anio.unique())

# ------------------------------- paletas -------------------------------
OSCURO = dict(bg="#0A1628", card="#12213A", line="#1E3355", txt="#E6EEF9",
              mut="#8CA3C4", blue="#3B82F6", gold="#D4AF37", grid="#1B2B47")
CLARO = dict(bg="#FFFFFF", card="#F2F6FC", line="#CBD8EA", txt="#0A1628",
             mut="#54637D", blue="#1D4ED8", gold="#8A6D12", grid="#E3EAF5")

if "dark" not in st.session_state:
    st.session_state.dark = True

with st.sidebar:
    st.markdown("### Chuquisaca")
    st.caption("Parque automotor 2003-2025")
    st.toggle("Modo oscuro", key="dark")

P = OSCURO if st.session_state.dark else CLARO
bg, card, line, txt, mut = P["bg"], P["card"], P["line"], P["txt"], P["mut"]
blue, gold, grid = P["blue"], P["gold"], P["grid"]

st.markdown(f"""
<style>
  .stApp {{ background:{bg}; }}
  [data-testid="stSidebar"] {{ background:{card}; }}
  h1, h2, h3, p, span, label, .stMarkdown {{ color:{txt}; }}
  h2.step {{ color:{gold}; font-size:1.35rem; margin:.2rem 0 .5rem 0; }}
  .sb-box {{ background:{bg}; border:1px solid {line}; border-radius:10px;
             padding:10px 12px; color:{txt}; font-size:.82rem; line-height:1.5; }}
  .sb-box .rd {{ color:{gold}; font-weight:700; }}
  div[data-baseweb="select"] > div {{ background:{card}; border-color:{line}; color:{txt}; }}
  /* el multiselect se desbordaba sobre los bloques de abajo cuando hay muchos valores:
     se le pone altura maxima y barra propia */
  [data-testid="stSidebar"] div[data-baseweb="select"] > div {{ max-height:210px; overflow-y:auto; }}
  [data-testid="stSidebar"] span[data-baseweb="tag"] {{ height:22px; font-size:.71rem; margin:1px; }}
  span[data-baseweb="tag"] {{ background:{gold} !important; color:#0A1628 !important; }}
  span[data-baseweb="tag"] svg {{ fill:#0A1628 !important; }}
  [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {{
      background:{gold} !important; border-color:{gold} !important; }}
  [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div {{
      background:{gold} !important; }}
  [role="radiogroup"] label p, [role="radiogroup"] label div {{ color:{txt} !important; }}
  *::-webkit-scrollbar {{ width:9px; height:9px; }}
  *::-webkit-scrollbar-track {{ background:{card}; }}
  *::-webkit-scrollbar-thumb {{ background:{gold}; border-radius:9px; }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f'<p class="sb-box" style="background:transparent;border:none;padding:0;'
                f'color:{mut};font-size:.76rem">Rango de años</p>', unsafe_allow_html=True)
    a0, a1 = st.select_slider("Rango", options=ANIOS, value=(ANIOS[0], ANIOS[-1]),
                              label_visibility="collapsed")

    st.markdown(f'<p style="color:{mut};font-size:.76rem;margin-top:14px">Clasificador</p>',
                unsafe_allow_html=True)
    dim = st.selectbox("Clasificador", list(DIMENSIONES.keys()),
                       format_func=lambda k: DIMENSIONES[k], label_visibility="collapsed")

    sub = df[df.dimension == dim]
    if dim in ORDEN:
        presentes = [c for c in ORDEN[dim] if c in set(sub.categoria)]
        resto = sorted(set(sub.categoria) - set(presentes), key=lambda s: -sub[sub.categoria == s].valor.sum())
        cats = presentes + resto
    else:  # municipio, servicio y clase: por tamaño
        cats = list(sub.groupby("categoria").valor.sum().sort_values(ascending=False).index)

    st.markdown(f'<p style="color:{mut};font-size:.76rem;margin-top:14px">Valores</p>',
                unsafe_allow_html=True)
    # caja de altura fija: con 27 municipios las etiquetas se desbordaban sobre
    # los bloques de abajo. Asi la lista se desplaza dentro de su propia caja.
    with st.container(height=232, border=False):
        sel = st.multiselect("Valores", cats, default=cats, label_visibility="collapsed")

    st.markdown(f'<p style="color:{mut};font-size:.76rem;margin-top:18px">Filtro aplicado</p>'
                f'<div class="sb-box">{a0} a {a1}<br>'
                f'<span class="rd">{DIMENSIONES[dim]}</span><br>'
                f'<span class="rd">{len(sel)}</span> de {len(cats)} valores<br>'
                f'<span style="font-size:.72rem">Afecta los 3 pasos</span></div>',
                unsafe_allow_html=True)

    st.markdown(f'<p style="color:{mut};font-size:.76rem;margin-top:22px">Fuente</p>'
                f'<p style="color:{mut};font-size:.74rem">INE (2026) · Elaboración propia</p>',
                unsafe_allow_html=True)

# ------------------------------- datos -------------------------------
base = df[(df.dimension == dim) & (df.categoria.isin(sel))]
base = base[(base.anio >= a0) & (base.anio <= a1)]
total = df[df.dimension == "tipo_vehiculo"]
total = total[(total.anio >= a0) & (total.anio <= a1)]
serie = total.groupby("anio").valor.sum()

FUENTE = "FUENTE: Elaboración propia con base en INE (2026)."
T = "plotly_dark" if st.session_state.dark else "plotly_white"
AX = dict(gridcolor=grid, linecolor=line, zeroline=False, tickfont=dict(color=txt, size=12),
          title=dict(font=dict(color=txt, size=13)))
LAY = dict(template=T, paper_bgcolor=card, plot_bgcolor=bg,
           font=dict(color=txt, family="Inter, Arial"),
           xaxis=dict(**AX), yaxis=dict(**AX), margin=dict(l=10, r=10, t=30, b=10))


def con_fuente(fig, y=-0.28, b=100):
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=b))
    fig.add_annotation(text=FUENTE, xref="paper", yref="paper", x=0, y=y, xanchor="left",
                       yanchor="top", showarrow=False, font=dict(size=10, color=mut))
    return fig


def num(v, dec=0):
    """Formato del documento: miles con punto y decimales con coma. 1234.5 -> 1.234,5"""
    return f"{v:,.{dec}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


st.title("La transformación del parque automotor de Chuquisaca")
st.caption("Tres pasos para entender qué pasó entre 2003 y 2025, por clasificador.")
st.divider()

paso = st.radio("Paso", ["1 · Cuánto creció", "2 · Cómo se compone", "3 · Qué tan viejo es"],
                horizontal=True, label_visibility="collapsed")
st.caption("En el panel de la izquierda elegí el **clasificador** y movés el extremo del "
           "**rango de años** para ver la composición en cualquier año del periodo. "
           "El rango de años afecta los tres pasos; el clasificador y los valores, el paso 2. "
           "El paso 3 usa siempre el clasificador «modelo».")

tramos = len(serie)

# ----------------------- paso 1: el total -----------------------
if paso.startswith("1"):
    v0, v1 = int(serie.iloc[0]), int(serie.iloc[-1])
    tasa = ((v1 / v0) ** (1 / max(tramos - 1, 1)) - 1) * 100
    st.markdown(f"<h2 class='step'>El total pasó de {num(v0)} a {num(v1)} vehículos</h2>",
                unsafe_allow_html=True)
    st.markdown(f"Se multiplicó por **{num(v1 / v0, 1)}** en {tramos} años. La tasa anual "
                f"promedio fue de **{num(tasa, 1)} %**.")
    f = go.Figure(go.Scatter(x=serie.index, y=serie.values, mode="lines+markers",
                             line=dict(color=gold, width=3), marker=dict(size=7, color=gold),
                             fill="tozeroy", fillcolor="rgba(212,175,55,0.14)"))
    f.update_layout(**LAY, height=420, xaxis_title="Año", yaxis_title="Vehículos")
    con_fuente(f, y=-0.30, b=110)
    st.plotly_chart(f, use_container_width=True, theme=None)

# ------------------- paso 2: la composicion -------------------
elif paso.startswith("2"):
    ult = base[base.anio == a1].groupby("categoria").valor.sum().sort_values(ascending=False)
    if ult.empty:
        st.warning("No hay valores seleccionados para ese año.")
    else:
        tot_u = ult.sum()
        top = ult.head(3)
        st.markdown(f"<h2 class='step'>{top.index[0]} encabeza la composición de {a1}</h2>",
                    unsafe_allow_html=True)
        detalle = ", ".join(f"**{c}** con {num(int(v))} ({num(v / tot_u * 100, 1)} %)"
                            for c, v in top.items())
        st.markdown(f"Total del clasificador «{DIMENSIONES[dim]}»: **{num(int(tot_u))}** vehículos. "
                    f"{detalle}.")
        # aclaracion de la unidad, cuando hace falta
        if dim == "capacidad_carga":
            st.caption("La capacidad de carga se mide en **toneladas métricas** (INE, 2026): es el peso "
                       "que puede llevar el vehículo, no la cantidad de pasajeros. El bloque "
                       "«sin especificar» es un hueco del propio registro.")
        elif dim == "cilindrada":
            st.caption("La cilindrada es la suma del volumen de los cilindros del motor, en "
                       "centímetros cúbicos (INE, 2026).")
        elif dim == "modelo":
            st.caption("Cada tramo agrupa años de modelo. En el paso 3 los tramos hasta 2000 se "
                       "reúnen como «modelo 2000 o anterior».")

        # tipo de grafico: el anillo esta disponible para todos los clasificadores.
        # Cuando hay muchas categorias, agrupa la cola en "Otros" para que se lea:
        # con 16 clases o 27 municipios, las porciones chicas no se verian.
        forma = st.radio("Forma", ["Barras", "Anillo"], horizontal=True, key="forma",
                         label_visibility="collapsed")

        if forma == "Anillo":
            ANILLO_MAX = 9
            if len(ult) > ANILLO_MAX:
                cabeza = ult.head(ANILLO_MAX - 1)
                cola = ult.iloc[ANILLO_MAX - 1:]
                datos_anillo = pd.concat([cabeza, pd.Series(
                    {f"Otros ({len(cola)} categorías)": cola.sum()})])
            else:
                datos_anillo = ult
            colores_anillo = [gold, blue, "#7FA8D9", "#8CA3C4", "#4A7FBF",
                              "#B9CBE6", "#D4AF37", "#6E8FB8", "#93A9C6"]
            tot_anillo = datos_anillo.sum()
            f = go.Figure(go.Pie(labels=list(datos_anillo.index),
                                 values=list(datos_anillo.values), hole=0.55, sort=False,
                                 marker=dict(colors=colores_anillo[:len(datos_anillo)],
                                             line=dict(color=card, width=3)),
                                 text=[f"{c} · {num(v / tot_anillo * 100, 1)} %"
                                       for c, v in datos_anillo.items()],
                                 textinfo="text", textposition="outside",
                                 textfont=dict(color=txt, size=12)))
            f.update_layout(**LAY, height=560, showlegend=False,
                            annotations=[dict(text=f"{num(int(tot_anillo))}<br>"
                                                   f"<span style='font-size:13px'>vehículos</span>",
                                              x=0.5, y=0.5, showarrow=False,
                                              font=dict(size=24, color=gold))])
            con_fuente(f, y=-0.04, b=40)
            st.plotly_chart(f, use_container_width=True, theme=None)
            if len(ult) > ANILLO_MAX:
                st.caption(f"El anillo muestra las {ANILLO_MAX - 1} categorías mayores y agrupa "
                           f"las {len(ult) - (ANILLO_MAX - 1)} menores en «Otros». El gráfico de "
                           f"barras las muestra todas por separado.")
        else:
            g = ult.sort_values()
            f = go.Figure(go.Bar(x=g.values, y=g.index, orientation="h", marker_color=blue,
                                 text=[f"{num(v / tot_u * 100, 1)} %" for v in g.values],
                                 textposition="outside", textfont=dict(color=txt)))
            f.update_layout(**LAY, height=max(320, 26 * len(g) + 120), xaxis_title="Vehículos")
            con_fuente(f, y=-0.18, b=80)
            st.plotly_chart(f, use_container_width=True, theme=None)

# ------------------- paso 3: la antiguedad (la dona) -------------------
elif paso.startswith("3"):
    VIEJOS = ["≤ 1969", "1970 - 1975", "1976 - 1980", "1981 - 1985", "1986 - 1990",
              "1991 - 1995", "1996 - 2000"]
    mod = df[(df.dimension == "modelo") & (df.anio == a1)]
    viejos = int(mod[mod.categoria.isin(VIEJOS)].valor.sum())
    total_m = int(mod.valor.sum())
    nuevos = total_m - viejos
    pct_v = viejos / total_m * 100 if total_m else 0
    st.markdown(f"<h2 class='step'>{num(pct_v, 1)} % tiene 25 años o más</h2>",
                unsafe_allow_html=True)
    st.markdown(f"**{num(viejos)}** vehículos de {a1} son modelo 2000 o anterior. "
                f"El parque creció, pero también envejeció.")
    f = go.Figure(go.Pie(labels=["Modelo 2001 o posterior", "Modelo 2000 o anterior"],
                         values=[nuevos, viejos], hole=0.62, sort=False,
                         text=[f"{num(nuevos / total_m * 100, 1)} % · Modelo 2001 o posterior"
                               if total_m else "",
                               f"{num(pct_v, 1)} % · Modelo 2000 o anterior"],
                         textinfo="text", textposition="outside",
                         marker=dict(colors=[blue, gold], line=dict(color=card, width=3)),
                         textfont=dict(color=txt, size=13)))
    f.update_layout(**LAY, height=470, showlegend=False,
                    annotations=[dict(text=f"{num(pct_v, 1)} %<br>"
                                           f"<span style='font-size:13px'>modelo ≤ 2000</span>",
                                      x=0.5, y=0.5, showarrow=False,
                                      font=dict(size=26, color=gold))])
    con_fuente(f, y=-0.06, b=50)
    st.plotly_chart(f, use_container_width=True, theme=None)
    with st.expander("Ver el detalle por tramo de modelo"):
        s = mod.copy()
        s["tramo"] = pd.Categorical(s.categoria, ORDEN["modelo"], ordered=True)
        s = s.sort_values("tramo")
        f2 = go.Figure(go.Bar(x=s.tramo.astype(str), y=s.valor,
                              marker_color=[gold] * 7 + [blue] * (len(s) - 7),
                              text=[num(v) for v in s.valor], textposition="outside",
                              textfont=dict(color=txt, size=9)))
        f2.update_layout(**LAY, height=420, yaxis_title="Vehículos")
        con_fuente(f2, y=-0.28, b=100)
        st.plotly_chart(f2, use_container_width=True, theme=None)

st.divider()
st.header("Comparación normativa: España y Bolivia")
FILAS = [
    ("Clasificación por antigüedad",
     "Etiquetas B, C o sin etiqueta, según año y combustible (DGT, 2025)",
     "No existe clasificación por antigüedad"),
    ("Gasolina: desde cuándo se considera limpio", "B desde 2001; C desde 2006",
     "Sin corte de circulación. Importación de livianos: máximo 1 año (D.S. 2232)"),
    ("Diésel: desde cuándo se considera limpio", "B desde 2006; C desde 2015",
     "Prohibido importar diésel en autos. Camiones: máximo 3 años"),
    ("¿Pueden circular los más antiguos?",
     "No en Zonas de Bajas Emisiones (centros de Madrid y Barcelona)",
     "Sí, si aprueban la ITV anual"),
]
html = (f'<table style="width:100%;border-collapse:collapse;font-size:.88rem">'
        f'<tr style="background:{blue}">'
        f'<th style="text-align:left;padding:11px 13px;border:1px solid {line};color:#fff">Criterio</th>'
        f'<th style="text-align:left;padding:11px 13px;border:1px solid {line};color:#fff">España (referencia)</th>'
        f'<th style="text-align:left;padding:11px 13px;border:1px solid {line};color:#fff">Bolivia (situación)</th></tr>')
for i, (c, e, b) in enumerate(FILAS):
    fondo = card if i % 2 == 0 else bg
    html += (f'<tr style="background:{fondo}">'
             f'<td style="padding:11px 13px;border:1px solid {line};font-weight:600;color:{gold}">{c}</td>'
             f'<td style="padding:11px 13px;border:1px solid {line};color:{txt}">{e}</td>'
             f'<td style="padding:11px 13px;border:1px solid {line};color:{txt}">{b}</td></tr>')
html += "</table>"
st.markdown(html, unsafe_allow_html=True)
st.caption("FUENTE: Elaboración propia con base en DGT (2025), D.S. N.º 2232 (2014) y Ley N.º 165 (2011).")
