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
        padding: 0.6rem 1rem;
    }
    .stButton>button:hover {
        background-color: #00CC52;
        color: #FFFFFF;
    }
    
    /* Cajas de texto y selectores */
    .stTextInput>div>div>input {
        background-color: #1E3E62;
        color: #FFFFFF;
        border-radius: 6px;
        border: 1px solid #00B4D8;
    }
    
    /* Elementos interactivos secundarios con Azul Celeste */
    .metric-card {
        background-color: #1E3E62;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00B4D8;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración del cliente Gemini utilizando los Secrets de Streamlit
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=gemini_api_key)
except Exception as e:
    client = None

# Inicializar el estado de la sesión para saber si el usuario ha iniciado sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Título principal profesional y moderno (Intacto)
st.markdown("""
    <h1 style='font-family: sans-serif; font-weight: 800; font-size: 2.8rem; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 0px;'>
        Fut<span style='color: #00B4D8;'>Analytix</span>
    </h1>
""", unsafe_allow_html=True)

# Subtítulo solicitado (Intacto)
st.markdown("<p style='font-size: 1.2rem; color: #00B4D8; margin-top: 5px; margin-bottom: 30px;'>Asistente AI para analizar fútbol en vivo</p>", unsafe_allow_html=True)

# ==========================================
# VISTA 1: SI NO HA INICIADO SESIÓN (REGISTRO / ACCESO)
# ==========================================
if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    
    with col_l2:
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Registrarse", use_container_width=True):
                if not usuario or not contrasena:
                    st.warning("Por favor ingresa usuario y contraseña.")
                else:
                    st.session_state.autenticado = True
                    st.success("¡Registro exitoso!")
                    st.rerun()
        with col_b2:
            if st.button("Iniciar Sesión", use_container_width=True):
                if not usuario or not contrasena:
                    st.warning("Por favor ingresa tus datos.")
                else:
                    st.session_state.autenticado = True
                    st.rerun()
                    
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Olvidé mi contraseña", use_container_width=True):
            st.info("Instrucciones de recuperación enviadas a tu sistema registrado.")

# ==========================================
# VISTA 2: SI YA ESTÁ AUTENTICADO (PLATAFORMA PRINCIPAL)
# ==========================================
else:
    # Botón para cerrar sesión en la esquina superior
    col_top1, col_top2 = st.columns([6, 1])
    with col_top2:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

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
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=f"Eres un experto analista de datos de fútbol y gestión de riesgos en apuestas deportivas. Responde de forma estructurada, profesional y directa al siguiente análisis: {prompt_usuario}"
                        )
                        st.success("¡Análisis completado!")
                        st.markdown(f"<div class='metric-card'>{response.text}</div>", unsafe_allow_html=True)
                        
                        # Generar audio con gTTS
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
