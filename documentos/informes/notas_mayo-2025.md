# Informe pipeline transcripción - resumen - llenado de planilla 

## 1. Contexto
Desarrollo de un sistema **Retrieval‑Augmented Generation (RAG)** para generar resúmenes de charlas y usarlas para completar planillas.  
Hardware disponible: **GPU Nvidia A30, 24 GB VRAM** (Nabu UNC CCAD)

---

## 2. Temas a trabajar

| Tema | Detalles clave |
|------|----------------|
| **Modelos LLM** | *Mistral‑7B* (preferido para pruebas; 32 K contexto), alternativas: Llama 3‑8B, Falcon‑7B, Gemma‑27B, Phi‑4‑14B, Qwen2.5‑72B (cuantizado). |
| **Embedders** | 1. `hiiamsid/sentence_similarity_spanish_es` (768 dims)<br>2. `all-mpnet-base-v2` (768 dims)<br>3. `paraphrase-multilingual-mpnet-base-v2`<br>4. `E5-large-v2` (1024 dims)<br>5. `jina-embeddings-v2-base-es` (8192 token window). |
| **Vector DB** | Para prototipos: **ChromaDB**; para producción y optimización: **FAISS** (o servicios gestionados) |
| **Prompting** | Estructura sugerida: contexto ⟶ instrucción ⟶ ejemplos; controlar estilo y longitud. |
| **Chunking** | Dividir audio transcrito en fragmentos de 1 000‑2 000 tokens para mejorar relevancia y evitar superar el límite del LLM. |
| **Retrieval híbrido** | Combinar vectorial + BM25/TF‑IDF; planificado para una fase posterior. |

---

## 3. Recomendaciones

1. **LLM de referencia para pruebas:**  
   - Cargar **Mistral‑7B** en FP16 (`torch_dtype=torch.float16`) o 4‑bit (`bitsandbytes`) usando `device_map="auto"`.
2. **Embedding de alta fidelidad en español:**  
   - Iniciar con `hiiamsid/sentence_similarity_spanish_es`; probar `paraphrase-multilingual-mpnet-base-v2` y `E5-large-v2` si se requiere mayor performance.
3. **Motor de búsqueda vectorial:**  
   - Mantener **ChromaDB** para iterar rápido.  
   - Migrar a **FAISS** + HNSW + filtros si la latencia se vuelve crítica.
4. **Mejorar prompt y pipeline:**  
   - Añadir ejemplos *few‑shot* de (charla ⟶ resumen) para coherencia.  
   - Parametrizar `k` (documentos recuperados) entre 5‑10.  
   - Evaluar con ROUGE/BERTScore y revisión humana.
5. **Siguientes pasos:**  
   1. Implementar retrieval híbrido.  
   2. Medir impacto en calidad vs. latencia.  
   3. Afinar cuantización o loRA si se migran modelos mayores (Phi‑4‑14B, Qwen‑72B).

