if btn_buscar:
        if not client:
            st.error("⚠️ Configura la `GEMINI_API_KEY` en los Secrets de tu aplicación de Streamlit.")
        elif not equipo_input.strip():
            st.warning("Por favor ingresa un nombre de equipo válido.")
        else:
            # 1. Definición del Prompt Maestro alineado exactamente a tus 3 reglas de oro
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
                # 2. Indicador visual de carga profesional para el usuario
                with st.spinner(f"Consultando últimos datos y estadísticas de {equipo_input}..."):
                    respuesta_ia = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt_analisis
                    )
                
                # 3. Renderizado limpio dentro de tu tarjeta visual estilizada
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-card'>{respuesta_ia.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"No se pudo completar el análisis en este momento. Detalle técnico: {e}")
