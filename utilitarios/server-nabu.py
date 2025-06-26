#!/usr/bin/env python3
import tempfile
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from transformers import pipeline
import torch

# Valores por defecto, se pueden sobrescribir vía POST
DEFAULT_MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"
DEFAULT_PROMPT_TEMPLATE = (
    "Eres un asistente experto en generar resúmenes de charlas en español.\n"
    "A continuación tienes la transcripción completa:\n\n"
    "«{transcription}»\n\n"
    "Por favor, devuelve:\n"
    "1. Un índice de 3–5 temas principales en viñetas.\n"
    "2. Un resumen de máximo 200 palabras, claro y bien redactado.\n"
)

app = FastAPI(title="Llama3 Summarizer")

@app.post("/generate", response_class=FileResponse)
async def generate(
    doc: UploadFile = File(...),
    model_id: str = Form(DEFAULT_MODEL_ID),
    prompt_template: str = Form(DEFAULT_PROMPT_TEMPLATE),
    max_new_tokens: int = Form(512)
):
    # 1. Leer el archivo de texto
    transcript = (await doc.read()).decode("utf-8")

    # 2. Construir el prompt con el template enviado o por defecto
    full_prompt = prompt_template.format(transcription=transcript)

    # 3. Instanciar el pipeline con el modelo solicitado
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        return_full_text=False,
    )

    # 4. Generar el texto
    result = pipe(
        full_prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.2,
        top_p=0.9,
        repetition_penalty=1.1
    )[0]["generated_text"].strip()

    # 5. Escribir en un archivo temporal y devolverlo
    tmp = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt", encoding="utf-8")
    tmp.write(result)
    tmp.flush()
    return FileResponse(tmp.name, media_type="text/plain", filename="respuesta.txt")

