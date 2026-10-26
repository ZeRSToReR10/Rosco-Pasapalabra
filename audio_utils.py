import streamlit as st
import base64
import os
from config import AUDIO_FILES

@st.cache_data
def get_audio_base64(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                data = f.read()
            return f"data:audio/mpeg;base64,{base64.b64encode(data).decode()}"
        except Exception:
            return ""
    return ""

def cargar_todos_los_audios():
    audios = {}
    faltantes = []
    for clave, nombre_archivo in AUDIO_FILES.items():
        b64 = get_audio_base64(nombre_archivo)
        audios[clave] = b64
        if not b64:
            faltantes.append(nombre_archivo)
    return audios, faltantes