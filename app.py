import streamlit as st
import pandas as pd
import io

# Título y descripción
st.title("🌐 Extractor de Tablas a Excel")
st.write("Ingresa el enlace de una página web. La aplicación buscará todas las tablas disponibles y te permitirá descargarlas en un único archivo de Excel (una tabla por hoja).")

# Input para la URL
url = st.text_input("Ingrese la URL de la página:")

if st.button("Extraer Tablas"):
    if url:
        try:
            with st.spinner('Analizando la página y extrayendo datos...'):
                # pd.read_html devuelve una lista de DataFrames
                lista_tablas = pd.read_html(url)
            
            st.success(f"¡Éxito! Se encontraron {len(lista_tablas)} tablas en la página.")
            
            # Crear un buffer en memoria para guardar el Excel sin usar el disco duro
            buffer = io.BytesIO()
            
            # Usar ExcelWriter para guardar múltiples hojas
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                for i, df in enumerate(lista_tablas):
                    # Nombramos cada hoja de forma secuencial
                    nombre_hoja = f"Tabla_{i+1}"
                    df.to_excel(writer, sheet_name=nombre_hoja, index=False)
            
            # Preparar el botón de descarga
            st.download_button(
                label="📥 Descargar archivo Excel",
                data=buffer.getvalue(),
                file_name="datos_extraidos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Mostrar una vista previa de la primera tabla como validación visual
            st.subheader("Vista previa de la primera tabla encontrada:")
            st.dataframe(lista_tablas[0])

        except ValueError:
            st.error("No se encontraron tablas HTML en esta URL. Es posible que los datos estén ocultos o cargados dinámicamente.")
        except Exception as e:
            st.error(f"Ocurrió un error al intentar leer la página: {e}")
    else:
        st.warning("Por favor, ingresa un enlace antes de presionar el botón.")