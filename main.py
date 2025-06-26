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

    ## -----------------------------------------------------------
    ## Éstas dos variables quedan definidas para process y deliver.
    ## Si quiero usar distintas hay que cambiar esto.
    engine = config["processing"]["engine"]            
#pfs este es el que va, modificar yaml para arreglarlo    model  = config["models"][engine]                  
    model  = config["models"]["hf_textgen"]                  
    ## ----------------------------------------------------------


    # 4. Procesar transcripciones: generar resúmenes, índices, análisis
    #    - transcribe_dir: donde buscar archivos transcritos
    #    - metadata_dir: destino para resúmenes y metadata
    #    - model: modelo LLM para resumen
    #    - prompt: prompt base para el LLM
    process.resumen(
        transcribe_dir=config["paths"]["transcriptions"],
        metadata_dir=config["paths"]["metadata"],
        model=model,
        prompt=config["prompts"]["summary"],
        engine=engine
    )

    # 5. Llenar plantillas con la metadata generada
    #    - metadata_dir: fuente de datos
    #    - template_dir: directorio de plantillas (.md, .xlsx, etc.)
    #    - output_dir: dónde guardar los documentos finales
    #    - template_name: nombre de la plantilla a usar
    deliver.llenado(
        transcribe_dir = config["paths"]["transcriptions"],
        metadata_dir   = config["paths"]["metadata"],
        template_dir   = config["paths"]["templates"],
        output_dir     = config["paths"]["outputs"],
        template_name  = config["templates"]["default"],
        model          = model,
        engine         = engine,
        strategy_name  = "EstrategiaEscuela.md"
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
