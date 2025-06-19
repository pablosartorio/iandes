#!/usr/bin/env python3
# check_tokens.py

import sys
from transformers import AutoTokenizer

def contar_tokens(model_id, ruta_txt):
    """
    Carga el tokenizador del modelo indicado y cuenta cuántos tokens
    genera el contenido de ruta_txt.
    """
    # 1. Cargamos el tokenizador del modelo (descarga una vez de HuggingFace)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # 2. Leemos todo el texto del archivo
    with open(ruta_txt, 'r', encoding='utf-8') as f:
        texto = f.read()

    # 3. Tokenizamos (sin truncar) y contamos longitud
    tokens = tokenizer(texto, return_attention_mask=False, return_tensors=None)
    num_tokens = len(tokens["input_ids"])

    # 4. Límite de contexto del modelo
    max_context = tokenizer.model_max_length

    print(f"Modelo: {model_id}")
    print(f"Tokens en este texto: {num_tokens:,}")
    print(f"Límite (model_max_length): {max_context:,}")
    if num_tokens > max_context:
        print(">>> ATENCIÓN: El texto supera el límite de contexto. <<<")
    else:
        print("El texto cabe dentro del límite de contexto.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <model_id> <ruta_archivo.txt>")
        sys.exit(1)
    model_id = sys.argv[1]
    ruta = sys.argv[2]
    contar_tokens(model_id, ruta)
