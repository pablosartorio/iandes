#!/usr/bin/env python3
"""
ingest.py - Módulo para transcripción de audio a texto usando Whisper
"""

import os
import json
from pathlib import Path
import whisper


def transcribe(audio_dir: str, output_dir: str, model: str):
    """
    Transcribe todos los archivos WAV en audio_dir usando Whisper,
    y guarda los resultados en output_dir en formatos JSON, TXT y SRT.

    Args:
        audio_dir (str): Ruta al directorio con archivos .wav a transcribir.
        output_dir (str): Ruta al directorio donde se guardarán las transcripciones.
        model (str): Nombre o ruta del modelo Whisper a cargar (p.ej. "base", "small", "large").
    """
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Cargar el modelo Whisper
    print(f"Cargando modelo Whisper: {model}")
    wh_model = whisper.load_model(model)

    # Iterar sobre cada archivo WAV en el directorio de audio
    for audio_path in Path(audio_dir).glob("*.wav"):
        stem = audio_path.stem
        out_subdir = Path(output_dir) / stem
        out_subdir.mkdir(parents=True, exist_ok=True)

        print(f"Transcribiendo: {audio_path.name} → {out_subdir}")
        # Realizar la transcripción
        result = wh_model.transcribe(str(audio_path), verbose=False)

        # 1) Guardar JSON completo con timestamps y texto
        json_file = out_subdir / f"{stem}.json"
        with open(json_file, "w", encoding="utf-8") as f_json:
            json.dump(result, f_json, ensure_ascii=False, indent=2)

        # 2) Guardar sólo el texto plano
        txt_file = out_subdir / f"{stem}.txt"
        with open(txt_file, "w", encoding="utf-8") as f_txt:
            f_txt.write(result.get("text", ""))

        # 3) Guardar archivo SRT con marcas de tiempo si existen segmentos
        segments = result.get("segments", [])
        if segments:
            srt_file = out_subdir / f"{stem}.srt"
            with open(srt_file, "w", encoding="utf-8") as f_srt:
                for i, seg in enumerate(segments, start=1):
                    start_ts = format_timestamp(seg["start"])
                    end_ts = format_timestamp(seg["end"])
                    text = seg.get("text", "").strip()
                    f_srt.write(f"{i}\n{start_ts} --> {end_ts}\n{text}\n\n")


def format_timestamp(seconds: float) -> str:
    """
    Convierte un tiempo en segundos a formato SRT (HH:MM:SS,mmm).
    """
    millis = int(seconds * 1000)
    hours = millis // 3600000
    minutes = (millis % 3600000) // 60000
    secs = (millis % 60000) // 1000
    ms = millis % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"

