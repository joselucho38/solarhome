# =========================================================
# DASHBOARD ENERGÍA SOLAR - STREAMLIT
# ---------------------------------------------------------
# Objetivo:
# - Mostrar indicadores clave y gráficos de consumo mensual.
# - Estimar número de paneles y potencia del sistema de acuerdo
#   con supuestos ajustables por el usuario (HSP y Wp del panel).
# - Estimar ahorro en $ según cobertura y costo del kWh.
#
# Librerías estándar vistas en clase: pandas, numpy, matplotlib, seaborn.
# =========================================================

import json
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ------------------------------
# Configuración general de página
# ------------------------------
st.set_page_config(
    page_title="Dashboard Energía Solar",
    page_icon="☀️",
    layout="wide"
)

# Estilo Matplotlib/Seaborn (coherente con el tema)
sns.set_style("whitegrid")

# ------------------------------
# Carga de datos (reproducible)
# ------------------------------
# Nota: apuntamos al JSON que también consume la web (datos.html)
# Estructura esperada: [{"mes":"2025-01","kwh":410.2}, ...]
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "consumo_por_mes.json"

@st.cache_data(show_spinner=False)
def cargar_datos(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        # Dataset mínimo por si no existe el archivo
        ejemplo = [
            {"mes": "2025-01", "kwh": 410.2},
            {"mes": "2025-02", "kwh": 398.7},
            {"mes": "2025-03", "kwh": 450.1},
            {"mes": "2025-04", "kwh": 430.0},
            {"mes": "2025-05", "kwh": 470.8},
            {"mes": "2025-06", "kwh": 455.6},
        ]
        df = pd.DataFrame(ejemplo)
    else:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

    # Conversión de periodo (mes) a fecha para orden y gráficos
    # "YYYY-MM" -> usaremos el primer día del mes como timestamp
    df["fecha"] = pd.PeriodIndex(df["mes"], freq="M").to_timestamp()
    df = df.sort_values("fecha").reset_index(drop=True)
    df["kwh"] = pd.to_numeric(df["kwh"], errors="coerce")
    return df

df = cargar_datos(DATA_PATH)

# ------------------------------
# Barra lateral (controles)
# ------------------------------
st.sidebar.header("⚙️ Parámetros de estimación")

# Costo del kWh y cobertura deseada (para ahorro)
costo_kwh = st.sidebar.number_input("Costo por kWh ($)", min_value=0.0, value=650.0, step=10.0)
cobertura = st.sidebar.slider("Cobertura objetivo con solar (%)", min_value=10, max_value=100, value=80, step=5)

# Supuestos técnicos
st.sidebar.markdown("**Supuestos técnicos (ajustables):**")
hsp = st.sidebar.slider("Horas Sol Pico (HSP) por día", 3.0, 6.0, 4.0, 0.5)
wp_panel = st.sidebar.select_slider("Potencia del panel (Wp)", options=[330, 370, 400, 450, 500], value=400)

# Nota teórica
st.sidebar.info(
    "Producción aprox. por panel (kWh/mes) = (Wp/1000) * HSP * 30 días.\n"
    "Ajusta HSP y Wp según tu ciudad y panel seleccionado."
)

# ------------------------------
# Cálculos base para decisiones
# ------------------------------
consumo_prom = df["kwh"].mean()
consumo_max = df["kwh"].max()
consumo_min = df["kwh"].min()

# Tendencia: diferencia % entre últimos 3 meses vs 3 anteriores (si hay datos)
def tendencia_pct(d: pd.DataFrame) -> float:
    if len(d) < 6:
        return np.nan
    ult3 = d["kwh"].tail(3).mean()
    prev3 = d["kwh"].tail(6).head(3).mean()
    if prev3 == 0:
        return np.nan
    return (ult3 - prev3) / prev3 * 100.0

tend = tendencia_pct(df)

# Producción estimada por panel (kWh/mes)
kwh_panel_mes = (wp_panel/1000.0) * hsp * 30.0

# Paneles para cubrir el consumo promedio con la "cobertura" definida
paneles_nec = np.ceil((consumo_prom * (cobertura/100.0)) / kwh_panel_mes).astype(int)

# Ahorro estimado mensual ($) con cobertura y costo_kwh
ahorro_mensual = (consumo_prom * (cobertura/100.0)) * costo_kwh

# ------------------------------
# Encabezado
# ------------------------------
st.title("☀️ Dashboard de Energía Solar")
st.caption("Indicadores y estimaciones para apoyar la toma de decisiones.")

# ------------------------------
# KPIs principales
# ------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("kWh promedio/mes", f"{consumo_prom:,.0f}")
col2.metric("kWh máximo/mes", f"{consumo_max:,.0f}")
col3.metric("kWh mínimo/mes", f"{consumo_min:,.0f}")

if pd.notna(tend):
    tendencia_label = f"{tend:+.1f} %"
else:
    tendencia_label = "N/D"
col4.metric("Tendencia 3m vs previos", tendencia_label)

# ------------------------------
# Gráfico de consumo mensual + media móvil
# ------------------------------
st.subheader("Consumo mensual (kWh) y media móvil")
window = st.slider("Ventana media móvil (meses)", min_value=2, max_value=6, value=3, step=1)

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.bar(df["fecha"], df["kwh"], label="kWh mensual")
df["kwh_mm"] = df["kwh"].rolling(window=window).mean()
ax.plot(df["fecha"], df["kwh_mm"], linewidth=2.5, label=f"Media móvil ({window}m)", color="#FFCC00")
ax.set_xlabel("Mes"); ax.set_ylabel("kWh"); ax.legend()
plt.tight_layout()
st.pyplot(fig)

# ------------------------------
# Estimador de sistema fotovoltaico
# ------------------------------
st.subheader("Estimación de tamaño del sistema")
c1, c2, c3, c4 = st.columns(4)
c1.metric("HSP (días)", f"{hsp:.1f}")
c2.metric("Panel Wp", f"{wp_panel} Wp")
c3.metric("kWh/panel/mes", f"{kwh_panel_mes:.1f}")
c4.metric("Paneles necesarios", f"{paneles_nec:,}")

st.markdown(
    f"Para cubrir el **{cobertura}%** del consumo promedio mensual (≈ **{consumo_prom:,.0f} kWh**), "
    f"con panel de **{wp_panel} Wp** y **{hsp} HSP**, se requieren aproximadamente **{paneles_nec} paneles**."
)

# Potencia pico del arreglo (kWp) y ahorro estimado
pot_kwp = (paneles_nec * wp_panel) / 1000.0
st.info(
    f"**Potencia del sistema** estimada: **{pot_kwp:.2f} kWp**.  \n"
    f"**Ahorro mensual estimado**: **${ahorro_mensual:,.0f}** (con costo de **${costo_kwh:,.0f}/kWh** "
    f"y cobertura del **{cobertura}%**)."
)

# ------------------------------
# Tabla simple (opcional) y descarga
# ------------------------------
st.subheader("Tabla de consumo")
st.dataframe(df[["mes", "kwh"]].rename(columns={"mes": "Mes", "kwh": "kWh"}), use_container_width=True)

st.download_button(
    "Descargar datos (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="consumo_mensual.csv",
    mime="text/csv"
)

# ------------------------------
# Notas metodológicas
# ------------------------------
with st.expander("Notas y supuestos"):
    st.write("""
- **Producción por panel**: `(Wp / 1000) * HSP * 30 días` → kWh/mes.
- **HSP** varía por ciudad y época del año; usa rangos conservadores (3–6).
- La estimación es **aproximada** y no reemplaza un diseño detallado (pérdidas, sombras, orientación, temperatura, etc.).
- Este dashboard usa el mismo dataset **mensual** que la web (para coherencia y reproducibilidad).
""")
