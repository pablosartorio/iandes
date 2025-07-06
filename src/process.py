#!/usr/bin/env python3
"""
process.py - Módulo para generar resúmenes, índices y análisis usando diferentes motores de LLM.
"""

import os
from pathlib import Path
from google import genai

def resumen(transcribe_dir: str, metadata_dir: str, model: str, prompt: str, engine: str):
    """
    Genera resúmenes a partir de las transcripciones en 'transcribe_dir'
    y guarda los resultados en 'metadata_dir', pero solo si aún no existen.
    """
    # Crear carpeta de salida
    os.makedirs(metadata_dir, exist_ok=True)

    # Iterar cada subdirectorio en transcribe_dir
    for subdir in Path(transcribe_dir).iterdir():
        if not subdir.is_dir():
            continue

        stem = subdir.name
        txt_file = subdir / f"{stem}.txt"
        if not txt_file.exists():
            print(f"Advertencia: no se encontró texto en {txt_file}")
            continue

        # Definir ruta de salida
        out_file = Path(metadata_dir) / f"{stem}_resumen.txt"
        # Si ya existe el resumen, lo omitimos
        if out_file.exists():
            print(f"Resumen ya existe para '{stem}', omitiendo generación.")
            continue

        text = txt_file.read_text(encoding="utf-8")
        summary = ""

        if engine.lower() == "gemini":
            client = genai.Client()
            file_resp = client.files.upload(file=str(txt_file))
            resp = client.models.generate_content(
                model=model,
                contents=[prompt, file_resp]
            )
            summary = resp.text

        else:
            summary = f"Engine no soportado: {engine}"

        # Guardar resumen
        out_file.write_text(summary, encoding="utf-8")
        print(f"Resumen guardado: {out_file}")