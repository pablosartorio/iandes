#!/usr/bin/env python3
"""
preparaaudios.py – convierte y organiza tus crudos en 01-inputs/
"""

import os
import subprocess
from pathlib import Path

def preparaaudios(input_dir: str, audio_dir: str):
    """
    Convierte todos los archivos de video/audio en input_dir a WAV estandarizados
    y los almacena en audio_dir.

    Args:
        input_dir (str): Directorio con archivos originales (video/audio).
        audio_dir (str): Directorio de salida donde guardar los .wav.
    """
    # Crear directorio de salida si no existe
    os.makedirs(audio_dir, exist_ok=True)

    # Extensiones soportadas para conversión
    extensiones = [".mp4", ".mov", ".mkv", ".ogg", ".mp3", ".wav"]

    # Recorrer todos los archivos en input_dir
    for root, _, files in os.walk(input_dir):
        for nombre in files:
            ext = Path(nombre).suffix.lower()
            if ext in extensiones:
                origen = Path(root) / nombre
                destino = Path(audio_dir) / (Path(nombre).stem + ".wav")

                # Comando ffmpeg para convertir a WAV mono 16kHz
                cmd = [
                    "ffmpeg", "-y",
                    "-i", str(origen),
                    "-ac", "1",       # mono
                    "-ar", "16000",   # 16 kHz
                    str(destino)
                ]
                print(f"Convirtiendo {origen} → {destino}")
                subprocess.run(cmd, check=True)

    # TODO: Detectar y concatenar secuencias con prefijos/timestamps
    #       Puedes usar ffmpeg concat demuxer si los archivos deben unirse.

