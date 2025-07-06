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
    y guarda los resultados en output_dir en formatos JSON, TXT y SRT,
    sin sobrescribir transcripciones ya existentes.
    Args:
        audio_dir (str): Ruta al directorio con archivos .wav a transcribir.
        output_dir (str): Ruta al directorio donde se guardarán las transcripciones.
        model (str): Nombre o ruta del modelo Whisper a cargar (p.ej. "base", "small", "large").
    """
    # 1. Crear directorio de salida
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 2. Cargar modelo Whisper
    print(f"Cargando modelo Whisper: {model}")
    wh_model = whisper.load_model(model)

    # 3. Procesar cada WAV
    for audio_path in Path(audio_dir).glob("*.wav"):
        stem = audio_path.stem
        out_subdir = Path(output_dir) / stem
        out_subdir.mkdir(parents=True, exist_ok=True)

        # Rutas de salida
        json_file = out_subdir / f"{stem}.json"
        txt_file  = out_subdir / f"{stem}.txt"
        srt_file  = out_subdir / f"{stem}.srt"

        # 4. Saltar si JSON ya existe
        if json_file.exists():
            print(f"Omitiendo {stem}, transcripción ya existe.")
            continue

        print(f"Transcribiendo: {audio_path.name} → {out_subdir}")
        result = wh_model.transcribe(str(audio_path), verbose=False)

        # 5. Guardar JSON
        with open(json_file, "w", encoding="utf-8") as f_json:
            json.dump(result, f_json, ensure_ascii=False, indent=2)

        # 6. Guardar TXT si no existe
        if not txt_file.exists():
            with open(txt_file, "w", encoding="utf-8") as f_txt:
                f_txt.write(result.get("text", ""))

        # 7. Guardar SRT si hay segmentos y no existe
        segments = result.get("segments", [])
        if segments and not srt_file.exists():
            with open(srt_file, "w", encoding="utf-8") as f_srt:
                for i, seg in enumerate(segments, start=1):
                    start_ts = format_timestamp(seg["start"])
                    end_ts   = format_timestamp(seg["end"])
                    text      = seg.get("text", "").strip()
                    f_srt.write(f"{i}\n{start_ts} --> {end_ts}\n{text}\n\n")

def format_timestamp(seconds: float) -> str:
    """
    Convierte un tiempo en segundos a formato SRT (HH:MM:SS,mmm).
    """
    millis  = int(seconds * 1000)
    hours   = millis // 3600000
    minutes = (millis % 3600000) // 60000
    secs    = (millis % 60000) // 1000
    ms      = millis % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"