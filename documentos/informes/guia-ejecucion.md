# Guía de ejecución del pipeline

Este documento explica cómo reproducir el flujo completo de **Ingest - Process - Deliver**.

## Instalación de dependencias

1. Instalar Python 3.10 o superior.
2. Ejecutar (yo lo hago dentro de un entorno conda):

```bash
python -m pip install -r requirements.txt
```
## Ejecución rápida

Con las carpetas definidas en `config.yaml` se puede ejecutar el pipeline con:

`python main.py` que orquesta la preparación de audios, la transcripción con Whisper, el resumen y el llenado de plantillas.

## Server LLM con Llama

En caso de usar la opción que le pega al server llm con llama via api (no ollama que es interno ni gemini) hay que setear el server. En este caso estamos e nabu... en ccad.unc.edu.ar.

Recordatorio para mi:

[en server]
1. conda activate rag_new
2. uvicorn server-nabu:app --host 0.0.0.0 --port 8314
[en local]
1. ssh -N -L 8314:localhost:8314 nabu
uvicorn server-nabu:app --host 0.0.0.0 --port 8314
[en local]
1. ssh -N -L 8314:localhost:8314 nabu
uvicorn server-nabu:app --host 0.0.0.0 --port 8314
[en local]
1. ssh -N -L 8314:localhost:8314 nabu
2. de ahí se puede testear con curl o ya se puede ejecutar main.py normal
