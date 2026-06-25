import streamlit as st

#titulo
st.title("Mi primera app con python")

#texto
st.write("Bienvenido")

#saludar
nombre = st.text_input("Ingrese el nombre")

if st.button("Saludar"):
    st.success(f"Hola {nombre} ¿como estas?")