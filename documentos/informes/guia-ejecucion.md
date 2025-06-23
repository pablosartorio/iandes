# Guía de ejecución del pipeline

Este documento explica cómo reproducir el flujo completo de **Ingest - Process - Deliver**.

## Instalación de dependencias

1. Instalar Python 3.10 o superior.
2. Ejecutar:

```bash
python -m pip install -r requirements.txt
```

## Ejecución rápida

Con las carpetas definidas en `config.yaml` se puede ejecutar el pipeline con:

```bash
bash scripts/run_pipeline.sh
```

El script invoca `python main.py` que orquesta la preparación de audios, la transcripción con Whisper, el resumen y el llenado de plantillas con Gemini.

## Pruebas automáticas

Para validar que los módulos principales se integran correctamente, ejecute:

```bash
pytest
```

Esto carga la configuración y verifica que `main.py` llama a cada etapa del proceso.
