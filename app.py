import streamlit as st
import sqlite3

# Configuración inicial de la página (INTACTA)
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

# Estados de sesión (INTACTOS)
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

if "lista_apuestas" not in st.session_state:
    st.session_state.lista_apuestas = []

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
    with col_top2:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.session_state.lista_apuestas = []
            st.rerun()

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
    
    # Botones de acción inferiores
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("+Apuestas"):
            if len(st.session_state.lista_apuestas) < 10:
                st.info("Listo para adjuntar la siguiente apuesta.")
            else:
                st.warning("Ya tienes el límite máximo de 10 apuestas activas.")
    with col_btn2:
        if st.button("Consultar ultimos enfrentamientos del equipo"):
            st.info("Función para consultar últimos enfrentamientos activada.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #00B4D8; font-size: 0.9rem;'>FutAnalytix © 2026 - Todos los derechos reservados</p>", unsafe_allow_html=True)
