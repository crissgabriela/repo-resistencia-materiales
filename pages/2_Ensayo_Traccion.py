import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="wide")
st.title("Laboratorio Virtual: Ensayo de Tracción")
st.markdown("Analiza el comportamiento mecánico de diferentes materiales sometidos a carga axial.")

# 1. Base de datos de materiales (Valores aproximados en MPa)
materiales = {
    "Acero Estructural (A36)": {"E": 200000, "Sy": 250, "Su": 400, "ef": 0.25},
    "Aluminio (6061-T6)": {"E": 69000, "Sy": 276, "Su": 310, "ef": 0.12},
    "Cobre Recocido": {"E": 110000, "Sy": 33, "Su": 210, "ef": 0.45}
}

# 2. Interfaz lateral
st.sidebar.header("Parámetros del Ensayo")
mat_seleccionado = st.sidebar.selectbox("Selecciona el Material", list(materiales.keys()))
mat = materiales[mat_seleccionado]

# Slider que actúa como el motor de la máquina de tracción
progreso = st.sidebar.slider("Progreso del Ensayo (Deformación %)", 0.0, mat["ef"] * 100, 0.0, step=0.1)
eps_actual = progreso / 100.0

# 3. Modelo Matemático de la Curva Esfuerzo-Deformación
def calcular_esfuerzo(eps, mat):
    ey = mat["Sy"] / mat["E"] # Deformación de fluencia
    eu = mat["ef"] * 0.6      # Aproximación de deformación última
    
    if eps <= ey:
        # Zona Elástica (Ley de Hooke)
        return mat["E"] * eps
    elif eps <= eu:
        # Zona Plástica (Endurecimiento por deformación - Aproximación parabólica)
        return mat["Sy"] + (mat["Su"] - mat["Sy"]) * ((eps - ey) / (eu - ey))**0.5
    else:
        # Zona de Estricción (Caída del esfuerzo nominal)
        return mat["Su"] - (mat["Su"] * 0.15) * ((eps - eu) / (mat["ef"] - eu))**2

# Generar datos para el gráfico de fondo
eps_total = np.linspace(0, mat["ef"], 200)
sig_total = [calcular_esfuerzo(e, mat) for e in eps_total]

# Calcular el esfuerzo en el instante actual del slider
sig_actual = calcular_esfuerzo(eps_actual, mat)

# 4. Configuración de Columnas para Visualización
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Curva Esfuerzo - Deformación")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    # Dibujar la curva completa en gris claro como "guía"
    ax.plot(eps_total, sig_total, color='lightgray', linestyle='--', label="Curva Teórica")
    
    # Dibujar la curva real hasta el progreso actual
    eps_progreso = np.linspace(0, eps_actual, 50)
    sig_progreso = [calcular_esfuerzo(e, mat) for e in eps_progreso]
    ax.plot(eps_progreso, sig_progreso, color='#c72979', linewidth=3, label="Ensayo en curso")
    
    # Punto actual
    ax.scatter(eps_actual, sig_actual, color='#00aeef', s=100, zorder=5)
    
    # Zonas e hitos
    ax.axvline(x=mat["Sy"]/mat["E"], color='#46247a', linestyle=':', alpha=0.5)
    ax.text(mat["Sy"]/mat["E"], mat["Sy"], ' Fluencia', color='#46247a')
    
    ax.set_xlabel("Deformación Unitaria $\epsilon$ (mm/mm)")
    ax.set_ylabel("Esfuerzo Nominal $\sigma$ (MPa)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    
    st.pyplot(fig)

with col2:
    st.subheader("Probeta Virtual")
    fig2, ax2 = plt.subplots(figsize=(3, 5))
    fig2.patch.set_alpha(0.0)
    ax2.set_facecolor('none')
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-1, 11)
    ax2.axis('off')
    
    # Geometría de la probeta dependiente de la deformación
    L0 = 8.0
    W0 = 1.5
    L_actual = L0 * (1 + eps_actual)
    
    # Simulación visual del coeficiente de Poisson y estricción
    W_actual = W0 * (1 - 0.3 * eps_actual) # Reducción de área general
    
    eu = mat["ef"] * 0.6
    if eps_actual > eu:
        # Si pasa el esfuerzo último, simulamos la estricción (cuello) en el centro
        estriccion = 1 - 0.4 * ((eps_actual - eu) / (mat["ef"] - eu))
        W_centro = W_actual * estriccion
        # Dibujar probeta con cuello usando un polígono
        y_pts = [0, L_actual*0.3, L_actual*0.5, L_actual*0.7, L_actual]
        x_pts = [W_actual/2, W_actual/2, W_centro/2, W_actual/2, W_actual/2]
        ax2.plot(x_pts, y_pts, color='#2d2d2d', lw=2)
        ax2.plot([-x for x in x_pts], y_pts, color='#2d2d2d', lw=2)
        ax2.fill_betweenx(y_pts, [-x for x in x_pts], x_pts, color='#00aeef', alpha=0.5)
    else:
        # Dibujar probeta recta
        probeta = patches.Rectangle((-W_actual/2, 0), W_actual, L_actual, linewidth=2, edgecolor='#2d2d2d', facecolor='#00aeef', alpha=0.5)
        ax2.add_patch(probeta)
        
    # Mordazas fijas
    ax2.add_patch(patches.Rectangle((-1.5, -1), 3, 1, color='#46247a'))
    ax2.add_patch(patches.Rectangle((-1.5, L_actual), 3, 1, color='#46247a'))
    
    # Texto de datos en tiempo real
    ax2.text(0, L_actual + 1.5, f"$\sigma$: {sig_actual:.1f} MPa\n$\epsilon$: {eps_actual:.3f}", ha='center', fontsize=12, fontweight='bold')
    
    st.pyplot(fig2)
