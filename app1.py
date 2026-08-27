import streamlit as st
import cv2
import numpy as np
import pytesseract

# Configuración de la página
st.set_page_config(
    page_title="Scanner OCR Studio",
    page_icon="✨",
    layout="wide"
)

# Estilos CSS personalizados (Colores, bordes redondeados y efectos)
st.markdown("""
    <style>
    /* Fondo general de la app */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Titular con texto degradado */
    .gradient-title {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Estilo de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 1px solid #334155;
    }

    /* Tarjetas de contenido con bordes muy suaves */
    div[data-testid="stVerticalBlock"] > div:has(div.card-container) {
        background-color: #1E293B;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Personalización del botón de descarga */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    
    div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
        background: linear-gradient(135deg, #4F46E5 0%, #9333EA 100%);
    }

    /* Formato del área de texto resultante */
    textarea {
        background-color: #0F172A !important;
        color: #38BDF8 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado estilizado
st.markdown("<h1 class='gradient-title'>✨ Scanner OCR Studio</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Procesamiento óptico de caracteres con estilo visual moderno</p>", unsafe_allow_html=True)

# Barra lateral con diseño ajustado
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    st.divider()
    filtro = st.radio("Ajuste de Filtro:", ('Sin Filtro', 'Con Filtro (Invertir colores)'))
    
    st.markdown("---")
    st.info("💡 **Tip de captura:** Invertir los colores facilita la lectura en textos blancos con fondos oscuros.")

# Entrada de la cámara
img_file_buffer = st.camera_input("📷 Haz clic abajo para tomar una foto")

if img_file_buffer is not None:
    # Procesamiento con OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Con Filtro (Invertir colores)':
        cv2_img = cv2.bitwise_not(cv2_img)
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    
    st.write("") # Espaciador
    
    # Distribución en 2 columnas dentro de contenedores estilizados
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card-container"></div>', unsafe_allow_html=True)
        st.markdown("### 🖼️ Imagen Procesada")
        st.image(img_rgb, use_column_width=True)
        
    with col2:
        st.markdown('<div class="card-container"></div>', unsafe_allow_html=True)
        st.markdown("### 📄 Resultado Digital")
        
        if text.strip():
            st.text_area("Texto Detectado", value=text, height=260, label_visibility="collapsed")
            st.write("")
            st.download_button(
                label="⚡ DESCARGAR TEXTO DETECTADO",
                data=text,
                file_name="texto_extraido.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("⚠️ No se detectó texto en la imagen. Intenta con mejor iluminación o cambiando el filtro.")
