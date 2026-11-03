import streamlit as st
from google import genai
from gtts import gTTS
import io

# Configuración inicial de la página
st.set_page_config(
    page_title="FutAnalytix",
    page_icon="⚽",
    layout="wide"
)

# Estilos CSS personalizados (Aesthetic: Azul rey, textos blancos, botones verde limón y azul celeste)
st.markdown("""
    <style>
    /* Fondo general de la aplicación (Azul Rey) */
    .stApp {
        background-color: #0B192C;
        color: #FFFFFF;
    }
    
    /* Textos principales */
    h2, h3, h4, h5, h6, p, span, label {
        color: #FFFFFF !important;
    }
    
    /* Botones principales con acento en Verde Limón */
    .stButton>button {
        background-color: #00FF66;
        color: #0B192C;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #00CC52;
        color: #FFFFFF;
    }
    
    /* Elementos interactivos secundarios con Azul Celeste */
    .metric-card {
        background-color: #1E3E62;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00B4D8;
    }
    
    /* Cajas de texto y selectores */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #1E3E62;
        color: #FFFFFF;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración del cliente Gemini utilizando los Secrets de Streamlit
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=gemini_api_key)
except Exception as e:
    client = None

# Título principal profesional y moderno con toque de alta seguridad corporativa
st.markdown("""
    <h1 style='font-family: sans-serif; font-weight: 800; font-size: 2.8rem; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 0px;'>
        Fut<span style='color: #00B4D8;'>Analytix</span>
    </h1>
""", unsafe_allow_html=True)

# Subtítulo solicitado
st.markdown("<p style='font-size: 1.2rem; color: #00B4D8; margin-top: 5px; margin-bottom: 25px;'>Asistente AI para analizar fútbol en vivo</p>", unsafe_allow_html=True)

# Sección de consulta y análisis con Gemini
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🤖 Asistente Táctico y de Apuestas (Gemini)")
    prompt_usuario = st.text_area("Consulta sobre un partido, estadísticas de clubes (Stuttgart, Man City, Milan, Juventus) o análisis de probabilidades:", 
                                  placeholder="Ej: Analiza el riesgo y probabilidades para el próximo partido...")
    
    if st.button("Generar Análisis Proactivo"):
        if not client:
            st.error("⚠️ Falta configurar la `GEMINI_API_KEY` en los Secrets de Streamlit Cloud.")
        elif not prompt_usuario.strip():
            st.warning("Por favor ingresa una consulta para el análisis.")
        else:
            with st.spinner("Analizando variables del encuentro con Inteligencia Artificial..."):
                try:
                    # Usando el modelo de Gemini para generar el análisis deportivo
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Eres un experto analista de datos de fútbol y gestión de riesgos en apuestas deportivas. Responde de forma estructurada, profesional y directa al siguiente análisis: {prompt_usuario}"
                    )
                    st.success("¡Análisis completado!")
                    st.markdown(f"<div class='metric-card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    # Generar audio con gTTS para lectura de alertas
                    tts = gTTS(text=response.text[:500], lang='es')
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    st.audio(audio_buffer, format='audio/mp3')
                    
                except Exception as err:
                    st.error(f"Error al conectar con la API de Gemini: {err}")

with col2:
    st.subheader("📊 Métricas Rápidas")
    st.markdown("<div class='metric-card'><b>Estado del Sistema:</b> <span style='color: #00FF66;'>Activo 🟢</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='metric-card'><b>Monitoreo de Clubes:</b><br>• Stuttgart<br>• Manchester City<br>• Milan<br>• Juventus</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #00B4D8;'>FutAnalytix © 2026 - Todos los derechos reservados</p>", unsafe_allow_html=True)
