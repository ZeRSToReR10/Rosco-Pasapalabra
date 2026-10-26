import math
import time
import streamlit as st
from config import LETRAS, ROSCO_CONFIG

def inyectar_css():
    st.markdown("""
        <style>
        div.stButton > button {
            border-radius: 30px; font-weight: 900; font-size: 22px !important;
            height: 65px; border: 2px solid transparent; box-shadow: 0 6px 10px rgba(0,0,0,0.15);
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover {
            transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.25); border: 2px solid #333;
        }
        </style>
    """, unsafe_allow_html=True)

def render_rosco(estados, indice_actual, estado_juego, juego_terminado):
    radio = ROSCO_CONFIG["radio"]
    centro = ROSCO_CONFIG["centro"]
    tamano_letra = ROSCO_CONFIG["tamano_letra"]
    mitad_letra = tamano_letra / 2
    letra_actual = LETRAS[indice_actual]
    
    html_rosco = f'<div style="position: relative; width: {centro*2}px; height: {centro*2}px; margin: auto; font-family: \'Segoe UI\', sans-serif;">'
    
    if estado_juego == 'PREPARADO':
        html_rosco += '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 60px; font-weight: 900; color: #555; text-shadow: 2px 2px 8px rgba(0,0,0,0.1); text-align: center;">¿LISTO?</div>'
    elif not juego_terminado:
        html_rosco += f'<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 200px; font-weight: 900; color: #0a2351; text-shadow: 6px 6px 15px rgba(0,0,0,0.2); opacity: 1;">{letra_actual}</div>'
    else:
        html_rosco += '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 80px; font-weight: 900; color: #1e7e34; text-shadow: 4px 4px 12px rgba(0,0,0,0.2); text-align: center;">¡FIN DEL<br>ROSCO!</div>'
    
    for i, letra in enumerate(LETRAS):
        angulo = (i / len(LETRAS)) * 2 * math.pi - (math.pi / 2)
        x = centro + radio * math.cos(angulo) - mitad_letra
        y = centro + radio * math.sin(angulo) - mitad_letra
        estado = estados[letra]
        
        if estado == 'correcta': bg, color_texto = "background: radial-gradient(circle at 30% 30%, #34d058, #155724);", "color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);"
        elif estado == 'incorrecta': bg, color_texto = "background: radial-gradient(circle at 30% 30%, #ff4757, #721c24);", "color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);"
        elif estado == 'pasapalabra': bg, color_texto = "background: radial-gradient(circle at 30% 30%, #ffd93d, #856404);", "color: black; font-weight: 900;"
        else: bg, color_texto = "background: radial-gradient(circle at 30% 30%, #2f80ed, #00224e);", "color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);"
            
        es_actual = (i == indice_actual) and not juego_terminado and estado_juego != 'PREPARADO'
        
        if es_actual:
            if estado_juego == 'PAUSA_ERROR':
                borde, escala, sombra = "4px solid #ff4757", "transform: scale(1.6);", "box-shadow: 0 0 25px 12px rgba(255, 71, 87, 0.7);"
            elif estado_juego == 'PAUSA_PASAPALABRA':
                borde, escala, sombra = "4px solid #ffd93d", "transform: scale(1.6);", "box-shadow: 0 0 25px 12px rgba(255, 217, 61, 0.7);"
            else:
                borde, escala, sombra = "4px solid white", "transform: scale(1.6);", "box-shadow: 0 0 25px 12px rgba(47, 128, 237, 0.7);"
            z_index = "z-index: 10;"
        else:
            borde, escala, z_index = "2px solid rgba(255,255,255,0.8)", "transform: scale(1);", "z-index: 1;"
            sombra = "box-shadow: 0 6px 12px rgba(0,0,0,0.4);"
            
        transicion = "transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);"
        html_rosco += f'<div style="position: absolute; left: {x}px; top: {y}px; width: {tamano_letra}px; height: {tamano_letra}px; border-radius: 50%; {bg} {color_texto} display: flex; align-items: center; justify-content: center; font-family: sans-serif; font-size: 26px; border: {borde}; {sombra} {transicion} {escala} {z_index}">{letra}</div>'
        
    html_rosco += '</div>'
    st.markdown(html_rosco, unsafe_allow_html=True)

def render_temporizador(estado_juego, tiempo_config, musica_activa, audio_fondo):
    js_musica_activa = "true" if musica_activa else "false"
    
    temporizador_html = f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
    </style>
    <div style="position: relative; background-color: #080808; padding: 20px 15px; border-radius: 25px; box-shadow: 0 15px 30px rgba(0,0,0,0.4); border: 3px solid #222; text-align: center; font-family: 'Segoe UI', sans-serif; overflow: hidden;">
        <div style="font-size: 1.4rem; color: #999; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 5px; font-weight: bold;">Tiempo Restante</div>
        <div style="font-size: 6.8rem; font-weight: 900; color: #00ffcc; text-shadow: 0 0 35px rgba(0, 255, 204, 0.8); font-family: 'Courier New', monospace; line-height: 1;" id="timer"></div>
    </div>
    
    <script>
        let pyState = "{estado_juego}";
        let timerElement = document.getElementById('timer');
        let tiempoConfig = {tiempo_config};
        let isRunning = false;
        let musicaActiva = {js_musica_activa};

        let bgSrc = "{audio_fondo}";
        if (!window.bgAudio && bgSrc) {{
            window.bgAudio = new Audio(bgSrc);
            window.bgAudio.loop = true;
            window.bgAudio.volume = 0.4;
        }}

        if (pyState === "PREPARADO") {{
            sessionStorage.setItem('rosco_time', tiempoConfig);
            sessionStorage.setItem('bg_time', '0');
            if (window.bgAudio) window.bgAudio.pause();
        }}

        let timeLeft = sessionStorage.getItem('rosco_time') !== null ? parseInt(sessionStorage.getItem('rosco_time')) : tiempoConfig;

        function updateDisplay() {{
            if (timeLeft < 0) {{
                timerElement.innerText = "∞";
                timerElement.style.color = "#00ffcc";
                timerElement.style.textShadow = "0 0 35px rgba(0, 255, 204, 0.8)";
            }} else {{
                timerElement.innerText = timeLeft;
                sessionStorage.setItem('rosco_time', timeLeft);
                if(timeLeft <= 15 && timeLeft > 0) {{ 
                    timerElement.style.color = "#ff3333"; timerElement.style.textShadow = "0 0 35px rgba(255, 51, 51, 0.8)"; 
                }} else {{ 
                    timerElement.style.color = "#00ffcc"; timerElement.style.textShadow = "0 0 35px rgba(0, 255, 204, 0.8)"; 
                }}
            }}
        }}

        if (pyState === "PREPARADO") {{
            timeLeft = tiempoConfig;
        }} else if (pyState === "JUGANDO") {{
            isRunning = true;
            if (window.bgAudio) {{
                window.bgAudio.currentTime = parseFloat(sessionStorage.getItem("bg_time") || 0);
                if (musicaActiva) {{ window.bgAudio.play().catch(e => console.log(e)); }} 
                else {{ window.bgAudio.pause(); }}
            }}
        }} else if (pyState === "PAUSA_ERROR" || pyState === "PAUSA_PASAPALABRA" || pyState === "TERMINADO") {{
            isRunning = false;
            if (window.bgAudio) window.bgAudio.pause();
        }}

        updateDisplay();

        setInterval(() => {{
            if (isRunning && timeLeft > 0) {{
                timeLeft--; updateDisplay();
                if (timeLeft === 0) {{
                    isRunning = false;
                    if (window.bgAudio) window.bgAudio.pause();
                    try {{
                        let btns = window.parent.document.querySelectorAll('button');
                        btns.forEach(btn => {{ if(btn.innerText.includes('TIEMPO AGOTADO')) btn.click(); }});
                    }} catch(e) {{}}
                }}
            }}
            if (window.bgAudio && !window.bgAudio.paused) {{
                sessionStorage.setItem("bg_time", window.bgAudio.currentTime);
            }}
        }}, 1000);
    </script>
    """
    st.iframe(temporizador_html, height=210)

def render_efecto_sonido(efecto_b64):
    if efecto_b64:
        uid = time.time()
        st.iframe(f"""
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}
        </style>
        <script>
            let audio = new Audio("{efecto_b64}");
            audio.play().catch(e => console.log("Bloqueado:", e));
        </script>
        <!-- UID: {uid} -->
        """, height=1)

def render_resumen_resultados(estados):
    correctas = sum(1 for e in estados.values() if e == 'correcta')
    incorrectas = sum(1 for e in estados.values() if e == 'incorrecta')
    
    st.markdown(f"""
    <div style='display:flex; justify-content:space-around; align-items: center; background-color: #f8f9fa; padding: 15px; border-radius: 15px; border: 2px solid #ddd; margin-bottom: 20px;'>
        <div style='text-align: center;'><div style='font-size: 36px; font-weight: 900; color: #1e7e34;'>{correctas}</div><div style='color: #444; font-size: 14px; font-weight: 900;'>ACIERTOS ✅</div></div>
        <div style='text-align: center;'><div style='font-size: 36px; font-weight: 900; color: #c82333;'>{incorrectas}</div><div style='color: #444; font-size: 14px; font-weight: 900;'>ERRORES ❌</div></div>
    </div>
    """, unsafe_allow_html=True)