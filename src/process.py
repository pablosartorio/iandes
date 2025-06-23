#!/usr/bin/env python3
"""
process.py - Módulo para generar resúmenes, índices y análisis usando diferentes motores de LLM.
"""

import os
from pathlib import Path
from transformers import pipeline
import ollama
from google import genai

def resumen(transcribe_dir: str, metadata_dir: str, model: str, prompt: str, engine: str = "config"):
    """
    Genera resúmenes a partir de las transcripciones en 'transcribe_dir'
    y guarda los resultados en 'metadata_dir'.

    Args:
        transcribe_dir (str): Directorio con subdirectorios de transcripciones (con .txt).
        metadata_dir (str): Directorio donde se guardarán los archivos de resumen.
        model (str): Nombre o ruta del modelo a usar según el 'engine'.
        prompt (str): Prompt base para la generación de contenido.
        engine (str): Motor a usar: "config" (por defecto), "ollama" o "gemini".
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

        text = txt_file.read_text(encoding="utf-8")
        summary = ""

        # 1) Engine por defecto: Hugging Face text-generation pipeline
        if engine.lower() == "config":
            generator = pipeline("text-generation", model=model)
            response = generator(
                prompt + "\n" + text,
                max_new_tokens=200,
                do_sample=False
            )
            summary = response[0].get("generated_text", "")

        # 2) Ollama local usando la librería Python
        elif engine.lower() == "ollama":
            try:
                response = ollama.generate(
                    model=model,
                    prompt=prompt + "\n" + text
                )
                # La respuesta puede tener 'completion' o 'choices'
                summary = response.get("completion", 
                    response.get("choices", [{}])[0].get("message", {}).get("content", ""))
            except Exception as e:
                summary = f"Error Ollama: {str(e)}"

        # 3) Google Gemini API
        elif engine.lower() == "gemini":
            client = genai.Client()
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

