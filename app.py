import streamlit as st
from agente_calendar import agente

st.title("📅 Agente de Calendario")
st.write("Escribe lo que quieres agregar a tu calendario en lenguaje natural")

mensaje = st.text_input("¿Qué quieres agendar?", placeholder="Ejemplo: Tengo una reunion mañana a las 4pm")

if st.button("Agregar al Calendar"):
    if mensaje:
        resultado = agente(mensaje)
        st.success("¡Evento agregado!")
    else:
        st.warning("Escribe algo primero")