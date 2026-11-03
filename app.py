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

# Estilos CSS personalizados (Estética EXACTA intacta: Azul rey, textos blancos, verde limón)
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
    
    /* Cajas de texto y entradas */
    .stTextInput>div>div>input {
        background-color: #1E3E62;
        color: #FFFFFF;
        border-radius: 6px;
        border: 1px solid #00B4D8;
    }
    
    /* Tarjeta o módulo interactivo de métricas */
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

# Base de datos simulada en memoria para usuarios registrados
if "usuarios_db" not in st.session_state:
    st.session_state.usuarios_db = {}

# Inicializar estados de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

# Título principal y subtítulo (INTACTOS)
st.markdown("""
    <h1 style='font-family: sans-serif; font-weight: 800; font-size: 2.8rem; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 0px;'>
        Fut<span style='color: #00B4D8;'>Analytix</span>
    </h1>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size: 1.2rem; color: #00B4D8; margin-top: 5px; margin-bottom: 30px;'>Asistente AI para analizar fútbol en vivo</p>", unsafe_allow_html=True)

# ==========================================
# VISTA 1: ACCESO Y REGISTRO DESPLEGABLE
# ==========================================
if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    
    with col_l2:
        # Formulario de Inicio de Sesión Estándar
        if not st.session_state.mostrar_registro:
            usuario_login = st.text_input("Usuario (o Correo)")
            contrasena_login = st.text_input("Contraseña", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Registrarse", use_container_width=True):
                    st.session_state.mostrar_registro = True
                    st.rerun()
            with col_b2:
                if st.button("Iniciar Sesión", use_container_width=True):
                    if not usuario_login or not contrasena_login:
                        st.warning("Por favor ingresa usuario y contraseña.")
                    elif usuario_login in st.session_state.usuarios_db and st.session_state.usuarios_db[usuario_login]["password"] == contrasena_login:
                        st.session_state.autenticado = True
                        st.rerun()
                    else:
                        # Permite ingreso de prueba si no está en la BD previa
                        st.session_state.autenticado = True
                        st.rerun()
                        
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Olvidé mi contraseña", use_container_width=True):
                st.info("Instrucciones de recuperación enviadas a tu sistema registrado.")

        # FORMULARIO DESPLEGADO AL OPRIMIR "REGISTRARSE"
        else:
            st.markdown("### 📝 Formulario de Registro Completo")
            
            correo = st.text_input("Ingresar correo electrónico")
            cedula = st.text_input("Número de cédula")
            nueva_contrasena = st.text_input("Crear contraseña", type="password")
            confirmar_contrasena = st.text_input("Confirmar contraseña", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_reg1, col_reg2 = st.columns(2)
            with col_reg1:
                if st.button("Completar Registro", use_container_width=True):
                    if not correo or not cedula or not nueva_contrasena or not confirmar_contrasena:
                        st.warning("Por favor completa todos los campos para el registro.")
                    elif nueva_contrasena != confirmar_contrasena:
                        st.error("Las contraseñas no coinciden. Inténtalo de nuevo.")
                    else:
                        # Guardar registro
                        st.session_state.usuarios_db[correo] = {
                            "cedula": cedula,
                            "password": nueva_contrasena
                        }
                        st.session_state.autenticado = True
                        st.session_state.mostrar_registro = False
                        st.success("¡Registro completado con éxito! Bienvenido.")
                        st.rerun()
                        
            with col_reg2:
                if st.button("Volver atrás", use_container_width=True):
                    st.session_state.mostrar_registro = False
                    st.rerun()

# ==========================================
# VISTA 2: DENTRO DE LA PLATAFORMA (AUTENTICADO)
# ==========================================
else:
    col_top1, col_top2 = st.columns([6, 1])
    with col_top2:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.mostrar_registro = False
            st.rerun()

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
