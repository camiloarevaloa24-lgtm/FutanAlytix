import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="FutAnalytix",
    page_icon="⚽",
    layout="centered"
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
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00CC52;
        color: #FFFFFF;
    }
    
    /* Cajas de texto (Usuario y Contraseña) */
    .stTextInput>div>div>input {
        background-color: #1E3E62;
        color: #FFFFFF;
        border-radius: 6px;
        border: 1px solid #00B4D8;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal profesional y moderno (Intacto)
st.markdown("""
    <h1 style='font-family: sans-serif; font-weight: 800; font-size: 2.8rem; color: #FFFFFF; letter-spacing: -0.5px; margin-bottom: 0px;'>
        Fut<span style='color: #00B4D8;'>Analytix</span>
    </h1>
""", unsafe_allow_html=True)

# Subtítulo solicitado (Intacto)
st.markdown("<p style='font-size: 1.2rem; color: #00B4D8; margin-top: 5px; margin-bottom: 30px;'>Asistente AI para analizar fútbol en vivo</p>", unsafe_allow_html=True)

# Campos de acceso directos sin recuadro ni títulos adicionales
usuario = st.text_input("Usuario")
contrasena = st.text_input("Contraseña", type="password")

st.markdown("<br>", unsafe_allow_html=True)

# 1. Registrarse
if st.button("Registrarse"):
    if not usuario or not contrasena:
        st.warning("Por favor ingresa tu usuario y contraseña.")
    else:
        st.success("¡Registro completado con éxito!")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Olvidé mi contraseña
if st.button("Olvidé mi contraseña"):
    st.info("Instrucciones de recuperación enviadas a tu sistema registrado.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #00B4D8;'>FutAnalytix © 2026 - Todos los derechos reservados</p>", unsafe_allow_html=True)
