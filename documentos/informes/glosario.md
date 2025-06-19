# Glosario de términos específicos

A continuación se presentan definiciones para los términos ya listados y se agregan otros conceptos útiles para las tres etapas principales del proyecto:  
1. **Transcribir (ingesta)**  
2. **Aumentar (resumir, generar índices, etc.)**  
3. **Reutilizar (llenado de plantillas, armado de chatbots, etc.)**

---

## chunking
**Definición:**  
Proceso de dividir un texto largo en fragmentos (“chunks”) más pequeños y manejables. Estos fragmentos suelen tener un tamaño limitado en tokens (por ejemplo, 500–1 000 tokens) para adaptarse a las restricciones de contexto de los modelos de lenguaje.  

**Uso en el proyecto:**  
- Facilita la posterior generación de embeddings y la indexación en bases de datos vectoriales.  
- Permite resumir o analizar por secciones grandes transcripciones sin exceder la ventana de contexto del modelo.

---

## embedding
**Definición:**  
Representación numérica (vectorial) de un texto o fragmento de texto en un espacio de alta dimensión. Cada palabra, frase o chunk se convierte en un vector de números flotantes que captura su significado semántico.  

**Uso en el proyecto:**  
- Indexación en una base de datos vectorial (por ejemplo, ChromaDB, Qdrant).  
- Búsqueda semántica: encontrar fragmentos similares en función de distancia euclidiana o coseno.  
- Entradas para mecanismos de “Retrieval-Augmented Generation” (RAG).

---

## tokenize
**Definición:**  
Dividir un texto en unidades básicas llamadas “tokens” (palabras, sub-palabras o caracteres). En el contexto de modelos de lenguaje como GPT o LLaMA, se utilizan tokenizadores que transforman cadenas de texto en secuencias de identificadores de token.  

**Uso en el proyecto:**  
- Saber cuántos tokens ocupa una transcripción o un prompt para respetar el límite de la ventana de contexto.  
- Preparar la entrada para modelos de lenguaje y cuantificar el costo de inferencia (por token).

---

## ventana de contexto
**Definición:**  
Cantidad máxima de tokens que un modelo de lenguaje puede procesar en una sola pasada. Por ejemplo, GPT-3 puede manejar 4 096 tokens, GPT-4 otorga hasta 8 192 o 32 768 tokens según la variante, y Llama-3 (8 B) maneja 8 K tokens.  

**Uso en el proyecto:**  
- Al fragmentar (chunking) transcripciones para el resumen o el análisis, hay que asegurarse de que cada chunk no exceda la ventana de contexto soportada por el modelo que se use.  
- Determina cuántos tokens de prompt + respuesta caben en una sola llamada al modelo.

---

## beam
**Definición:**  
Abreviatura de “beam search”, método de decodificación en modelos generativos para encontrar la secuencia de tokens más probable. Mantiene en cada paso las N hipótesis parciales más probables (donde N es el ancho del “beam”).  
- **Beam width (ancho de beam):** número de hipótesis que se expanden en paralelo.  

**Uso en el proyecto:**  
- Al generar resúmenes o textos largos, se puede ajustar el beam width para equilibrar fluidez y diversidad.  
- Un beam más ancho tiende a generar textos más coherentes, pero aumenta el costo computacional.

---

## RAG (Retrieval-Augmented Generation)
**Definición:**  
Arquitectura que combina recuperación de información (retrieval) y generación de texto (generation).  
1. **Retrieval:** a partir de una pregunta o prompt, el sistema busca documentos o fragmentos relevantes en una base de datos vectorial o textual.  
2. **Augmentation:** esos fragmentos recuperados se concatenan al prompt original como contexto adicional.  
3. **Generation:** un modelo de lenguaje genera la respuesta final tomando en cuenta el prompt y los documentos recuperados.  

**Uso en el proyecto:**  
- Útil para responder preguntas específicas sobre una transcripción larga (por ejemplo: “¿En qué minuto se habló de X?”).  
- Mejora la precisión del modelo al darle contexto concreto extraído de la base de datos de embeddings.

---

## Transcripción
**Definición:**  
Proceso de convertir audio (o video con pista de audio) en texto legible.  
1. **Transcripción automática:** uso de modelos como OpenAI Whisper, Google Speech-to-Text o sistemas open-source para generar un texto bruto (plain text).  
2. **Transcripción “verbose”:** versión que incluye metadatos (timestamps palabra por palabra, probabilidades, segmentación por altavoces, etc.).  

**Uso en el proyecto (Ingesta):**  
- Punto de partida para todo el flujo: capturar el contenido hablado.  
- La versión “verbose” permite generar índices temáticos o análisis de segmentos.

---

## Diarización
**Definición:**  
“Speaker diarization”; proceso de identificar “quién habló cuándo” en un audio con múltiples interlocutores.  
- Detecta cambios de hablante y asigna etiquetas (Speaker 1, Speaker 2, etc.) a cada segmento.  

**Uso en el proyecto (Ingesta):**  
- Con herramientas como Pyannote-audio, se segmenta la transcripción por hablante.  
- Permite fines de análisis: por ejemplo, generar resumen por interlocutor, análisis de turnos de habla, métricas de tiempo de intervención.

---

## Whisper
**Definición:**  
Modelo de OpenAI para reconocimiento automático de voz (ASR).  
- Versiones: tiny, base, small, medium, large, turbo (las últimas más grandes y costosas de GPU).  
- Ofrece transcripción en múltiples idiomas, timestamping y segmentación.

**Uso en el proyecto (Ingesta):**  
- Generar las transcripciones iniciales de entrevistas y charlas.  
- Se puede ejecutar localmente (instalando `whisper` con PyTorch) o vía API.

---

## WER (Word Error Rate)
**Definición:**  
Métrica estándar en ASR para medir la calidad de una transcripción.  
- Fórmula básica:  
  \[
    \text{WER} = \frac{S + D + I}{N}
  \]  
  donde S = sustituciones, D = eliminaciones (deletions), I = inserciones (insertions) comparadas con la “ground truth” y N = número total de palabras en la referencia.  

**Uso en el proyecto (Ingesta / Calidad):**  
- Evaluar precisión de la transcripción automática frente a una transcripción humana.  
- Diagnosticar segmentos problemáticos para corrección manual o ajustes de modelo.

---

## Resumen extractivo
**Definición:**  
Técnica de resumen que selecciona frases, oraciones o párrafos clave del texto original sin generar texto nuevo.  
- Métodos: scores de importancia (TF-IDF, TextRank, etc.) que puntúan las oraciones y eligen las más relevantes.  

**Uso en el proyecto (Aumentar):**  
- Resumir transcripciones largas eligiendo fragmentos literales que cubran el contenido principal.  
- Suele ser más rápido y menos costoso computacionalmente que generar un resumen abstractivo.

---

## Resumen abstractivo
**Definición:**  
Generación de un resumen “nuevo” que reescribe el contenido original con palabras propias, condensando la idea general en frases sintéticas.  
- Requiere un modelo generativo (LLM).  

**Uso en el proyecto (Aumentar):**  
- Ofrecer resúmenes más naturales y cohesivos (por ejemplo, “Genera un resumen de 200 palabras sobre los tópicos discutidos en la charla”).  
- Más flexible para dar distintos niveles de detalle según el prompt (breve, medio, detallado).

---

## Índice temático
**Definición:**  
Lista organizada de los temas o secciones principales que aparecen en un texto (o transcripción), generalmente con timestamps o referencias de página.  
- Permite navegar rápidamente al punto donde se discute cada tema.  

**Uso en el proyecto (Aumentar):**  
- Junto con el resumen, facilita la localización de contenidos relevantes.  
- Por ejemplo:  
  1. “Introducción al proyecto” (00:00–02:15)  
  2. “Metodología propuesta” (02:16–10:30)  
  3. “Casos de uso en la empresa” (10:31–20:00)  
  4. …

---

## NER (Named Entity Recognition) o Reconocimiento de Entidades Nombradas
**Definición:**  
Tarea de procesamiento de lenguaje natural (NLP) que identifica y clasifica menciones de entidades (personas, organizaciones, lugares, fechas, etc.) en el texto.  

**Uso en el proyecto (Aumentar):**  
- Extraer metadatos: nombres de participantes, empresas, tecnologías mencionadas.  
- Apoya la elaboración de resúmenes orientados a información crítica (por ejemplo, “Nombrar todos los expertos mencionados”).

---

## Análisis de sentimiento (o análisis emocional)
**Definición:**  
Proceso de clasificar segmentos de texto según su carga emocional (positivo, negativo, neutral) o identificar emociones específicas (alegría, tristeza, enfado, etc.).  

**Uso en el proyecto (Aumentar):**  
- Evaluar tono de ciertas declaraciones en entrevistas (por ejemplo, detectar preocupaciones o entusiasmo).  
- Complementa resúmenes temáticos con perspectiva emocional.

---

## Base de datos vectorial
**Definición:**  
Almacén especializado en guardar vectores de embedding y permitir búsquedas de similitud (nearest neighbors) de forma eficiente.  
- Ejemplos: ChromaDB, Qdrant, Milvus, Weaviate.  

**Uso en el proyecto (Reutilizar / Aumentar):**  
- Cuando se requiere recuperar fragmentos de texto relacionados semánticamente con una consulta.  
- Pilar central para arquitecturas RAG: se indexan los embeddings de todos los chunks y se consultan cuando el usuario hace preguntas.

---

## Base de datos estructurada (SQL / NoSQL)
**Definición:**  
Almacén de datos tradicional para información tabular (SQL: PostgreSQL, MySQL) o documentos/arreglos (NoSQL: MongoDB).  
- Puede complementarse con extensiones vectoriales (p. ej., pgvector en PostgreSQL).  

**Uso en el proyecto (Reutilizar):**  
- Guardar metadatos de cada entrevista: fecha, entrevistador, entrevistado, títulos, categorías.  
- Asociar las transcripciones (plain text) o enlaces a los embeddings indexados en la base de datos vectorial.

---

## Prompt (o indicación)
**Definición:**  
Texto que se envía a un modelo de lenguaje para guiar la generación de respuestas.  
- Incluye instrucciones (“Eres un asistente que resume charlas…”) y contexto adicional (chunks relevantes, metadatos).  

**Uso en el proyecto (Aumentar / Reutilizar):**  
- Construir prompts que pida al LLM generar resúmenes breves, índices temáticos, plantillas pre-llenadas.  
- Práctica de “prompt engineering” para obtener respuestas más precisas y coherentes.

---

## LLM (Large Language Model) / Modelo de Lenguaje
**Definición:**  
Modelos entrenados con decenas de miles de millones (o más) de parámetros para procesar y generar lenguaje natural. Ejemplos: GPT-3, GPT-4, Llama-3, Mistral 7B, Geminis, etc.  

**Uso en el proyecto (Aumentar / Reutilizar):**  
- Generar resúmenes abstractivos, índices, preguntas para entrevistas, plantillas llenas.  
- Crear chatbots capaces de responder basados en la información previamente indexada (RAG).

---

## Beam Search
> (Ver “beam”)

---

## Prompt Engineering
**Definición:**  
Conjunto de técnicas para diseñar y optimizar los prompts que se envían a un modelo de lenguaje, buscando respuestas más precisas, coherentes y útiles.  

**Uso en el proyecto (Aumentar / Reutilizar):**  
- Definir la mejor estructura de prompt para generar un plan de acción basado en datos de la transcripción.  
- Ajustar parámetros como temperatura, top-k, top-p y beam width para equilibrar creatividad y fidelidad.

---

## Chatbot / Agente Conversacional
**Definición:**  
Sistema que simula una conversación con un usuario, generalmente impulsado por un LLM o flujo de diálogo predefinido.  
- Puede usar RAG para acceder a información específica de la transcripción y responder consultas.  

**Uso en el proyecto (Reutilizar):**  
- Permitir que un experto o colaborador haga preguntas directas sobre el contenido de las entrevistas y reciba respuestas contextuales.  
- Automatizar la generación de respuestas frecuentes (FAQs) basadas en la base de conocimiento creada.

---

## Plantilla
**Definición:**  
Documento estructurado con campos o secciones predefinidas que deben completarse con información específica.  
- En este flujo, se utiliza una plantilla genérica (ej. planilla de transferencia de conocimiento) que el sistema pre-llena con datos extraídos de transcripción, NER y resumen.  

**Uso en el proyecto (Reutilizar):**  
- Facilitar la creación de documentos estandarizados: plan de acción, perfil de conocimientos, etc.  
- Agilizar la labor del experto al tener prellenados los campos básicos y solo requerir su revisión o ajuste final.

---

## Conversión TTS (Text-to-Speech)
**Definición:**  
Proceso inverso a la transcripción: convertir texto en voz sintetizada.  
- Opcional en este proyecto, pero puede servir para generar resúmenes hablados o notificaciones de audio.  

**Uso en el proyecto (Reutilizar):**  
- Generar versiones habladas de los resúmenes para entregas en formato audio.  
- Permitir revisiones auditivas rápidas sin leer texto.

---

## OCR (Optical Character Recognition)
**Definición:**  
Reconocimiento óptico de caracteres en imágenes o PDF, convierte contenido impreso o escrito a mano en texto plano.  

**Uso en el proyecto (Ingesta / Aumentar):**  
- Si parte de la documentación relevante está en PDF escaneado, se puede aplicar OCR para incorporar el texto a la base de conocimientos.  
- Completa la fase de ingesta de fuentes “no estructuradas”.

---

## Data Augmentation (aumento de datos)
**Definición:**  
Técnicas para ampliar o diversificar el conjunto de datos original, por ejemplo, traduciendo, parafraseando o generando resúmenes alternativos.  

**Uso en el proyecto (Aumentar):**  
- Generar distintos niveles de resumen: breve, intermedio, detallado.  
- Crear consultas variadas para RAG y enriquecer la base de embeddings.

---

## OCR (repetido por si acaso)
> (Ya definido arriba)

---

## Whisper
> (Ver “Whisper”)

---

## Pyannote-audio
**Definición:**  
Conjunto de herramientas en Python basado en PyTorch para procesamiento de audio: segmentos de voz, diarización y reconocimiento de hablantes.  

**Uso en el proyecto (Ingesta):**  
- Detectar y segmentar diferentes hablantes en una grabación multipersona.  
- Enriquecer la transcripción con etiquetas de `speaker_1`, `speaker_2`, etc., para posteriores análisis.

---

## Chunk
> (Ver “chunking”)

---

## Token
> (Ver “tokenize”)

---

## GPT
**Definición:**  
Familia de modelos de lenguaje de OpenAI basados en la arquitectura Transformer: GPT-3, GPT-4, GPT-4o, etc.  
- Se usan para tareas de generación de texto, comprensión de lenguaje, traducción y más.  

**Uso en el proyecto (Aumentar / Reutilizar):**  
- Generar resúmenes abstractivos de alta calidad.  
- Formular preguntas de seguimiento para entrevistas.

---

## Llama-3 / Mistral-7B / Gemini-2.0
**Definición:**  
Ejemplos de LLMs desarrollados por Meta (Llama-3), Mistral AI (Mistral-7B) y Google DeepMind (Gemini).  
- Cada uno tiene características propias: tamaño de ventana de contexto, desempeño en español, costo de inferencia, etc.  

**Uso en el proyecto (Aumentar / Reutilizar):**  
- Seleccionar el modelo que mejor balancee calidad de resumen y costo computacional.  
- Experimentar con distintos LLMs para comparar calidad de síntesis y pertinencia.

---

## WER
> (Ver “WER”)

---

## ROUGE / BLEU
**Definición:**  
- **ROUGE (Recall-Oriented Understudy for Gisting Evaluation):** métricas basadas en n-gramas para evaluar la calidad de un resumen comparándolo con uno de referencia (e.g., ROUGE-1, ROUGE-2, ROUGE-L).  
- **BLEU (Bilingual Evaluation Understudy):** métrica inicialmente diseñada para evaluación de traducciones automáticas, basada en precisión de n-gramas.  

**Uso en el proyecto (Aumentar / Calidad):**  
- Evaluar automáticamente la calidad de los resúmenes generados por distintos modelos.  
- Comparar resúmenes extractivos vs. abstractivos contra una referencia humana.

---

## Api
**Definición:**  
Conjunto de funciones y protocolos que permite interactuar con un servicio o librería.  
- Ejemplo: API de OpenAI para transcripción (Whisper API), generación de texto (Chat Completions), etc.  

**Uso en el proyecto (Ingesta / Aumentar):**  
- Acceder a modelos en la nube sin instalar localmente.  
- Simplificar el pipeline delegando inferencia a la infraestructura del proveedor.

---

## Base de conocimiento (Knowledge Base)
**Definición:**  
Conjunto organizado de información (resúmenes, transcripciones, entidades, conexiones semánticas) que puede ser consultado.  
- Se construye a partir de embeddings indexados, metadatos y texto estructurado.  

**Uso en el proyecto (Reutilizar):**  
- Como punto de partida para RAG y chatbots; responder preguntas basadas en las entrevistas previas.  
- Plataforma para generar planes de acción personalizados usando datos ya almacenados.

---

## MLOps / Stack MLOps
**Definición:**  
Conjunto de prácticas, herramientas y procesos para operacionalizar proyectos de machine learning: desde el desarrollo hasta la producción, incluyendo versionado de modelos, pipelines y monitoreo.  

**Uso en el proyecto (General):**  
- Definir entornos reproducibles (conda, Docker) para que la ingesta, el preprocesamiento y la inferencia de LLM sean consistentes.  
- Automatizar la re-creación de embeddings cuando se agreguen nuevas entrevistas.

---

## KPI (Key Performance Indicator)
**Definición:**  
Indicador clave de desempeño que mide qué tan exitoso es un proceso o proyecto respecto a objetivos establecidos.  

**Uso en el proyecto (Gestión):**  
- Medir métricas como: tiempo de procesamiento por hora de audio, precisión de transcripción (WER), satisfacción de expertos con los resúmenes generados, reducción de tiempo de reunión gracias al plan de acción.  
- Ayuda a iterar y mejorar continuamente el flujo de trabajo.

---

## RACI (Responsible, Accountable, Consulted, Informed)
**Definición:**  
Matriz de asignación de roles y responsabilidades en proyectos.  
- **Responsible:** quién ejecuta la tarea.  
- **Accountable:** quién es el dueño final del entregable.  
- **Consulted:** quienes contribuyen con información relevante.  
- **Informed:** quienes deben ser informados de los avances.  

**Uso en el proyecto (Gestión):**  
- Aclarar quién hace qué en cada etapa: ingesta, preprocesamiento, generación de resúmenes, validación con el experto, armado de plantillas, revisión del plan final, etc.

---

## QA (Quality Assurance) / Control de calidad
**Definición:**  
Proceso de verificar que la salida (transcripción, resúmenes, plantillas) cumpla con estándares mínimos de calidad antes de entregarla al CTO o al experto.  

**Uso en el proyecto (Control de Calidad):**  
- Revisar manualmente muestras de transcripción para verificar WER aceptable.  
- Validar que los resúmenes cubran todos los temas críticos sin omisiones.

---

## JSON / JSONL
**Definición:**  
- **JSON (JavaScript Object Notation):** formato de texto ligero para intercambio de datos estructurados.  
- **JSONL (JSON Lines):** variante donde cada línea es un objeto JSON independiente, útil para procesar grandes volúmenes secuenciales.  

**Uso en el proyecto (Ingesta / Almacenamiento):**  
- La transcripción “verbose” de Whisper suele entregarse en JSON.  
- Guardar los fragmentos con metadatos, entidades y embeddings en JSON o JSONL facilita procesamiento por lotes.

---

## SRT (SubRip Subtitle)
**Definición:**  
Formato de archivo para subtítulos que asocia segmentos de texto con marcas de tiempo. Cada bloque incluye: índice, tiempo de inicio, tiempo de fin y texto.  

**Uso en el proyecto (Ingesta / Verificación):**  
- Permite reproducir el audio/video con subtítulos sincronizados para verificar manualmente la precisión de la transcripción.  
- Puede servir como recurso adicional para la revisión de contenidos y generación de índices temáticos.

---

## PT-PT / PT-ES / EN-ES (idiomas y dialectos)
**Definición:**  
Códigos de idioma y regionalización. Por ejemplo: `es-AR` (español de Argentina), `en-US` (inglés de EE. UU.), `pt-BR` (portugués de Brasil), etc.  

**Uso en el proyecto (Ingesta / Configuración):**  
- Asegurarse de que al invocar la API de transcripción (Whisper, Google), se especifique el idioma correcto para mejorar la precisión.  
- Configurar modelos de tokenización apropiados para cada dialecto.

---

## PyTorch / TensorFlow
**Definición:**  
Frameworks de deep learning. PyTorch (preferido en Hugging Face y Whisper) y TensorFlow (más común en entornos de producción de Google).  

**Uso en el proyecto (Infraestructura):**  
- Cargar modelos de transcripción (Whisper) y LLMs (Mistral, Llama) en PyTorch para inferencia local.  
- Facilita la personalización de pipelines en Python usando `transformers`, `torchaudio`, `pyannote`, etc.

---

# Términos adicionales por etapa

### 1. Transcribir (Ingesta)

- **WAV / MP3 / MP4 / FLAC**  
  **Definición:** formatos de audio/video de entrada.  
  **Uso:** decidir cuál es el formato óptimo para la transcripción (FLAC o WAV suele dar mejor calidad).

- **Bitrate / Sample Rate**  
  **Definición:** calidad de grabación en términos de kilobits por segundo (kbps) o frecuencia de muestreo en Hz.  
  **Uso:** grabaciones con mayor sample rate (≥ 16 kHz) mejoran la precisión de ASR.

- **Silence Removal (Eliminación de silencios)**  
  **Definición:** preprocesamiento que elimina segmentos de silencio prolongados para acelerar transcripción.  
  **Uso:** reduce el tiempo de inferencia y evita tokens innecesarios.

- **VAD (Voice Activity Detection)**  
  **Definición:** detección automática de segmentos donde hay voz activa vs. silencio.  
  **Uso:** delimitar mejor las regiones que deben transcribirse, evitar interpretaciones erróneas en silencios.

- **Segmentación por Alto Nivel**  
  **Definición:** división del audio en bloques más grandes (capítulos, secciones) antes de la diarización.  
  **Uso:** agilizar procesamiento paralelo en múltiples nodos o GPUs.

- **Timestamping**  
  **Definición:** etiquetar cada palabra o cada bloque de texto con marcas de tiempo precisas.  
  **Uso:** indispensable para generar índices temáticos y subtítulos.

### 2. Aumentar (Resumir, Generar Índices, etc.)

- **TF-IDF (Term Frequency–Inverse Document Frequency)**  
  **Definición:** métrica que pondera la importancia de una palabra en un documento frente a una colección de documentos.  
  **Uso:** fundamento para métodos extractivos de resumen como TextRank.

- **TextRank / LexRank**  
  **Definición:** algoritmos basados en grafos para extraer las oraciones más relevantes.  
  **Uso:** generar un primer resumen extractivo antes de pasar a un modelo abstractivo.

- **TF-IDF Weighted Sum**  
  **Definición:** sumar vectores de embedding de cada palabra ponderados por TF-IDF para obtener un embedding de oración.  
  **Uso:** crear embeddings a nivel oración para búsquedas semánticas más precisas.

- **Fine-Tuning / Ajuste fino**  
  **Definición:** proceso de entrenar un modelo preentrenado en un conjunto de datos específico para mejorar desempeño en tareas concretas.  
  **Uso:** en proyectos más avanzados, ajustar un LLM para generar resúmenes en un estilo particular o mejorar NER especializado.

- **Sparse Retrieval (Recuperación Dispersa)**  
  **Definición:** búsqueda basada en índices invertidos y conteo de tokens (p. ej., BM25), en contraste con la recuperación densa (embeddings).  
  **Uso:** combinar retrieval disperso + denso para mejorar cobertura en RAG.

- **Evaluación Automatizada de Calidad**  
  **Definición:** uso de métricas como ROUGE, BLEU, METEOR o BERTScore para comparar resúmenes generados contra referencias humanas.  
  **Uso:** medir iterativamente la mejora al cambiar prompts o modelos.

- **NER Avanzado (SpaCy, Hugging Face Transformers)**  
  **Definición:** modelos de reconocimiento de entidades más robustos entrenados en múltiples dominios.  
  **Uso:** extraer información técnica, nombres de proyectos, siglas, fechas críticas, etc.

- **Análisis de Cohesión / Coherencia**  
  **Definición:** métricas que evalúan la estructura global del texto (por ejemplo, Coh-Metrix).  
  **Uso:** evaluar si el resumen generado mantiene consistencia lógica con el original.

### 3. Reutilizar (Llenado de Plantillas, Armado de Chatbots, etc.)

- **Plantillas Dinámicas**  
  **Definición:** documentos pre-estructurados con marcadores de posición (<nombre>, <tema_principal>, <resumen_breve>, etc.) que luego se reemplazan con contenido extraído.  
  **Uso:** elaborar informes, planillas de transferencia de conocimiento, guías de entrevista personalizadas.

- **Variables de Plantilla**  
  **Definición:** identificadores en la plantilla que se substituyen dinámicamente (`{{ENTREVISTADO}}`, `{{FECHA_ENTREVISTA}}`, `{{RESUMEN_TEMAS}}`).  
  **Uso:** garantizar consistencia y evitar errores de formato manual.

- **Chatbot con Contexto**  
  **Definición:** agente conversacional que, además de un prompt, recibe contexto relevante (embedding, transcripción, resumen) para responder preguntas.  
  **Uso:** brindar acceso interactivo al contenido de las entrevistas (ej. “¿Qué dijo el experto sobre la migración de datos?”).

- **Fine-Tuning de Chatbot**  
  **Definición:** ajustar un LLM específicamente para responder según el tono y las reglas de negocio de la empresa.  
  **Uso:** en fases avanzadas, entrenar al chat para que adopte un “tono corporativo” o use terminología interna.

- **API REST / Microservicio**  
  **Definición:** interfaz que expone endpoints (ej. `/transcribe`, `/summarize`, `/chat`) para integrar el pipeline con otras aplicaciones.  
  **Uso:** permitir que distintos equipos consuman de forma sencilla los servicios de transcripción, análisis y chat.

- **Integración con Slack / Teams / Telegram**  
  **Definición:** conectores que permiten enviar mensajes automatizados al equipo cuando hay resultados nuevos (por ej., “Se generó resumen para la entrevista de hoy”).  
  **Uso:** mantener informado al CTO o a los interesados sin necesidad de revisar manualmente la base de datos.

- **Webhook / Eventos**  
  **Definición:** mecanismo para que, una vez completada una ingesta o un resumen, se notifique automáticamente a otro servicio (ej. desencadenar envío de correo al experto).  
  **Uso:** automatizar flujos de trabajo posteriores (revisión, aprobación, implementación de plan).

- **LLM-Driven Document Filling**  
  **Definición:** uso de un LLM para interpretar una plantilla genérica y rellenarla con datos estructurados o semiestructurados.  
  **Uso:** generar planillas de transferencia de conocimiento con residuo mínimo de intervención humana.

- **Pipeline Orquestado (Airflow, Luigi, Prefect)**  
  **Definición:** sistema para definir y ejecutar tareas en un orden determinado, con dependencia de resultados y posibilidad de reintentos.  
  **Uso:** asegurar que la ingesta, el preprocesamiento, la generación de embeddings, la creación de resúmenes y la actualización de plantillas se realicen secuencialmente y con trazabilidad.

- **Validación de Usuario / Feedback Loop**  
  **Definición:** mecanismo donde el experto revisa los contenidos generados (resúmenes, plantillas) y corrige o aprueba, alimentando el sistema con datos de corrección.  
  **Uso:** mejora continua de la calidad, ajustes en prompts y posible eventual fine-tuning.

---

# Ejemplos de uso en flujo

A continuación se ejemplifica cómo encajan algunos términos en el flujo de trabajo:

1. **Ingesta (Transcribir + Diarizar)**  
   - **Audio en formato WAV** → Pyannote-audio aplica **VAD** y **diarización** → segmentos con hablante identificado.  
   - Cada segmento pasa a **Whisper** para obtener **transcripción (texto + timestamps)** (JSON “verbose”).  
   - Se calcula el **WER** comparado con una muestra humana de control (calidad).  

2. **Preprocesamiento / Chunking**  
   - El texto completo (un solo JSON o plain-text) se divide en **chunks** de 1 000 tokens.  
   - Cada chunk se **tokeniza** y se verifica que no exceda la **ventana de contexto** del LLM (p. ej. 8 K tokens).  

3. **Generación de Embeddings**  
   - Cada chunk se convierte en un **embedding** (usando un modelo de embeddings como `sentence-transformers` o `OpenAI Embedding API`).  
   - Se indexan los embeddings en una **base de datos vectorial** (ChromaDB).  

4. **Aumentar (Resumen + Índice + NER)**  
   - Se generan resúmenes con un **modelo LLM** (p. ej. Mistral-7B o GPT-4):  
     - Prompt: “Eres un asistente que genera un **resumen abstractivo** de la siguiente transcripción…”  
     - Se miden métricas automáticas como **ROUGE** contra un resumen de control.  
   - Se crea un **índice temático** extrayendo timestamps y frases clave.  
   - Se aplica **NER** para listar entidades (nombres de proyectos, personas, fechas).  

5. **Reutilizar (Plantillas + Chatbot)**  
   - Los resultados (resumen, índice, entidades) se pasan a un **llenado de plantilla**:  
     ```yaml
     entrevistado: "Nombre Apellido"
     fecha: "2025-06-01"
     resumen_breve: "..."
     temas_principales:
       - "Tema 1 (00:00–02:05)"
       - "Tema 2 (02:06–10:30)"
     entidades:
       - "Empresa X"
       - "Tecnología Y"
     plan_accion:
       - "Paso 1: …"
       - …
     ```  
   - Se crea un **chatbot** que consulta la **base de conocimiento** (RAG) para responder consultas como “¿Qué dijo el entrevistado sobre la migración a la nube?”  

---

# Términos Extra que Pueden Ser Útiles

- **Fine-Tuning** (Ver arriba: Ajuste fino de modelos).  
- **Prompt Tokens vs. Response Tokens**: distinguir los tokens que se usan en la entrada del modelo y los que genera como respuesta, para controlar costos de API.  
- **Costos de Inference**: tarifa por cada 1 000 tokens procesados; influye en la elección de modelo y frecuencia de llamadas.  
- **Context Window Sliding**: técnica para procesar secuencias más largas que la ventana de contexto real, desplazándose incrementalmente.  
- **Cache de Embeddings**: guardar en disco o base de datos los embeddings generados para no recalcularlos cada vez.  
- **ChromaDB / Qdrant / Milvus** (Ver “Base de datos vectorial”).  
- **PostgreSQL + pgvector** (Ver “Base de datos estructurada” + extensión vectorial).  
- **Kibana / Grafana**: dashboards para monitorear KPIs del pipeline (cantidad de audios procesados, latencia, errores).  
- **Docker / Docker Compose**: contenerizar cada servicio (ASR, diarización, LLM, base de datos) para facilitar despliegue y escalado.  
- **Conda / Virtualenv** (Ver entorno del usuario): administrar entornos Python reproducibles.  
- **GPU Remota (NVIDIA A30)**: hardware especializado para acelerar inferencia de modelos grandes.  
- **FP16 / BF16**: formatos de precisión de punto flotante usados en GPU para reducir uso de memoria y acelerar cómputo sin perder (mucho) en calidad.  
- **Pipeline MLOps Orquestado**: ejemplos de frameworks: Airflow, Prefect, Luigi (Ver “Pipeline Orquestado”).  
- **Data Drift**: cambio en la distribución de datos (por ejemplo, estilo de charla, jerga nueva) que puede afectar la calidad del resumen con el tiempo. Requiere monitoreo y posible reentrenamiento o ajuste fino.  
- **Sharding / Parallel Processing**: dividir la carga de trabajo (chunks, calcolo de embeddings, llamadas LLM) en múltiples procesos o máquinas.  
- **Token Truncation / Padding**: cómo manejar textos que exceden la longitud máxima o que son demasiado cortos al enviar a un modelo.

---

## Conclusión

Este glosario cubre las definiciones básicas y avanzadas necesarias para abordar el proyecto en sus tres fases:  
1. **Transcribir (ingesta)**: términos relacionados con ASR, diarización, calidad de audio.  
2. **Aumentar (resumir, generar índices, análisis semántico)**: métricas de evaluación, técnicas de resumen y recuperación de información.  
3. **Reutilizar (llenado de plantillas, chatbots, pipelines MLOps)**: conceptos de orquestación, bases de datos vectoriales, prompt engineering y despliegue de servicios.
