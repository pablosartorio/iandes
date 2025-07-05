# 📐 Arquitectura de alto nivel - Sistema IA para Escuelas

## 🎯 Objetivo

Desarrollar un sistema web que permita a escuelas:

- Cargar documentos y audios.
- Procesar esa información con IA (LLM + Whisper).
- Almacenar y consultar resultados vía RAG.
- Generar planillas y documentos automáticos.
- Escalar según demanda con costos controlados.

---

## 🏗 Arquitectura general

El sistema está compuesto por:

### 1️⃣ Frontend Web

- **Framework:** React / Vue / Streamlit
- **Funciones:**

  - Formularios para subir documentos y audios.
  - Configurar prompts personalizados.
  - Visualizar resultados y planillas generadas.
- **Comunicación:** HTTP REST hacia el Backend.

---

### 2️⃣ Backend API

- **Framework:** FastAPI (Python) / Flask (o alternativamente Node.js con Express).

- **Funciones:**
  - Orquesta los servicios IA.
  - Decide si usa Ollama local, API externa o GPU remota.
  - Administra lógica de negocio, usuarios y seguridad.
- **Hosting:** VPS en DonWeb con Docker Compose.

---

### 3️⃣ Bases de Datos

- **PostgreSQL (relacional):**
  - Guarda usuarios, documentos, auditorías, configuraciones.
- **ChromaDB (vectorial):**
  - Almacena embeddings para búsquedas semánticas (RAG).

Ambas residen inicialmente en el mismo VPS.

---

### 4️⃣ Motores de IA

#### a) Ollama local

- Corre en CPU del VPS.
- Para inferencias económicas, consultas rápidas o sin dependencia externa.

#### b) API externa

- OpenAI (ChatGPT), Gemini (Google), Anthropic (Claude).
- Ideal para resultados premium sin mantener infraestructura.

#### c) GPU remota

- RunPod, LambdaLabs, Vast.ai o AWS EC2/SageMaker con GPU.
- Para grandes lotes de embeddings, transcripciones largas o LLMs complejos.
- Se paga sólo por uso, evitando costos fijos altos.

---

### 5️⃣ Whisper (speech-to-text)

- **Local en VPS:** Para audios cortos.
- **En GPU remota:** Para transcripciones largas, dentro del mismo nodo que el LLM.

---

## ⚙ Orquestación y despliegue

- Cada componente encapsulado en Docker.
- **Docker Compose** para manejo local del stack.
- El VPS en DonWeb centraliza el backend, DBs, Ollama y Whisper básicos.
- GPUs y APIs externas se integran vía HTTP, según la lógica orquestada por el backend.

---

## 🚀 Escalabilidad

- Al crecer la demanda o tamaño del vector DB, puede migrarse a:
  - Otro VPS dedicado con más RAM.
  - Servicios gestionados como Pinecone o Weaviate Cloud.
- Si suben las consultas LLM:
  - Balanceo entre varios nodos GPU remotos o upgrade a instancias permanentes.

---

## 📊 Diagrama de arquitectura

![Imagen del diagrama](documentos/diagramas/arquitectura.svg)

```plaintext
+-----------------------+
|       Frontend        |
|  (React / Streamlit)  |
+-----------------------+
            |
            v
+----------------------------+
|        Backend API         |
|     (FastAPI / Flask)      |
+----------------------------+
 |          |          |          |
 v          v          v          v
+---+    +------+   +------+   +------+
|SQL|    |Vector|   |Ollama|   |Whisper|
|DB |    |DB    |   |Local |   |Local  |
+---+    +------+   +------+   +------+
 |                        |
 +------------------------+
            |
            v
+----------------------------+
|   Llamadas a LLM externos  |
| (OpenAI, Gemini, GPU node) |
+----------------------------+
````

---

## 🧩 Stack tecnológico

| Capa            | Tecnologías posibles             |
| --------------- | -------------------------------- |
| Frontend        | React, Vue, Streamlit            |
| Backend API     | FastAPI (Python), Flask, Express |
| LLM local       | Ollama (CPU)                     |
| LLM externo     | OpenAI, Gemini, Anthropic        |
| GPU remota      | RunPod, LambdaLabs, Vast.ai, AWS |
| DB relacional   | PostgreSQL                       |
| DB vectorial    | ChromaDB                         |
| Transcripción   | Whisper CPU / GPU                |
| Contenerización | Docker + Docker Compose          |
| Infraestructura | VPS DonWeb + GPU spot externo    |

---

## ✅ Ventajas

- Costos fijos muy bajos: sólo el VPS.
- Escalable: se usa GPU o API solo cuando se necesita.
- Modular: cada componente puede evolucionar o moverse según crecimiento.

---

## 🚀 Próximos pasos

- Generar diagramas gráficos (draw\.io / Mermaid).
- Definir métricas y logs clave.
- Planificar escalabilidad (auto-escalado GPU, DBs gestionadas).

---
