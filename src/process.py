#!/usr/bin/env python3
"""
process.py - Módulo para generar resúmenes, índices y análisis usando diferentes motores de LLM.
"""

import os
from pathlib import Path
from transformers import pipeline
import ollama
from google import genai
import requests

# URL de tu API de resúmenes remota
SUMMARIZER_URL = "http://localhost:8314/generate"
# pfs mandar ésto a config.yaml

def process_with_remote(
    text: str,
    model_id: str,
    prompt_template: str,
    max_tokens: int = 200
) -> str:
    """
    Llama al servidor remoto vía HTTP para generar el resumen.
    """
    files = {
        "doc": ("transcript.txt", text.encode("utf-8"), "text/plain")
    }
    data = {
        "model_id": model_id,
        "prompt_template": prompt_template,
        "max_new_tokens": str(max_tokens),
    }
    resp = requests.post(SUMMARIZER_URL, files=files, data=data)
    resp.raise_for_status()
    return resp.text.strip()


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

        # 1) Engine por defecto: llama al servidor remoto
        if engine.lower() == "hf_textgen":
            try:
                summary = process_with_remote(
                    text=text,
                    model_id=model,
                    prompt_template=prompt,
                    max_tokens=200
                )
            except Exception as e:
                summary = f"Error al llamar a process_with_remote: {e}"

        # 2) Ollama local usando la librería Python
        # elif engine.lower() == "ollama":
        #     try:
        #         response = ollama.generate(model=model,prompt=prompt + "\n" + text)
        #         summary = response.get("completion",response.get("choices",[{}])[0].get("message", {}).get("content", ""))
        #     except Exception as e:
        #         summary = f"Error Ollama: {e}"
        
        elif engine.lower() == "ollama":
            url = "http://localhost:11434/api/generate"
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": f"{model}:latest",
                "prompt": prompt + "\n\n" + text,
                "stream": False
            }
            r = requests.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            summary = data.get("response") or data.get("results", [{}])[0].get("completion")

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

        # Guardar resumen
        out_file.write_text(summary, encoding="utf-8")
        print(f"Resumen guardado: {out_file}")