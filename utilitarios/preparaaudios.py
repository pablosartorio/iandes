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
    sin volver a procesar los ya convertidos, y los almacena en audio_dir.

    Args:
        input_dir (str): Directorio con archivos originales (video/audio).
        audio_dir (str): Directorio de salida donde guardar los .wav.
    """
    input_dir = Path(input_dir).resolve()
    audio_dir = Path(audio_dir).resolve()
    # Crear directorio de salida si no existe
    audio_dir.mkdir(parents=True, exist_ok=True)

    # Extensiones soportadas para conversión
    extensiones = [".mp4", ".mov", ".mkv", ".ogg", ".mp3", ".wav", "webm"]

    # Recorrer todos los archivos en input_dir, excepto la carpeta de audio salida
    for root, dirs, files in os.walk(input_dir):
        root_path = Path(root).resolve()
        # Evitar re-procesar archivos que ya están en audio_dir
        if root_path == audio_dir:
            continue

        for nombre in files:
            ext = Path(nombre).suffix.lower()
            if ext in extensiones:
                origen = root_path / nombre
                destino = audio_dir / (origen.stem + ".wav")

                # Si el archivo destino ya existe, saltar
                if destino.exists():
                    print(f"Omitiendo {origen.name}, ya existe {destino.name}")
                    continue

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
    #       Usa ffmpeg concat demuxer si los archivos deben unirse.

