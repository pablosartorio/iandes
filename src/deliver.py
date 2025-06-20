#!/usr/bin/env python3
"""
deliver.py - Módulo para el llenado de plantillas con metadata usando Google Gemini
Este script toma los archivos JSON de metadata generados en la etapa de procesamiento,
los carga en un contexto y completa una plantilla markdown mediante una llamada a Gemini.
"""

import os
import json
import argparse
from google import genai

# Configura tu API key de Google Gemini a través de la variable de entorno GOOGLE_API_KEY
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def llenado(metadata_dir: str, template_dir: str, output_dir: str, template_name: str, model: str = None):
    """
    Carga metadata desde metadata_dir, lee la plantilla desde template_dir,
    llama a Gemini para llenar la plantilla y guarda el resultado en output_dir.
    """
    # Selección de modelo
    modelo = model or os.getenv("GEMINI_MODEL", "gemini-pro-turbo")

    # Cargar metadata JSON en un diccionario
    contexto = {}
    for fname in os.listdir(metadata_dir):
        if fname.endswith(".json"):
            key = os.path.splitext(fname)[0]
            path = os.path.join(metadata_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    contexto[key] = json.load(f)
                except json.JSONDecodeError:
                    print(f"Advertencia: no se pudo parsear {fname}, se omite.")

    # Leer plantilla
    plantilla_path = os.path.join(template_dir, template_name)
    if not os.path.exists(plantilla_path):
        raise FileNotFoundError(f"No se encontró la plantilla: {plantilla_path}")
    with open(plantilla_path, "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Construir prompts
    system_prompt = (
        "Eres un asistente que llena plantillas markdown con datos estructurados."  
    )
    user_prompt = (
        f"Tienes los siguientes datos en JSON:\n{json.dumps(contexto, ensure_ascii=False, indent=2)}"
        "\n\nUsa esta información para completar la siguiente plantilla markdown exactamente como está,"
        " manteniendo el formato y reemplazando los campos necesarios:\n" + plantilla
    )

    # Llamada al modelo: pasa la lista de strings como contenidos
    resp = client.models.generate_content(
        model=modelo,
        contents=[system_prompt, user_prompt]
    )
    completado = resp.text

    # Guardar resultado
    os.makedirs(output_dir, exist_ok=True)
    salida_path = os.path.join(output_dir, template_name)
    with open(salida_path, "w", encoding="utf-8") as f:
        f.write(completado)

    print(f"✔ Plantilla completada y guardada en: {salida_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LLena plantillas markdown con metadata usando Google Gemini."
    )
    parser.add_argument(
        "--metadata_dir", required=True,
        help="Directorio que contiene archivos JSON de metadata"
    )
    parser.add_argument(
        "--template_dir", required=True,
        help="Directorio donde están las plantillas markdown"
    )
    parser.add_argument(
        "--output_dir", required=True,
        help="Directorio donde se guardarán los archivos completados"
    )
    parser.add_argument(
        "--template_name", required=True,
        help="Nombre del archivo de plantilla (por ejemplo default.md)"
    )
    parser.add_argument(
        "--model", help="Nombre del modelo Gemini a usar (opcional)"
    )
    args = parser.parse_args()
    llenado(
        metadata_dir=args.metadata_dir,
        template_dir=args.template_dir,
        output_dir=args.output_dir,
        template_name=args.template_name,
        model=args.model
    )

