#!/usr/bin/env python3
"""
process.py - Módulo para generar resúmenes, índices y análisis usando diferentes motores de LLM.
"""

import os
from pathlib import Path


def resumen(transcribe_dir: str,
             metadata_dir: str,
             model: str,
             prompt: str,
             engine: str = "config"):
    """
    Genera resúmenes a partir de las transcripciones en 'transcribe_dir'
    y guarda los resultados en 'metadata_dir'.

    Args:
        transcribe_dir (str): Directorio con subdirectorios de transcripciones (con .txt).
        metadata_dir (str): Directorio donde se guardarán los archivos de resumen.
        model (str): Nombre o ruta del modelo a usar según el 'engine'.
                     - 'config': modelo de Hugging Face para summarization.
                     - 'ollama': modelo local en Ollama.
                     - 'gemini': modelo de Google Gemini API.
        prompt (str): Prompt base para la generación de contenido.
        engine (str): Motor a usar: "config" (por defecto), "ollama" o "gemini".
    """
    # Crear carpeta de salida si no existe
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

        text = txt_file.read_text(encoding="utf-8")
        summary = ""

        # 1) Engine por defecto: Hugging Face pipeline
        if engine.lower() == "config":
            from transformers import pipeline
            summarizer = pipeline("summarization", model=model)
            result = summarizer(
                text,
                max_length=512,
                min_length=100,
                do_sample=False
            )
            summary = result[0].get("summary_text", "")

        # 2) Ollama local (requiere CLI 'ollama')
        elif engine.lower() == "ollama":
            import subprocess
            cmd = [
                "ollama", "generate", model,
                "--prompt", prompt + "\n" + text
            ]
            try:
                proc = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                summary = proc.stdout.strip()
            except subprocess.CalledProcessError as e:
                summary = f"Error Ollama: {e.stderr.strip()}"

        # 3) Google Gemini API (requiere google-genai)
        elif engine.lower() == "gemini":
            from google import genai
            client = genai.Client()
            # Subir archivo de texto para contexto
            file_resp = client.files.upload(file=str(txt_file))
            resp = client.models.generate_content(
                model=model,
                contents=[prompt, file_resp]
            )
            summary = resp.text

        else:
            summary = f"Engine no soportado: {engine}"
            print(summary)

        # Guardar resumen
        out_file = Path(metadata_dir) / f"{stem}_summary.txt"
        out_file.write_text(summary, encoding="utf-8")
        print(f"Resumen guardado: {out_file}")
