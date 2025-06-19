#!/usr/bin/env python3
"""
main.py - Pipeline principal para análisis de entrevistas y discursos
Este script orquesta todo el flujo: preparación de audios, transcripción, generación de metadata y llenado de plantillas.
"""

import os
import yaml
import utilitarios
from src import ingest, process #, deliver


def main():
    # 1. Cargar configuración desde config.yaml
    config = load_config("config.yaml")

#    # 2. Preparar audios: convierte y organiza archivos de entrada
#    #    - input_dir: directorio con crudos (videos/audios originales)
#    #    - audio_dir: donde se guardan los WAV/MP3 estandarizados
#    utilitarios.preparaaudios(
#        input_dir=config["paths"]["raw_inputs"],
#        audio_dir=config["paths"]["audio"]
#    )
#
#    # 3. Transcribir audios con Whisper
#    #    - audio_dir: entrada
#    #    - output_dir: dónde guardar transcripciones (.json, .txt, .srt)
#    #    - model: nombre o ruta del modelo Whisper a usar
#    ingest.transcribe(
#        audio_dir=config["paths"]["audio"],
#        output_dir=config["paths"]["transcriptions"],
#        model=config["models"]["whisper"]
#    )
#
#    # 4. Procesar transcripciones: generar resúmenes, índices, análisis
#    #    - transcribe_dir: donde buscar archivos transcritos
#    #    - metadata_dir: destino para resúmenes y metadata
#    #    - model: modelo LLM para resumen
#    #    - prompt: prompt base para el LLM
    
    engine = config.get("processing", {}).get("engine", "config").lower()
    # Mapeo de engine → clave del modelo en config['models']
    key_map = {"config": "hf_textgen", "ollama": "ollama", "gemini": "gemini"}
    try:
        model_key = key_map[engine]
    except KeyError:
        raise ValueError(f"Engine desconocido: {engine}")
    model = config["models"][model_key]
    
    process.resumen(
        transcribe_dir=config["paths"]["transcriptions"],
        metadata_dir=config["paths"]["metadata"],
        model=config["models"]["engine"],
        prompt=config["prompts"]["summary"],
    )


    # 5. Llenar plantillas con la metadata generada
    #    - metadata_dir: fuente de datos
    #    - template_dir: directorio de plantillas (.md, .xlsx, etc.)
    #    - output_dir: dónde guardar los documentos finales
    #    - template_name: nombre de la plantilla a usar
#    deliver.llenado(
#        metadata_dir=config["paths"]["metadata"],
#        template_dir=config["paths"]["templates"],
#        output_dir=config["paths"]["outputs"],
#        template_name=config["templates"]["default"]
#    )

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

#import utilitarios
#import ingest
#import process 
#import deliver
## el módulo (módulo) llm tiene las opciones de local o api
#
#utilitarios.preparaaudios
#(ésta función debería recorrer el directorio 01-inputs y crear un subdirectorio 01-inpts/audios con todo lo que encuentre ahí. Videos, audios en formatos que no sirven, etc. Pasar todo a audio.wav o audio.mp3 lo que convenga. No está resuelto lo de los audios secuenciales, pensar esa posibilidad. Una especie de if el audio termina con fecha y el minuto de finalización de uno es pegado al inicio de otro unirlos)
#
#ingest.transcribe
#funcion que lee todo lo que hay en el directorio 01-inputs/audio y genera un directorio por cada audio? o una serie de archivos con un nombre único e identificable dentro de 02-transcripciones/. Definir 2 cosas: el nombre y si va con subdirectorio, porque va a generar 3 archivos por cada audio. O un solo archivo de lo mas completo.
#Opción 1) si el audio es charladepepe-fecha.wav genero un archivo charladepep-fechaaudio-fechatranscripción-conquetranscribi.json.
#Opción 2) mismo audio. Directorio 02-transcripciones/charladepepe-fecha/ y ahí adentro meto un .json, .txt, .srt.
#
#process.resumen(opción 1, opción2, parametro1, parametro2, prompt)
#recorre todo el directorio 02-transcripciones/ o solo una parte y genera lo que tenga que generar (opciones) con los parámetros que tenga que generar (parametros).
#prompt= "eres un fantástico y vas a hacer algo normal"
#parametro1= la temperatura por ejemplo
#parametro2= el beam search que todavía no se que es
#opcion1= resumen largo, corto, indexado, etc
#opcion2= formato de salida o algo así
#
#deliver.llenado(input1, input2, template)
#toma un template a elegir de 04-templates y lo llena usando info de input1 e input2
#almacena en 05-output
