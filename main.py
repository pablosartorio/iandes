#!/usr/bin/env python3
"""
main.py - Pipeline principal para análisis de entrevistas y discursos
Este script orquesta todo el flujo: preparación de audios, transcripción, generación de metadata y llenado de plantillas.
"""

import os
import yaml
import utilitarios
from src import ingest, process, deliver


def main():
    # 1. Cargar configuración desde config.yaml
    config = load_config("config.yaml")

    # 2. Preparar audios: convierte y organiza archivos de entrada
    #    - input_dir: directorio con crudos (videos/audios originales)
    #    - audio_dir: donde se guardan los WAV/MP3 estandarizados
    utilitarios.preparaaudios(
        input_dir=config["paths"]["raw_inputs"],
        audio_dir=config["paths"]["audio"]
    )

    # 3. Transcribir audios con Whisper
    #    - audio_dir: entrada
    #    - output_dir: dónde guardar transcripciones (.json, .txt, .srt)
    #    - model: nombre o ruta del modelo Whisper a usar
    ingest.transcribe(
        audio_dir=config["paths"]["audio"],
        output_dir=config["paths"]["transcriptions"],
        model=config["models"]["whisper"]
    )

    # 4. Procesar transcripciones: generar resúmenes, índices, análisis
    #    - transcribe_dir: donde buscar archivos transcritos
    #    - metadata_dir: destino para resúmenes y metadata
    #    - model: modelo LLM para resumen y etc.
    #    - prompt: prompt base para el LLM
    engine_process = config["process"]["engine"]            
    model_process  = config["models"][engine_process]                  
    process.resumen(
        transcribe_dir=config["paths"]["transcriptions"],
        metadata_dir=config["paths"]["metadata"],
        model=model_process,
        prompt=config["prompts"]["resumen"],
        engine=engine_process
    )

    # 5. Llenar plantillas con la metadata generada
    #    - metadata_dir: fuente de datos
    #    - template_dir: directorio de plantillas (.md, .xlsx, etc.)
    #    - output_dir: dónde guardar los documentos finales
    #    - template_name: nombre de la plantilla a usar
    engine_deliver = config["deliver"]["engine"]            
    model_deliver  = config["models"][engine_deliver]                  
    deliver.llenado(
        transcribe_dir = config["paths"]["transcriptions"],
        metadata_dir   = config["paths"]["metadata"],
        template_dir   = config["paths"]["templates"],
        output_dir     = config["paths"]["outputs"],
        template_name  = config["templates"]["default"],
        model          = model_deliver,
        engine         = engine_deliver,
        strategy_name  = config["estrategia"]["default"] 
    )

    print("Pipeline completado exitosamente.")


def load_config(path):
    """
    Carga y valida el archivo de configuración YAML.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    main()
