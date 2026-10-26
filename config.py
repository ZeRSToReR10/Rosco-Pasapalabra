import os

LETRAS = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

AUDIO_DIR = "audio"

AUDIO_FILES = {
    "fondo": os.path.join(AUDIO_DIR, "pasapalabra_fondo.mp3"),
    "error": os.path.join(AUDIO_DIR, "error.mp3"),
    "pasar": os.path.join(AUDIO_DIR, "pasar.mp3"),
    "correcto": os.path.join(AUDIO_DIR, "correcto.mp3"),
    "clock": os.path.join(AUDIO_DIR, "clock.mp3"),
    "listo": os.path.join(AUDIO_DIR, "listo.mp3")
}

ROSCO_CONFIG = {
    "radio": 300,
    "centro": 350,
    "tamano_letra": 56
}