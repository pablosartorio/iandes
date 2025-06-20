### **Plan de Retención y Transferencia (KT\&R)**

**Nombre:**

**Abstract de perfil:**

---

#### **1 | Conocimiento crítico en riesgo** 

| Dominio | Justificación de criticidad | Evidencia de las entrevistas |
| :---: | :---: | :---: |

---

#### **2 | Sucesores y roles de aprendizaje**

| Rol futuro | Candidato principal | Estado actual | Brecha identificada |
| :---: | :---: | :---: | :---: |

---

#### **3 | Acciones de transferencia o explicitación**

| Tipo IAEA | Acción concreta | Responsable |
| :---: | :---: | :---: |

---

#### **4 | Riesgos y mitigaciones**

| Riesgo | Mitigación |
| :---: | :---: |

### **Etapa de “llenado de planilla” — paso a paso (alto nivel)**

1. **Transcribe cada audio y etiqueta los pasajes**

   * Pasa los audios por Whisper; guarda la transcripción con marcas de tiempo.

   * Asigna un identificador único a cada entrevista (ej.: ENT-001) para que después puedas rastrear la fuente de cada dato.

2. **Segmenta y limpia la transcripción**

   * Divide el texto en fragmentos breves (500–800 palabras) y elimina ruido (“eh…”, repeticiones, chistes internos).

   * Mantén los timestamps; serán la “dirección” que el modelo colocará como evidencia.

3. **Diseña cuatro prompts—uno por bloque de la plantilla KT\&R**

   * Prompt 1: Conocimiento crítico (Dominio, Justificación, Evidencias).

   * Prompt 2: Sucesores y roles.

   * Prompt 3: Acciones de transferencia.

   * Prompt 4: Riesgos y mitigaciones.  
      Cada prompt incluye:  
      *a)* una breve instrucción en español,  
      *b)* el fragmento de texto recuperado que parece relevante,  
      *c)* el formato JSON estricto que debe devolver.

4. **Orquesta la extracción automática**

   * Un pequeño script recorre las entrevistas:

     1. Busca los fragmentos más relacionados con cada bloque (palabras clave o embeddings).

     2. Llama al LLM con el prompt correspondiente.

     3. Vuelca la respuesta en la plantilla, junto a la cita y un campo “Confianza”.

   * Guarda cada plantilla como un archivo separado (JSON o Excel) con el mismo ID de entrevista.

5. **Validación rápida**

   * Un experto revisa la plantilla: marca ✔ si el dato es correcto y ✖ si debe corregirse.

   * Si hay inconsistencias de nombres entre bloques, ejecuta un segundo prompt de “reconciliación” para que el LLM unifique términos.

6. **Exportación y respaldo**

   * Convierte la plantilla validada a PDF o al formato que use tu repositorio de conocimiento.

   * Archiva el audio, la transcripción y la planilla final en la misma carpeta o sistema de versionado.

**Carga de trabajo aproximada**

* Configurar los prompts y el script: **1–2 días** de un analista.

* Ejecución automática por entrevista: **30 min** (tiempo de máquina).

* Revisión humana por entrevista: **40–60 min**.

Con este flujo, todo el esfuerzo manual se concentra en una revisión liviana; el resto lo hace el modelo de forma reproducible y trazable.

