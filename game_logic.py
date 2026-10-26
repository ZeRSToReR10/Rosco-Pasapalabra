import streamlit as st
from config import LETRAS

def inicializar_estado():
    if 'estados' not in st.session_state:
        st.session_state.estados = {letra: 'pendiente' for letra in LETRAS}
    if 'indice_actual' not in st.session_state:
        st.session_state.indice_actual = 0
    if 'estado_juego' not in st.session_state:
        st.session_state.estado_juego = 'PREPARADO' 
    if 'musica_activa' not in st.session_state:
        st.session_state.musica_activa = True  
    if 'play_correcto' not in st.session_state:
        st.session_state.play_correcto = False 
    if 'efecto_reproducido' not in st.session_state:
        st.session_state.efecto_reproducido = False
    if 'fin_motivo' not in st.session_state:
        st.session_state.fin_motivo = None  
    if 'tiempo_inicial_seg' not in st.session_state:
        st.session_state.tiempo_inicial_seg = 150

def es_juego_terminado():
    return all(estado in ['correcta', 'incorrecta'] for estado in st.session_state.estados.values())

def verificar_fin_juego():
    juego_terminado = es_juego_terminado()
    if juego_terminado and st.session_state.estado_juego not in ['PREPARADO', 'TERMINADO', 'PAUSA_ERROR', 'PAUSA_PASAPALABRA']:
        st.session_state.estado_juego = 'TERMINADO'
        if st.session_state.fin_motivo is None:
            st.session_state.fin_motivo = 'COMPLETO'

def avanzar_siguiente(es_pasapalabra=False):
    indice_anterior = st.session_state.indice_actual
    letra_actual = LETRAS[indice_anterior]
    
    if es_pasapalabra:
        st.session_state.estados[letra_actual] = 'pasapalabra'
        
    vuelta_reiniciada = False
    for _ in range(len(LETRAS)):
        st.session_state.indice_actual = (st.session_state.indice_actual + 1) % len(LETRAS)
        
        if not vuelta_reiniciada and st.session_state.indice_actual <= indice_anterior:
            vuelta_reiniciada = True
            for l in LETRAS:
                if st.session_state.estados[l] == 'pasapalabra':
                    st.session_state.estados[l] = 'pendiente'
                    
        nueva_letra = LETRAS[st.session_state.indice_actual]
        if st.session_state.estados[nueva_letra] not in ['correcta', 'incorrecta']:
            break

def finalizar_por_tiempo():
    for letra in LETRAS:
        if st.session_state.estados[letra] not in ['correcta', 'incorrecta']:
            st.session_state.estados[letra] = 'incorrecta'
    st.session_state.estado_juego = 'TERMINADO'
    st.session_state.fin_motivo = 'TIEMPO'

def reiniciar_juego():
    st.session_state.estados = {letra: 'pendiente' for letra in LETRAS}
    st.session_state.indice_actual = 0
    st.session_state.estado_juego = 'PREPARADO'
    st.session_state.musica_activa = True
    st.session_state.fin_motivo = None
    st.session_state.efecto_reproducido = False
    st.session_state.play_correcto = False