# Estructura de directorios del proyecto: Análisis de entrevistas y discursos

Este documento describe la función y el contenido esperado de cada directorio del proyecto.

## 01-inputs/
Contiene los archivos originales de entrada, típicamente en formato de audio o video (`.mp4`, `.wav`, etc). Son insumos crudos sin procesar provenientes de entrevistas o charlas.

## 02-ingest/
Scripts para la ingesta de datos. Incluye:
- `ingest.py`: ingreso inicial y preprocesamiento de archivos.
- `diarize-local.py` y `diarize-api.py`: diarización de hablantes, local o usando API.

## 03-transcribe/
Scripts para convertir el audio en texto. Se implementan diferentes estrategias y herramientas (Whisper, OpenAI, etc).
Incluye:
- `transcribe.py`: script principal con múltiples opciones.
- `export.py`: para exportar los resultados procesados.
- Subdirectorio `nlp-tests/`: pruebas y experimentación con librerías NLP como spaCy. También contiene ejemplos de transcripciones (`charla.txt`, etc.).

## 04-resumen/
Contiene scripts para realizar resúmenes e indexación.
Incluye:
- `resumen-simple.py`, `resumen-local.py`, `resumen_bruto.py`: scripts que prueban distintos enfoques de resumen.
- Subdirectorios `api-openai/` y `api-google/`: llamados específicos a APIs para generar resúmenes y consultas usando modelos externos.

## 05-outputs/
Directorio vacío reservado para almacenar salidas finales o productos intermedios generados por el pipeline, como textos resumidos, metadatos enriquecidos, etc.

## 06-informes/
Contiene reportes o análisis de calidad del proceso, como:
- `calidad-transc.md`: informe sobre la calidad de las transcripciones.

## diagramas/
Diagramas SVG que ilustran los flujos de trabajo:
- `Ingesta.svg`: describe la etapa de ingesta.
- `Diagrama.svg`: flujo general del proyecto.
- `AdvancedRAG.svg`: arquitectura extendida para recuperación aumentada.

## notas/
Notas de desarrollo y planificación:
- `notas_mayo-2025.md`: registro informal del trabajo realizado durante ese período.

## retrieval/
Directorio aún vacío. Reservado para lógica de recuperación de información y vectorización (por ejemplo, embeddings, consultas semánticas, etc.).

## small-run/
Ejemplos de ejecuciones pequeñas de prueba:
- Archivos `.json`, `.txt`, `.md` que documentan el proceso de transcripción, resumen y evaluación en casos concretos (como el archivo `lenguaje.mp4`).

## utilitarios/
Pequeños scripts de utilidad:
- `token_fit.py`, `token_number.py`: ayudan a analizar y ajustar la cantidad de tokens manejables por los modelos LLM.

## Archivos sueltos en la raíz

- `README.md`: descripción general del proyecto, motivación, objetivos, metodología y actores involucrados.
- `glosario.md`: glosario de términos clave relacionados con procesamiento de lenguaje natural y flujos de trabajo.
- `directorios.md`: versión previa o placeholder para este documento.

---

