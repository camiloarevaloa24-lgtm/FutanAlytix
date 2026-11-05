import streamlit as st
from google import genai

# Configuración inicial de la página
st.set_page_config(page_title="FutAnalytix", page_icon="⚽", layout="wide")

# Inicialización segura del cliente de Gemini usando Streamlit Secrets
client = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    pass

# Título y diseño visual de la sección
st.markdown("## Consultar Últimos Enfrentamientos y Análisis de Equipo")
st.markdown("Ingresa el nombre del equipo de fútbol para generar el informe completo con los últimos 6 partidos oficiales, plantilla, estadísticas y análisis inteligente.")

# Campo de entrada para el equipo
equipo_input = st.text_input("Nombre del equipo", placeholder="Ej: Real Madrid, Liverpool...")

# Botones de acción organizados
col1, col2 = st.columns(2)
with col1:
    btn_buscar = st.button("Buscar Equipo")
with col2:
    btn_regresar = st.button("Regresar al Gestor de Apuestas")

# Lógica del botón de búsqueda con el Prompt Maestro estructurado
if btn_buscar:
    if not client:
        st.error("⚠️ Configura la `GEMINI_API_KEY` en los Secrets de tu aplicación de Streamlit.")
    elif not equipo_input.strip():
        st.warning("Por favor ingresa un nombre de equipo válido.")
    else:
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

        try:
            with st.spinner(f"Consultando últimos datos y estadísticas de {equipo_input}..."):
                respuesta_ia = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt_analisis
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-card'>{respuesta_ia.text}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"No se pudo completar el análisis en este momento. Detalle técnico: {e}")
