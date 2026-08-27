import streamlit as st
import cv2
import numpy as np
import pytesseract

# Configuración de la página para aprovechar todo el ancho del navegador
st.set_page_config(
    page_title="Scanner OCR Pro",
    page_icon="🔍",
    layout="wide"
)

# Estilo personalizado básico con CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #2C3E50;
        margin-bottom: 2rem;
    }
    .stText {
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown("<h1 class='main-title'>🔍 Reconocimiento Óptico de Caracteres (OCR)</h1>", unsafe_allow_html=True)
st.caption("Captura una imagen desde tu cámara para extraer el texto automáticamente.")
st.divider()

# Barra lateral con controles
with st.sidebar:
    st.header("⚙️ Configuración")
    filtro = st.radio("Filtro de imagen:", ('Sin Filtro', 'Con Filtro (Invertir colores)'))
    st.info("💡 Tip: Invertir los colores ayuda a Tesseract a leer texto claro sobre fondos oscuros.")

# Área principal de la aplicación
img_file_buffer = st.camera_input("Toma una foto")

if img_file_buffer is not None:
    # Procesamiento de la imagen con OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Con Filtro (Invertir colores)':
        cv2_img = cv2.bitwise_not(cv2_img)
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    
    st.divider()
    
    # Distribución en 2 columnas para el resultado visual
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Imagen procesada")
        st.image(img_rgb, use_column_width=True, caption="Vista previa utilizada para la lectura")
        
    with col2:
        st.subheader("📄 Texto detectado")
        
        if text.strip():
            # Muestra el texto procesado dentro de una caja destacada
            st.text_area("Resultado OCR", value=text, height=300)
            st.success("¡Lectura completada con éxito!")
            
            # Botón opcional para copiar/descargar el texto
           with st.expander("💾 Opciones de exportación", expanded=True):
    st.write("Guarda el texto escaneado directamente en tu dispositivo:")
    st.download_button(
        label="📄 Guardar como archivo .TXT",
        data=text,
        file_name="escaneo_ocr.txt",
        mime="text/plain",
        use_container_width=True
    )


