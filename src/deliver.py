#!/usr/bin/env python3
"""
deliver.py - Módulo para el llenado de plantillas con transcripción completa,
resumen y contexto usando Google Gemini.
Este script toma la transcripción completa, el resumen y un contexto estratégico,
y completa una plantilla markdown mediante una llamada a Gemini, Ollama o al servidor remoto.
"""

import os
from pathlib import Path
import argparse
from google import genai
from datetime import datetime

def llenado(
    transcribe_dir: str,
    metadata_dir: str,
    template_dir: str,
    output_dir: str,
    template_name: str,
    model: str,
    engine: str,
    strategy_name: str
):
    """
    Genera un plan de acción combinando:
      - La transcripción completa (02-transcripciones/<stem>/<stem>.txt)
      - El resumen (_resumen.txt en metadata_dir)
      - Una estrategia (archivo strategy_name en template_dir)
    y usa distintos motores para llenar la plantilla markdown (template_name) en template_dir.

    Args:
        transcribe_dir (str): Directorio con subdirectorios de transcripciones (.txt).
        metadata_dir (str): Directorio con archivos de resumen (_resumen.txt).
        template_dir (str): Directorio donde están las plantillas markdown.
        output_dir (str): Directorio donde se guardarán los planes completados.
        template_name (str): Nombre del archivo de plantilla markdown.
        model (str): Nombre del modelo a usar (depende del engine).
        engine (str): Motor a usar: 'ollama', 'gemini' o 'hf_textgen'.
        strategy_name (str): Nombre del archivo de estrategia en template_dir.
    """
    # Leer estrategia -- pfs -- renombrar estrategia a contexto o algo así
    strategy_path = Path(template_dir) / strategy_name
    if not strategy_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de estrategia: {strategy_path}")
    estrategia = strategy_path.read_text(encoding="utf-8")

    # Buscar archivo de resumen
    summary_files = list(Path(metadata_dir).glob("*_resumen.txt"))
    if not summary_files:
        raise FileNotFoundError(f"No se encontraron archivos de resumen en: {metadata_dir}")
    summary_file = summary_files[0]
    stem = summary_file.stem.replace("_resumen", "")
    resumen = summary_file.read_text(encoding="utf-8")

    # Leer transcripción completa
    full_txt_path = Path(transcribe_dir) / stem / f"{stem}.txt"
    if not full_txt_path.exists():
        raise FileNotFoundError(f"No se encontró la transcripción completa en: {full_txt_path}")
    transcripcion = full_txt_path.read_text(encoding="utf-8")

    # Leer plantilla markdown
    plantilla_path = Path(template_dir) / template_name
    if not plantilla_path.exists():
        raise FileNotFoundError(f"No se encontró la plantilla: {plantilla_path}")
    plantilla = plantilla_path.read_text(encoding="utf-8")

    # Construir prompts base
    system_prompt = "Eres un asistente que llena plantillas con datos estructurados."
    user_prompt = (
        f"Estrategia:\n{estrategia}\n\n"
        f"Transcripción:\n{transcripcion}\n\n"
        f"Resumen:\n{resumen}\n\n"
        "Usa estos datos para completar la siguiente plantilla exactamente como está, manteniendo el formato:\n"
        f"{plantilla}"
    )

    engine_key = engine.lower()
    if engine_key == "gemini":
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        resp = client.models.generate_content(
            model=model,
            contents=[system_prompt, user_prompt]
        )
        completado = resp.text

    else:
        raise ValueError(f"Engine no soportado: {engine}")

    # Guardar resultado final
    Path(output_dir).mkdir(parents=True, exist_ok=True)
#    salida_path = Path(output_dir) / template_name
    salida_path = Path(output_dir) / f"{template_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    salida_path.write_text(completado, encoding="utf-8")
    print(f"✔ Plantilla completada y guardada en: {salida_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Llena plantilla de plan de acción combinando estrategia, transcripción y resumen usando varios motores."
    )
    parser.add_argument(
        "--transcribe_dir", required=True,
        help="Directorio con subdirectorios de transcripciones (.txt)"
    )
    parser.add_argument(
        "--metadata_dir", required=True,
        help="Directorio con archivos de resumen (_resumen.txt)"
    )
    parser.add_argument(
        "--template_dir", required=True,
        help="Directorio donde están las plantillas markdown"
    )
    parser.add_argument(
        "--output_dir", required=True,
        help="Directorio donde se guardarán los planes completados"
    )
    parser.add_argument(
        "--template_name", required=True,
        help="Nombre del archivo de plantilla (por ejemplo TemplatePlanifica.md)"
    )
    parser.add_argument(
        "--strategy_name", default="EstrategiaEscuela.md",
        help="Nombre del archivo de estrategia en template_dir"
    )
    parser.add_argument(
        "--engine", default="gemini",
        help="Motor a usar: 'ollama', 'gemini' o 'hf_textgen'"
    )
    parser.add_argument(
        "--model", help="Nombre del modelo a usar (opcional)"
    )
    
    args = parser.parse_args()
    llenado(
        transcribe_dir=args.transcribe_dir,
        metadata_dir=args.metadata_dir,
        template_dir=args.template_dir,
        output_dir=args.output_dir,
        template_name=args.template_name,
        model=args.model,
        engine=args.engine,
        strategy_name=args.strategy_name
    )

