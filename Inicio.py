import streamlit as st

st.set_page_config(
    page_title="Resistencia de Materiales | MakerBox",
    page_icon="🏗️",
    layout="wide"
)

st.title("Laboratorio Virtual: Resistencia de Materiales")
st.subheader("Facultad de Ingeniería - Universidad de Talca")

st.markdown("""
Les damos la bienvenida al entorno interactivo de Resistencia de Materiales. 

Este espacio está diseñado para complementar las clases teóricas con herramientas de simulación y cálculo en tiempo real.

### ¿Qué encontrarán aquí?
En el menú lateral podrán acceder a las distintas aplicaciones desarrolladas para este módulo:

* **1. Vigas:** Analizador de estática, donde podrán calcular reacciones y visualizar los diagramas de fuerza cortante (DFC) y momento flector (DMF) para vigas simplemente apoyadas.
* **2. Ensayo de Tracción:** Simulador del comportamiento mecánico de distintos materiales bajo carga axial. Podrán interactuar con la curva esfuerzo-deformación y observar las zonas elástica, plástica y de estricción.

👈 **Seleccionen una herramienta en el menú de la izquierda para comenzar.**

---
*Plataforma de apoyo docente desarrollada por Criss Carreño.*
""")
