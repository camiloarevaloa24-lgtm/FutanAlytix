import streamlit as st
import sqlite3
from google import genai
from gtts import gTTS
import io

# Configuración inicial de la página
st.set_page_config(
    page_title="FutAnalytix",
    page_icon="⚽",
    layout="wide"
)

# Estética visual intacta (Azul rey, textos blancos, verde limón)
st.markdown("""
    <style>
    .stApp {
        background-color: #0B192C;
        color: #FFFFFF;
    }
    h2, h3, h4, h5, h6, p, span, label {
        color: #FFFFFF !important;
    }
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
    .stTextInput>div>div>input {
        background-color: #1E3E62;
        color: #FFFFFF;
        border-radius: 6px;
        border: 1px solid #00B4D8;
    }
    .metric-card {
        background-color: #1E3E62;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00B4D8;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración de la base de datos persistente (SQLite)
def init_db():
    conn = sqlite3.connect('futanalytix_usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            cedula TEXT PRIMARY KEY,
            correo TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Configuración del cliente Gemini
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=gemini_api_key)
except Exception as e:
    client = None

# Estados de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

# Título principal y subtítulo (INTACTOS)
st.markdown("""
    <h1 style='font-family: sans-serif; font-weight: 800; font-size: 2.8rem; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 0px;'>
        Fut<span style='color: #00B4D8;'>Analytix</span>
    </h1>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size: 1.2rem; color: #00B4D8; margin-top: 5px; margin-bottom: 30px;'>Asistente AI para analizar fútbol en vivo</p>", unsafe_allow_html=True)

# ==========================================
# VISTA 1: LOGIN O REGISTRO (PANTALLA DE ACCESO)
# ==========================================
if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    
    with col_l2:
        # Pantalla de Registro Completo (si hace clic en Registrarse)
        if st.session_state.mostrar_registro:
            st.markdown("### 📝 Registro de Usuario Nuevo")
            correo = st.text_input("Ingresar correo electrónico")
            cedula = st.text_input("Número de cédula")
            nueva_contrasena = st.text_input("Crear contraseña", type="password")
            confirmar_contrasena = st.text_input("Confirmar contraseña", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_reg1, col_reg2 = st.columns(2)
            with col_reg1:
                if st.button("Registrarse", use_container_width=True):
                    if not correo or not cedula or not nueva_contrasena or not confirmar_contrasena:
                        st.warning("Por favor completa todos los campos.")
                    elif nueva_contrasena != confirmar_contrasena:
                        st.error("Las contraseñas no coinciden.")
                    else:
                        try:
                            conn = sqlite3.connect('futanalytix_usuarios.db')
                            cursor = conn.cursor()
                            cursor.execute('INSERT INTO usuarios (cedula, correo, password) VALUES (?, ?, ?)', (cedula, correo, nueva_contrasena))
                            conn.commit()
                            conn.close()
                            
                            st.session_state.autenticado = True
                            st.session_state.usuario_actual = cedula
                            st.session_state.mostrar_registro = False
                            st.success("¡Registro exitoso!")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Esta cédula ya se encuentra registrada. Por favor inicia sesión.")
                            
            with col_reg2:
                if st.button("Volver al Inicio", use_container_width=True):
                    st.session_state.mostrar_registro = False
                    st.rerun()

        # Pantalla de Inicio de Sesión Normal
        else:
            cedula_login = st.text_input("Número de Cédula (Usuario)")
            contrasena_login = st.text_input("Contraseña", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Registrarse", use_container_width=True):
                    st.session_state.mostrar_registro = True
                    st.rerun()
            with col_b2:
                if st.button("Iniciar Sesión", use_container_width=True):
                    if not cedula_login or not contrasena_login:
                        st.warning("Por favor ingresa tu cédula y contraseña.")
                    else:
                        conn = sqlite3.connect('futanalytix_usuarios.db')
                        cursor = conn.cursor()
                        cursor.execute('SELECT * FROM usuarios WHERE cedula = ? AND password = ?', (cedula_login, contrasena_login))
                        user = cursor.fetchone()
                        conn.close()
                        
                        if user:
                            st.session_state.autenticado = True
                            st.session_state.usuario_actual = cedula_login
                            st.success("¡Inicio de sesión exitoso!")
                            st.rerun()
                        else:
                            st.error("Cédula o contraseña incorrectas, o el usuario no existe.")
                            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Olvidé mi contraseña", use_container_width=True):
                st.info("Instrucciones de recuperación enviadas a tu sistema registrado.")

# ==========================================
# VISTA 2: DENTRO DE LA APLICACIÓN (YA INICIÓ SESIÓN)
# ==========================================
else:
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.markdown(f"<p style='color: #00B4D8;'>Sesión activa - Cédula: <b>{st.session_state.usuario_actual}</b></p>", unsafe_allow_html=True)
    with col_top2:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()

    col1, col2 = st.columns([2, 1])

    with col1:
        # Aquí es donde se abre la aplicación con el botón/recuadro para subir la imagen de la apuesta
        st.subheader("📸 Subir Imagen de Apuesta")
        imagen_apuesta = st.file_uploader("Descarga o sube la imagen de tu apuesta aquí", type=['png', 'jpg', 'jpeg'])
        
        if imagen_apuesta is not None:
            st.success("¡Imagen cargada correctamente!")
            st.image(imagen_apuesta, caption="Apuesta cargada", use_column_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🤖 Asistente Táctico y de Apuestas (Gemini)")
        prompt_usuario = st.text_area("Consulta sobre un partido, estadísticas de clubes o análisis de probabilidades:", 
                                      placeholder="Ej: Analiza el riesgo y probabilidades para el próximo partido...")
        
        if st.button("Generar Análisis Proactivo"):
            if not client:
                st.error("⚠️ Falta configurar la `GEMINI_API_KEY` en los Secrets de Streamlit Cloud.")
            elif not prompt_usuario.strip():
                st.warning("Por favor ingresa una consulta para el análisis.")
            else:
                with st.spinner("Analizando variables con Inteligencia Artificial..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=f"Eres un experto analista de datos de fútbol. Responde al siguiente análisis: {prompt_usuario}"
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
