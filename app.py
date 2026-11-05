import streamlit as st
import sqlite3
from google import genai

# Configuración inicial de la página (INTACTA)
st.set_page_config(
    page_title="FutAnalytix",
    page_icon="⚽",
    layout="wide"
)

# Estética visual intacta
st.markdown("""
    <style>
    .stApp {
        background-color: #0B192C;
        color: #FFFFFF;
    }
    h2, h3, h4, h5, h6, p, span, label {
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .stButton>button {
        background-color: #00FF66;
        color: #0B192C;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
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
    
    /* Botón exclusivo de Enfrentamientos en Azul Claro Elegante */
    div[element-id="btn_enfrentamientos"] > button {
        background-color: #00B4D8 !important;
        color: #0B192C !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.6px !important;
        border-radius: 8px !important;
        border: 1px solid #90E0EF !important;
        box-shadow: 0 2px 8px rgba(0, 180, 216, 0.3) !important;
    }
    div[element-id="btn_enfrentamientos"] > button:hover {
        background-color: #48CAE4 !important;
        color: #0B192C !important;
        box-shadow: 0 4px 12px rgba(72, 202, 228, 0.5) !important;
    }

    /* Personalización para el recuadro de subida más cuadrado y legible */
    [data-testid="stFileUploader"] {
        background-color: #1E3E62;
        border: 2px dashed #00B4D8;
        border-radius: 8px;
        padding: 20px;
    }
    [data-testid="stFileUploader"] section {
        padding: 10px;
    }
    [data-testid="stFileUploader"] button {
        background-color: #00FF66 !important;
        color: #0B192C !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #00CC52 !important;
        color: #FFFFFF !important;
    }
    .metric-card {
        background-color: #1E3E62;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00B4D8;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Base de datos SQLite (INTACTA)
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

# Configuración del cliente Gemini para el análisis deportivo
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=gemini_api_key)
except Exception:
    client = None

# Estados de sesión (INTACTOS + Estado de navegación para los enfrentamientos)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

if "lista_apuestas" not in st.session_state:
    st.session_state.lista_apuestas = []

if "ver_enfrentamientos" not in st.session_state:
    st.session_state.ver_enfrentamientos = False

# Título principal y subtítulo (INTACTOS)
st.markdown("""
    <h1 style='font-family: sans-serif; font-weight: 800; font-size: 2.8rem; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 0px;'>
        Fut<span style='color: #00B4D8;'>Analytix</span>
    </h1>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size: 1.2rem; color: #00B4D8; margin-top: 5px; margin-bottom: 30px;'>Asistente AI en vivo para tus apustas</p>", unsafe_allow_html=True)

# ==========================================
# VISTA 1: ACCESO (INGRESAR / REGISTRARSE)
# ==========================================
if not st.session_state.autenticado:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    
    with col_l2:
        if st.session_state.mostrar_registro:
            st.markdown("### Registro de Usuario Nuevo")
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
# VISTA 2: DENTRO DE LA APLICACIÓN
# ==========================================
else:
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.markdown("<p style='color: #00B4D8; font-weight: 600; letter-spacing: 0.5px;'>Sesión Activa</p>", unsafe_allow_html=True)
        
        # Botón estilizado en Azul Claro debajo de "Sesión Activa"
        st.markdown("<div element-id='btn_enfrentamientos'>", unsafe_allow_html=True)
        if st.button("Consultar ultimos enfrentamientos del equipo"):
            st.session_state.ver_enfrentamientos = not st.session_state.ver_enfrentamientos
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_top2:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.session_state.lista_apuestas = []
            st.session_state.ver_enfrentamientos = False
            st.rerun()

    # ==========================================
    # SECCIÓN: MÓDULO DE ÚLTIMOS ENFRENTAMIENTOS Y ANÁLISIS
    # ==========================================
    if st.session_state.ver_enfrentamientos:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Consultar Últimos Enfrentamientos y Análisis de Equipo")
        st.markdown("<p style='color: #00B4D8;'>Ingresa el nombre del equipo de fútbol para generar el informe completo con los últimos 6 partidos oficiales, plantilla, estadísticas y análisis inteligente.</p>", unsafe_allow_html=True)
        
        equipo_input = st.text_input("Nombre del equipo", placeholder="Ej: Real Madrid, Millonarios, Manchester City...")
        
        col_bus1, col_bus2 = st.columns([1, 4])
        with col_bus1:
            btn_buscar = st.button("Buscar Equipo")
        with col_bus2:
            if st.button("Regresar al Gestor de Apuestas"):
                st.session_state.ver_enfrentamientos = False
                st.rerun()

        if btn_buscar:
            if not client:
                st.error("⚠️ Configura la `GEMINI_API_KEY` en los Secrets de tu aplicación.")
            elif not equipo_input.strip():
                st.warning("Por favor ingresa un nombre de equipo válido.")
            else:
                with st.spinner(f"Consultando últimos datos y estadísticas de {equipo_input}..."):
                    prompt_analisis = f"""
                    Actúa como un experto analista de datos de fútbol y estadísticas deportivas. 
                    Para el equipo de fútbol '{equipo_input}', genera un informe ejecutivo estructurado exactamente con los siguientes 3 bloques utilizando formato Markdown (tablas nativas de Markdown y viñetas):

                    1. **Últimos 6 partidos oficiales:**
                       Genera una tabla con las columnas exactas: | Fecha | Competición | Rival | Marcador | Resultado |. (Indica claramente si ganó, empató o perdió).

                    2. **Posición y rendimiento en el torneo actual:**
                       Genera una tabla con las columnas exactas: | Competición | Posición | PJ | PG | PE | PP | GF | GC | Puntos |. (Muestra en qué parte de la tabla va o si avanzó de ronda).

                    3. **Parte médico y bajas:**
                       Un breve resumen en un solo texto indicando si el equipo durante esos seis enfrentamientos ha tenido bajas de jugadores importantes (por lesión, expulsión o decisión técnica), y especificando si para el próximo partido llega con bajas o con jugadores importantes recuperados.

                    Sé directo, profesional y estructurado. No inventes datos irreales, utiliza la información más reciente de la temporada actual.
                    """
                    
                    respuesta_ia = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt_analisis
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-card'>{respuesta_ia.text}</div>", unsafe_allow_html=True)
                    
                    exito = False
                    
                    # 1. Intentos automáticos con el modelo estándar gratuito
                    for intento in range(3):
                        try:
                            respuesta_ia = client.models.generate_content(
                                model="gemini-2.0-flash",
                                contents=prompt_analisis
                            )
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown(f"<div class='metric-card'>{respuesta_ia.text}</div>", unsafe_allow_html=True)
                            exito = True
                            break
                        except Exception:
                            time.sleep(2)  # Espera 2 segundos antes de reintentar
                    
                    # 2. Respaldo automático gratuito si el servidor principal se satura
                    if not exito:
                        try:
                            respuesta_ia = client.models.generate_content(
                                model="gemini-2.5-pro",
                                contents=prompt_analisis
                            )
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown(f"<div class='metric-card'>{respuesta_ia.text}</div>", unsafe_allow_html=True)
                        except Exception as e:
                            st.error("Los servidores de Google están experimentando un pico de tráfico. Por favor presiona 'Buscar Equipo' nuevamente en un par de segundos.")
    # ==========================================
    # VISTA PRINCIPAL: GESTOR DE APUESTAS Y CARGA (INTACTA)
    # ==========================================
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Sube la imagen de tu apuesta aqui")
        
        # Mostrar las apuestas subidas de forma numerada
        if st.session_state.lista_apuestas:
            for idx, apuesta_img in enumerate(st.session_state.lista_apuestas, 1):
                st.success(f"Apuesta {idx} cargada correctamente.")
                st.image(apuesta_img, caption=f"Apuesta {idx}", width=400)

        # Validar el límite de máximo 10 apuestas
        if len(st.session_state.lista_apuestas) < 10:
            imagen_apuesta = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key=f"uploader_{len(st.session_state.lista_apuestas)}")
            
            if imagen_apuesta is not None:
                if imagen_apuesta not in st.session_state.lista_apuestas:
                    st.session_state.lista_apuestas.append(imagen_apuesta)
                    st.rerun()
        else:
            st.warning("Has alcanzado el límite máximo permitido.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #00B4D8; font-weight: 500;'>Aviso: Máximo 10 apuestas a la vez</p>", unsafe_allow_html=True)
        
        if st.button("+Apuestas"):
            if len(st.session_state.lista_apuestas) < 10:
                st.info("Listo para adjuntar la siguiente apuesta.")
            else:
                st.warning("Ya tienes el límite máximo de 10 apuestas activas.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #00B4D8; font-size: 0.9rem;'>FutAnalytix © 2026 - Todos los derechos reservados</p>", unsafe_allow_html=True)
