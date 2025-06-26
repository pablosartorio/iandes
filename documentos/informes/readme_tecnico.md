## Requisitos previos
- Python 3.10 o superior
- `ffmpeg` disponible en el sistema (para la conversión de audio)
- Clave de API de Google (`GOOGLE_API_KEY`) si se utilizará Gemini
- Dentro del server LLM hace falta huggingface-cli login

Instale las dependencias de Python con:

```bash
python -m pip install -r requirements.txt
```
## Configuración
Toda la información de rutas, modelos y prompts se centraliza en
`config.yaml`. Los campos principales son:

Ajustar estos valores según necesidades antes de ejecutar el flujo.

Todas las configuraciones toqueteables deberían estar acá.

## Ejecución rápida
Con la configuración por defecto puede lanzar todo el pipeline ejecutando:

`python main.py`, que orquesta las etapas:
1. **Preparación de audios** (`utilitarios.preparaaudios`)
2. **Transcripción** (`src.ingest.transcribe`)
3. **Generación de resúmenes** (`src.process.resumen`)
4. **Llenado de plantillas** (`src.deliver.llenado`)

Los resultados finales se almacenan en el directorio definido en
`paths.outputs` que por ahora es 05-outputs

## Estructura de directorios

- `01-inputs/` ‒ datos crudos de audio/video
- `02-transcripciones/` ‒ archivos generados por Whisper
- `03-metadata/` ‒ resúmenes y metadatos
- `04-templates/` ‒ plantillas markdown y estrategias
- `05-outputs/` ‒ documentos finales generados
