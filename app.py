"""VERSIÓN OFICIAL — Azul profundo, sin rojo, modo claro legible."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Parque automotor Chuquisaca", page_icon="📊", layout="wide")
D = "data_processed/"

@st.cache_data
def load():
    df = pd.read_csv(D + "tidy_chuquisaca.csv")
    df["subcategoria"] = df["subcategoria"].fillna("")
    # limpia el numero de nota al pie que quedo pegado al nombre (p. ej. "Bus(3)")
    df["categoria"] = (df["categoria"].str.replace(r"\(\d+\)$", "", regex=True)
                                    .str.strip())
    return df, pd.read_csv(D + "tidy_chuquisaca_modelo.csv")
df, dfm = load()

if "dark" not in st.session_state:
    st.session_state.dark = True
with st.sidebar:
    st.toggle("Modo oscuro", key="dark")

dark = st.session_state.dark
if dark:
    bg, card, line, txt, mut = "#0A1628", "#12213A", "#1E3355", "#E6EEF9", "#8CA3C4"
    blue, gold, soft = "#3B82F6", "#D4AF37", "#7FA8D9"
    chip_blue = "#D4AF37"
    chip_text = "#0A1628"
    chip_bg, chip_bd, chip_tx = "#1E3355", "#2B4570", "#C9DCF5"
    grid = "rgba(255,255,255,0.07)"
else:
    bg, card, line, txt, mut = "#FFFFFF", "#F2F6FC", "#CBD8EA", "#0A1628", "#54637D"
    blue, gold, soft = "#1D4ED8", "#8A6D12", "#4A7FBF"
    chip_blue = "#C9A227"
    chip_text = "#0A1628"
    chip_bg, chip_bd, chip_tx = "#DCE7F5", "#B9CDE5", "#0A1628"
    grid = "rgba(10,22,40,0.14)"

st.markdown(f"""
<style>
.stApp {{ background:{bg}; }}
.stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{ color:{txt}; }}

/* metricas */
[data-testid="stMetric"] {{ background:{card}; border:1px solid {line};
    border-radius:10px; padding:14px 16px; }}
[data-testid="stMetricValue"] div {{ color:{gold} !important; font-weight:700; }}
[data-testid="stMetricLabel"] div, [data-testid="stMetricLabel"] p {{
    color:{mut} !important; text-transform:uppercase; letter-spacing:.8px; font-size:.72rem; }}

/* chips del multiselect: sin rojo, legibles en ambos modos */
[data-testid="stMultiSelect"] div {{ background-color:{bg} !important; }}
[data-testid="stMultiSelect"] input {{ background-color:transparent !important;
    color:{txt} !important; }}
[data-testid="stMultiSelect"] span {{ background-color:{chip_blue} !important;
    color:{chip_text} !important; border:none !important; border-radius:6px !important;
    font-weight:600 !important; }}
[data-testid="stMultiSelect"] span svg {{ fill:{chip_text} !important; }}
[data-testid="stMultiSelect"] svg {{ fill:{txt} !important; }}
div[data-baseweb="popover"] ul {{ background-color:{card} !important; }}
div[data-baseweb="popover"] li {{ color:{txt} !important; }}

/* slider y toggle */
div[data-testid="stSlider"] div, div[data-testid="stSelectSlider"] div {{
    color:{txt} !important; }}
div[data-testid="stToggle"] label span {{ color:{txt} !important; }}

/* cajas de aviso */
[data-testid="stAlert"] {{ background:{card} !important; border:1px solid {line} !important; }}
[data-testid="stAlert"] p, [data-testid="stAlert"] div {{ color:{txt} !important; }}

/* desplegable */
div[data-testid="stExpander"] {{ background:{card} !important;
    border:1px solid {line} !important; border-radius:8px !important; }}
div[data-testid="stExpander"] summary, div[data-testid="stExpander"] summary span {{
    color:{txt} !important; }}

/* tablas y estructura */
div[data-testid="stDataFrame"] {{ border:1px solid {line} !important; }}
hr {{ border-color:{line} !important; }}
[data-testid="stCaptionContainer"] p, .stApp small {{ color:{mut} !important; }}
[role="radiogroup"] label, [role="radiogroup"] p {{ color:{txt} !important; }}
[data-baseweb="tab"] div, [data-baseweb="tab"] p {{ color:{txt} !important; }}
[data-baseweb="tab"][aria-selected="true"] div {{ color:{gold} !important; font-weight:600; }}

/* barra lateral */
section[data-testid="stSidebar"] {{ background:{card}; border-right:1px solid {line}; }}
.sb-title {{ color:{gold}; font-size:1.15rem; font-weight:700; letter-spacing:.4px;
             margin:0 0 2px 0; padding-left:10px; border-left:3px solid {gold}; }}
.sb-sub {{ color:{mut}; font-size:.78rem; margin:0 0 18px 13px; }}
.sb-label {{ color:{mut}; font-size:.68rem; text-transform:uppercase; letter-spacing:1.2px;
             font-weight:600; margin:14px 0 2px 0; }}
.sb-box {{ background:{bg}; border:1px solid {line}; border-radius:8px; padding:10px 12px;
           margin-top:6px; font-size:.78rem; color:{txt}; }}
.rd {{ color:{gold}; font-weight:700; }}
h2.step {{ color:{gold}; margin:6px 0 4px 0; }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p class="sb-title">Chuquisaca</p>', unsafe_allow_html=True)
    st.markdown('<p class="sb-sub">Parque automotor 2003-2025</p>', unsafe_allow_html=True)
    st.markdown('<p class="sb-label">Rango de años</p>', unsafe_allow_html=True)
    anios = sorted(df.anio.unique())
    a0, a1 = st.select_slider("Rango", options=anios, value=(anios[0], anios[-1]),
                              label_visibility="collapsed")
    st.markdown('<p class="sb-label">Clases de vehículo</p>', unsafe_allow_html=True)
    clases = sorted(df[(df.categoria != "TOTAL") & (df.subcategoria == "")].categoria.unique())
    sel = st.multiselect("Clases", clases, default=clases, label_visibility="collapsed")
    st.markdown('<p class="sb-label">Filtro aplicado</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-box">{a0} a {a1}<br><span class="rd">{len(sel)}</span> de '
                f'{len(clases)} clases<br><span style="font-size:.72rem">Afecta los 3 pasos</span>'
                f'</div>', unsafe_allow_html=True)
    st.markdown('<p class="sb-label" style="margin-top:22px">Fuente</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{mut};font-size:.74rem;margin:0 0 0 2px">'
                f'INE (2026) · Elaboración propia</p>', unsafe_allow_html=True)

base = df[(df.subcategoria == "") & (df.categoria != "TOTAL") & (df.categoria.isin(sel))]
base = base[(base.anio >= a0) & (base.anio <= a1)]
serie = base.groupby("anio").valor.sum()
v0, v1 = int(serie.iloc[0]), int(serie.iloc[-1])
T = "plotly_dark" if dark else "plotly_white"
AX = dict(gridcolor=grid, linecolor=line, zerolinecolor=line, zeroline=False,
          tickfont=dict(color=txt, size=12),
          title=dict(font=dict(color=txt, size=13)))
LAY = dict(template=T, paper_bgcolor=card, plot_bgcolor=bg,
           font=dict(color=txt, family="Inter, Arial"),
           xaxis=dict(**AX), yaxis=dict(**AX),
           margin=dict(l=10, r=10, t=30, b=10))

st.title("La transformación del parque automotor de Chuquisaca")
st.caption("Tres pasos para entender qué pasó entre 2003 y 2025.")
st.divider()

paso = st.radio("Paso", ["1 · Cuánto creció", "2 · Qué creció", "3 · Qué tan viejo es"],
                horizontal=True, label_visibility="collapsed")

if paso.startswith("1"):
    st.markdown(f"<h2 class='step'>Se multiplicó por {v1/v0:.1f} en {len(serie)} años</h2>",
                unsafe_allow_html=True)
    st.markdown(f"De **{v0:,}** vehículos a **{v1:,}**. La tasa anual promedio fue de "
                f"**{((v1/v0)**(1/max(len(serie)-1,1))-1)*100:.1f}%**.".replace(",", "."))
    f = go.Figure(go.Scatter(x=serie.index, y=serie.values, mode="lines+markers",
                             line=dict(color=gold, width=3), marker=dict(size=7, color=gold),
                             fill="tozeroy", fillcolor="rgba(212,175,55,0.14)"))
    f.update_layout(**LAY, height=420, xaxis_title="Año", yaxis_title="Vehículos")
    st.plotly_chart(f, use_container_width=True, theme=None)

elif paso.startswith("2"):
    g = base[base.anio == a1].groupby("categoria").valor.sum().reset_index().sort_values("valor")
    g["pct"] = (g.valor / g.valor.sum() * 100).round(1)
    a, b = g.iloc[-1], g.iloc[-2]
    st.markdown(f"<h2 class='step'>{a.categoria} y {b.categoria} son la mitad del parque</h2>",
                unsafe_allow_html=True)
    st.markdown(f"**{a.categoria}** suma {a.valor:,} ({a.pct}%) y **{b.categoria}** suma "
                f"{b.valor:,} ({b.pct}%). Juntas son el {a.pct+b.pct:.1f}%.".replace(",", "."))
    f = go.Figure(go.Bar(x=g.valor, y=g.categoria, orientation="h", marker_color=blue,
                         text=g.pct.apply(lambda p: f"{p:.1f}%"), textposition="outside",
                         textfont=dict(color=txt)))
    f.update_layout(**LAY, height=460, xaxis_title="Vehículos")
    st.plotly_chart(f, use_container_width=True, theme=None)

else:
    orden = ["1969", "1970 - 1975", "1976 - 1980", "1981 - 1985", "1986 - 1990",
             "1991 - 1995", "1996 - 2000", "2001 - 2005", "2006 - 2010",
             "2011 - 2015", "2016 - 2020", "2021 - 2025", "2026 - 2030"]
    s = dfm.copy()
    s["tramo"] = pd.Categorical(s.tramo, orden, ordered=True)
    s = s.sort_values("tramo")
    total = int(s.valor.sum())
    viejos = int(s[s.tramo.isin(orden[:7])].valor.sum())
    pct_v = viejos / total * 100
    st.markdown(f"<h2 class='step'>{pct_v:.1f}% tiene 25 años o más</h2>",
                unsafe_allow_html=True)
    st.markdown(f"**{viejos:,}** vehículos son modelo 2000 o anterior. El parque creció, "
                f"pero también envejeció.".replace(",", "."))
    f = go.Figure(go.Pie(labels=["Modelo 2001 o posterior", "Modelo 2000 o anterior"],
                         values=[total - viejos, viejos], hole=0.62, sort=False,
                         marker=dict(colors=[blue, gold], line=dict(color=card, width=3)),
                         textinfo="label+percent", textposition="outside",
                         textfont=dict(color=txt, size=13)))
    f.update_layout(**LAY, height=470, showlegend=False,
                    annotations=[dict(text=f"{pct_v:.1f}%<br><span style='font-size:13px'>"
                                           f"modelo ≤ 2000</span>",
                                      x=0.5, y=0.5, showarrow=False,
                                      font=dict(size=26, color=gold))])
    st.plotly_chart(f, use_container_width=True, theme=None)
    with st.expander("Ver el detalle por tramo de modelo"):
        f2 = go.Figure(go.Bar(x=s.tramo.astype(str), y=s.valor,
                              marker_color=[gold] * 7 + [blue] * 6,
                              text=[f"{v:,}".replace(",", ".") for v in s.valor],
                              textposition="outside", textfont=dict(color=txt, size=9)))
        f2.update_layout(**LAY, height=420, yaxis_title="Vehículos")
        st.plotly_chart(f2, use_container_width=True, theme=None)

st.divider()
st.header("Comparación normativa: España y Bolivia")
filas = [
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
html = f"""<table style="width:100%;border-collapse:collapse;font-size:.88rem">
<tr style="background:{blue}">
  <th style="text-align:left;padding:11px 13px;border:1px solid {line};color:#fff">Criterio</th>
  <th style="text-align:left;padding:11px 13px;border:1px solid {line};color:#fff">España (referencia)</th>
  <th style="text-align:left;padding:11px 13px;border:1px solid {line};color:#fff">Bolivia (situación)</th>
</tr>"""
for i, (c, e, b) in enumerate(filas):
    fondo = card if i % 2 == 0 else bg
    html += (f'<tr style="background:{fondo}">'
             f'<td style="padding:11px 13px;border:1px solid {line};font-weight:600;'
             f'color:{gold}">{c}</td>'
             f'<td style="padding:11px 13px;border:1px solid {line};color:{txt}">{e}</td>'
             f'<td style="padding:11px 13px;border:1px solid {line};color:{txt}">{b}</td></tr>')
html += "</table>"
st.markdown(html, unsafe_allow_html=True)
st.caption("FUENTE: Elaboración propia con base en DGT (2025), D.S. N.º 2232 (2014) y Ley N.º 165 (2011).")
st.divider()
st.caption("Elaboración propia con base en INE (2026).")
