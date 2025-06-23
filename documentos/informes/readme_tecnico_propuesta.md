# Propuesta de README técnico

Este documento ofrece una estructura de README más detallada y orientada a la
implementación del pipeline **Ingest → Process → Deliver**. Incluye instrucciones
concretas de instalación, configuración y ejecución.

## Requisitos previos
- Python 3.10 o superior
- `ffmpeg` disponible en el sistema (para la conversión de audio)
- Clave de API de Google (`GOOGLE_API_KEY`) si se utilizará Gemini

Instale las dependencias de Python con:

```bash
python -m pip install -r requirements.txt
```

## Configuración
Toda la información de rutas, modelos y prompts se centraliza en
`config.yaml`. Los campos principales son:

```yaml
paths:
  raw_inputs: "01-inputs"           # Audios o videos originales
  audio: "01-inputs/audio"          # Salida de utilitarios.preparaaudios
  transcriptions: "02-transcripciones"  # Salida de ingest.transcribe
  metadata: "03-metadata"           # Resúmenes y metadatos de process.resumen
  templates: "04-templates"         # Plantillas usadas por deliver.llenado
  outputs: "05-outputs"             # Documentos finales
models:
  whisper: "tiny"                   # Modelo Whisper
  hf_textgen: "meta-llama/Llama-3.1-8B-Instruct"
  gemini: "gemini-2.0-flash-001"
  ollama: "ollama-llama2"
prompts:
  summary: |
    Eres un asistente experto en resumir entrevistas técnicas...
processing:
  engine: "config"                  # Motor para process.resumen
```

Ajuste estos valores según sus necesidades antes de ejecutar el flujo.

## Ejecución rápida
Con la configuración por defecto puede lanzar todo el pipeline ejecutando:

```bash
bash scripts/run_pipeline.sh
```

El script invoca `python main.py`, que orquesta las etapas:
1. **Preparación de audios** (`utilitarios.preparaaudios`)
2. **Transcripción** (`src.ingest.transcribe`)
3. **Generación de resúmenes** (`src.process.resumen`)
4. **Llenado de plantillas** (`src.deliver.llenado`)

Los resultados finales se almacenan en el directorio definido en
`paths.outputs`.

## Pruebas automáticas
El repositorio incluye pruebas básicas que validan la carga de la
configuración y la secuencia principal. Ejecútelas con:

```bash
pytest
```

## Estructura de directorios
Para una descripción completa consulte `documentos/informes/estructura-de-directorios.md`.
En resumen:

- `01-inputs/` ‒ datos crudos de audio/video
- `02-transcripciones/` ‒ archivos generados por Whisper
- `03-metadata/` ‒ resúmenes y metadatos
- `04-templates/` ‒ plantillas markdown y estrategias
- `05-outputs/` ‒ documentos finales generados

Esta propuesta de README busca facilitar la puesta en marcha del proyecto y
explicar de forma concisa cómo se relacionan los módulos principales.
