import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Vigas - Resistencia de Materiales", layout="wide")

st.title("Análisis de Vigas Simplemente Apoyadas")
st.markdown("Visualización en tiempo real de reacciones, fuerza cortante y momento flector.")

# --- 1. CONFIGURACIÓN EN LA BARRA LATERAL ---
st.sidebar.header("Parámetros de la Viga")
L = st.sidebar.number_input("Longitud de la viga (m)", min_value=1.0, max_value=20.0, value=10.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("Carga Puntual (P)")
P = st.sidebar.number_input("Fuerza P (kN) [Hacia abajo]", min_value=0.0, value=50.0, step=5.0)
a = st.sidebar.slider("Posición de P desde la izquierda (m)", 0.0, float(L), float(L)/2, step=0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("Carga Distribuida (w)")
w = st.sidebar.number_input("Carga w (kN/m) [En toda la viga]", min_value=0.0, value=10.0, step=2.0)

# --- 2. CÁLCULO ESTÁTICO (Reacciones) ---
# Sumatoria de momentos en el apoyo izquierdo (A) = 0
# Rb * L - P * a - w * L * (L/2) = 0
Rb = (P * a + w * L * (L / 2)) / L

# Sumatoria de fuerzas en Y = 0
# Ra + Rb - P - w * L = 0
Ra = P + w * L - Rb

# --- 3. FUNCIONES DE CORTE (V) Y MOMENTO (M) ---
x = np.linspace(0, L, 500)
V = np.zeros_like(x)
M = np.zeros_like(x)

for i, xi in enumerate(x):
    # Fuerza Cortante
    V[i] = Ra - w * xi
    if xi > a:
        V[i] -= P
        
    # Momento Flector
    M[i] = Ra * xi - w * xi**2 / 2
    if xi > a:
        M[i] -= P * (xi - a)

# --- 4. VISUALIZACIÓN ---
# Crear 3 subgráficos alineados verticalmente
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True, gridspec_kw={'height_ratios': [1, 1.5, 1.5]})
fig.patch.set_alpha(0.0)

# Colores Makerbox
c_viga = "#2d2d2d"
c_corte = "#00aeef"   # Cian
c_momento = "#c72979" # Fucsia/Magenta
c_fuerzas = "#46247a" # Morado profundo

# -- Gráfico 1: Esquema de la Viga --
ax1.set_facecolor('none')
ax1.set_title("Esquema Físico y Reacciones", fontweight="bold")
ax1.set_xlim(-0.5, L + 0.5)
ax1.set_ylim(-2, 3)
ax1.axis('off')

# Dibujar la viga
viga_rect = patches.Rectangle((0, -0.2), L, 0.4, facecolor='lightgray', edgecolor=c_viga, lw=2)
ax1.add_patch(viga_rect)

# Apoyos (Triángulos simples)
ax1.plot(0, -0.2, marker='^', markersize=15, color=c_viga)
ax1.plot(L, -0.2, marker='^', markersize=15, color=c_viga)

# Reacciones (Flechas hacia arriba)
ax1.annotate(f"Ra={Ra:.1f} kN", xy=(0, -0.2), xytext=(0, -1.8),
             arrowprops=dict(facecolor=c_fuerzas, edgecolor=c_fuerzas, shrink=0.05, width=2, headwidth=8),
             ha='center', fontweight='bold', color=c_fuerzas)
ax1.annotate(f"Rb={Rb:.1f} kN", xy=(L, -0.2), xytext=(L, -1.8),
             arrowprops=dict(facecolor=c_fuerzas, edgecolor=c_fuerzas, shrink=0.05, width=2, headwidth=8),
             ha='center', fontweight='bold', color=c_fuerzas)

# Carga Puntual P
if P > 0:
    ax1.annotate(f"{P} kN", xy=(a, 0.2), xytext=(a, 2.5),
                 arrowprops=dict(facecolor=c_momento, edgecolor=c_momento, shrink=0.05, width=3, headwidth=10),
                 ha='center', fontweight='bold', color=c_momento)

# Carga Distribuida w
if w > 0:
    for wx in np.linspace(0, L, max(5, int(L)*2)):
        ax1.annotate("", xy=(wx, 0.2), xytext=(wx, 1.2),
                     arrowprops=dict(facecolor=c_corte, edgecolor=c_corte, shrink=0.05, width=1, headwidth=5))
    ax1.text(L/2, 1.5, f"w = {w} kN/m", ha='center', fontweight='bold', color=c_corte)

# -- Gráfico 2: Diagrama de Fuerza Cortante (V) --
ax2.set_facecolor('none')
ax2.plot(x, V, color=c_corte, lw=2)
ax2.fill_between(x, V, 0, alpha=0.3, color=c_corte)
ax2.axhline(0, color='black', lw=1)
ax2.set_ylabel("Fuerza Cortante V (kN)", fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)

# -- Gráfico 3: Diagrama de Momento Flector (M) --
ax3.set_facecolor('none')
ax3.plot(x, M, color=c_momento, lw=2)
ax3.fill_between(x, M, 0, alpha=0.3, color=c_momento)
ax3.axhline(0, color='black', lw=1)
ax3.set_xlabel("Posición en la viga x (m)", fontweight='bold')
ax3.set_ylabel("Momento Flector M (kN·m)", fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.5)

# Invertir el eje Y del momento flector (convención común en ingeniería estructural)
ax3.invert_yaxis() 

st.pyplot(fig)

# --- 5. RESUMEN DE RESULTADOS MÁXIMOS ---
col1, col2, col3 = st.columns(3)
col1.metric("Reacción Izquierda (Ra)", f"{Ra:.2f} kN")
col2.metric("Fuerza Cortante Máxima (|V| max)", f"{np.max(np.abs(V)):.2f} kN")
col3.metric("Momento Flector Máximo (M max)", f"{np.max(M):.2f} kN·m")
