import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Extractor de Tablas Pro", page_icon="🌐")

st.title("🌐 Extractor de Tablas con Vista Previa")

# 1. Inicializar el Session State si no existe
if 'tablas' not in st.session_state:
    st.session_state.tablas = None

url = st.text_input("Ingrese la URL de la página:")

# Botón para extraer (solo ocurre una vez al hacer clic)
if st.button("Extraer Tablas"):
    if url:
        try:
            with st.spinner('Extrayendo datos...'):
                # Guardamos el resultado directamente en el estado de la sesión
                st.session_state.tablas = pd.read_html(url)
                st.success(f"Se encontraron {len(st.session_state.tablas)} tablas.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Por favor, ingresa una URL.")

# 2. Si ya hay tablas en la memoria, mostrar las opciones de interacción
if st.session_state.tablas:
    st.divider()
    
    # Selector de tabla para vista previa
    opciones = [f"Tabla {i+1}" for i in range(len(st.session_state.tablas))]
    seleccion = st.selectbox("Seleccione la tabla que desea previsualizar:", opciones)
    
    # Obtener el índice numérico de la selección
    indice = opciones.index(seleccion)
    
    st.subheader(f"Vista previa de: {seleccion}")
    st.dataframe(st.session_state.tablas[indice])

    # Lógica de descarga (usa todas las tablas guardadas en memoria)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        for i, df in enumerate(st.session_state.tablas):
            df.to_excel(writer, sheet_name=f"Tabla_{i+1}", index=False)
    
    st.download_button(
        label="📥 Descargar todas las tablas en Excel",
        data=buffer.getvalue(),
        file_name="tablas_extraidas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Botón para limpiar la sesión y empezar de nuevo
    if st.button("Limpiar resultados"):
        st.session_state.tablas = None
        st.rerun()

### ¿Qué cambió exactamente?

1.  **`st.session_state.tablas`**: Ahora los datos no viven en una variable común, sino en un contenedor que Streamlit respeta aunque la página se recargue.
2.  **Lógica fuera del botón**: El `st.selectbox` y el `st.dataframe` están en un bloque `if st.session_state.tablas:`. Esto significa que una vez que extraes los datos, estos controles aparecerán y se mantendrán visibles sin importar cuántas veces cambies la selección.
3.  **Botón de Limpieza**: Agregamos una opción para resetear el estado y permitir una nueva búsqueda limpia.

¡Tu aplicación ahora se siente mucho más profesional y fluida! ¿Te gustaría añadirle algo más?
