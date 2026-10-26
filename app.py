import streamlit as st
from config import LETRAS
from audio_utils import cargar_todos_los_audios
from game_logic import (
    inicializar_estado,
    verificar_fin_juego,
    es_juego_terminado,
    avanzar_siguiente,
    finalizar_por_tiempo,
    reiniciar_juego
)
from ui_components import (
    inyectar_css,
    render_rosco,
    render_temporizador,
    render_efecto_sonido,
    render_resumen_resultados
)

st.set_page_config(page_title="Rosco de Pasapalabra", layout="wide", page_icon="🔵")
inyectar_css()

audios, audios_faltantes = cargar_todos_los_audios()
if audios_faltantes:
    st.warning(f"Faltan los siguientes audios en la carpeta: {', '.join(audios_faltantes)}")

inicializar_estado()
verificar_fin_juego()
juego_terminado = es_juego_terminado()

col_rosco, col_controles = st.columns([1.8, 1])

with col_rosco:
    render_rosco(
        estados=st.session_state.estados,
        indice_actual=st.session_state.indice_actual,
        estado_juego=st.session_state.estado_juego,
        juego_terminado=juego_terminado
    )

with col_controles:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.estado_juego == 'PREPARADO':
        st.markdown("<h3 style='text-align: center; color: #333;'>Configuración del Juego</h3>", unsafe_allow_html=True)
        modo_tiempo = st.radio(
            "Selecciona el modo de tiempo:",
            ["Con Límite de Tiempo", "Tiempo Infinito"],
            key="radio_modo_tiempo"
        )
        if modo_tiempo == "Con Límite de Tiempo":
            minutos_input = st.number_input(
                "Tiempo de juego (en minutos):",
                min_value=0.5,
                max_value=60.0,
                value=2.5,
                step=0.5,
                key="input_minutos_juego"
            )
            st.session_state.tiempo_inicial_seg = int(minutos_input * 60)
        else:
            st.session_state.tiempo_inicial_seg = -1

    render_temporizador(
        estado_juego=st.session_state.estado_juego,
        tiempo_config=st.session_state.tiempo_inicial_seg,
        musica_activa=st.session_state.musica_activa,
        audio_fondo=audios.get("fondo", "")
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.estado_juego == 'PREPARADO':
        if st.button("▶️ INICIAR ROSCO", use_container_width=True, type="primary"):
            st.session_state.estado_juego = 'JUGANDO'
            st.rerun()

    elif st.session_state.estado_juego == 'PAUSA_ERROR':
        st.error("❌ ¡ERROR! TIEMPO Y MÚSICA PAUSADOS")
        if st.button("▶️ REANUDAR JUEGO", use_container_width=True, type="primary"):
            st.session_state.estado_juego = 'JUGANDO'
            st.rerun()
            
    elif st.session_state.estado_juego == 'PAUSA_PASAPALABRA':
        st.warning("⏭️ ¡PASAPALABRA! TIEMPO Y MÚSICA PAUSADOS")
        if st.button("▶️ REANUDAR JUEGO", use_container_width=True, type="primary"):
            st.session_state.estado_juego = 'JUGANDO'
            st.rerun()

    elif st.session_state.estado_juego == 'TERMINADO':
        render_resumen_resultados(st.session_state.estados)
        if st.button("🔄 Reiniciar Juego", use_container_width=True):
            reiniciar_juego()
            st.rerun()

    elif st.session_state.estado_juego == 'JUGANDO':
        st.markdown("<h4 style='text-align: center; color: #555; text-transform: uppercase;'>Panel de Árbitro</h4>", unsafe_allow_html=True)
        letra_actual = LETRAS[st.session_state.indice_actual]
        
        if st.button("✅ CORRECTA", use_container_width=True):
            st.session_state.estados[letra_actual] = 'correcta'
            avanzar_siguiente(es_pasapalabra=False)
            st.session_state.play_correcto = True
            st.rerun()
            
        if st.button("❌ INCORRECTA", use_container_width=True):
            st.session_state.estados[letra_actual] = 'incorrecta'
            avanzar_siguiente(es_pasapalabra=False)
            st.session_state.estado_juego = 'PAUSA_ERROR' 
            st.rerun()
            
        if st.button("⏭️ PASAPALABRA", use_container_width=True):
            avanzar_siguiente(es_pasapalabra=True)
            st.session_state.estado_juego = 'PAUSA_PASAPALABRA'
            st.rerun()
            
        st.markdown("<hr style='margin: 15px 0; border: none; border-top: 2px dashed #ccc;'>", unsafe_allow_html=True)
        
        if st.session_state.musica_activa:
            if st.button("⏸️ PAUSAR MÚSICA", use_container_width=True):
                st.session_state.musica_activa = False
                st.rerun()
        else:
            if st.button("🔊 REANUDAR MÚSICA", use_container_width=True):
                st.session_state.musica_activa = True
                st.rerun()
                
        if st.button("⏰ TIEMPO AGOTADO", use_container_width=True):
            finalizar_por_tiempo()
            st.rerun()

# --- LÓGICA DE AUDIOS ---
efecto_a_reproducir = None

if st.session_state.estado_juego == 'TERMINADO':
    if not st.session_state.efecto_reproducido:
        if st.session_state.fin_motivo == 'TIEMPO':
            efecto_a_reproducir = audios.get("clock")
        elif st.session_state.fin_motivo == 'COMPLETO':
            efecto_a_reproducir = audios.get("listo")
        st.session_state.efecto_reproducido = True
    st.session_state.play_correcto = False

elif st.session_state.play_correcto:
    efecto_a_reproducir = audios.get("correcto")
    st.session_state.play_correcto = False

elif st.session_state.estado_juego == 'PAUSA_ERROR':
    if not st.session_state.efecto_reproducido:
        efecto_a_reproducir = audios.get("error")
        st.session_state.efecto_reproducido = True

elif st.session_state.estado_juego == 'PAUSA_PASAPALABRA':
    if not st.session_state.efecto_reproducido:
        efecto_a_reproducir = audios.get("pasar")
        st.session_state.efecto_reproducido = True

elif st.session_state.estado_juego == 'JUGANDO':
    st.session_state.efecto_reproducido = False

render_efecto_sonido(efecto_a_reproducir)