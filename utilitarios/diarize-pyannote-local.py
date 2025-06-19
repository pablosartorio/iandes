#!/usr/bin/env python3
"""
diarize.py - Segundo paso del pipeline: aplica PyAnnote para detectar quién habla cuándo.

Uso:
    python diarize.py <manifest.json> <output_dir> --token <HUGGINGFACE_TOKEN>

Requisitos:
    - Python 3.7+
    - pip install pyannote.audio
    - pip install torch  # con soporte CUDA si querés GPU
    - Tener un token de Hugging Face con acceso al modelo de diarización

El script lee el manifest.json generado por ingest.py, recorre cada audio,
lanza el pipeline de diarización y guarda, para cada archivo, un JSON con:
    {
      "source": "ruta/al/audio.wav",
      "segments": [
         {"start": 0.0, "end": 3.5, "speaker": "SPEAKER_00"},
         ...
      ]
    }

"""
import os
import argparse
import json
import torch
from pyannote.audio import Pipeline

def parse_args():
    parser = argparse.ArgumentParser(
        description="Diarización de speakers con PyAnnote"
    )
    parser.add_argument(
        'manifest',
        help='Ruta al manifest.json generado en ingest.py'
    )
    parser.add_argument(
        'output_dir',
        help='Carpeta donde se guardarán los resultados de diarización'
    )
    parser.add_argument(
        '--token',
        required=True,
        help='Token de Hugging Face para acceder al modelo preentrenado'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Creamos la carpeta de salida si no existe
    os.makedirs(args.output_dir, exist_ok=True)

    # Detectar dispositivo (GPU si está disponible)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Cargar el pipeline de diarización de PyAnnote y moverlo al dispositivo
    pipeline = Pipeline.from_pretrained(
        'pyannote/speaker-diarization',
        use_auth_token=args.token
    )
    pipeline.to(device)

    # Leer el manifest para obtener la lista de audios
    with open(args.manifest, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    for entry in manifest:
        audio_path = entry['audio']
        base = os.path.splitext(os.path.basename(audio_path))[0]

        # Ejecutar diarización (nota: ahora se pasa argumento 'file')
        diarization = pipeline(file=audio_path)

        # Extraer segmentos con timestamps y labels de speaker
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                'start': round(turn.start, 2),
                'end': round(turn.end, 2),
                'speaker': speaker
            })

        # Guardar resultado en JSON
        out_path = os.path.join(args.output_dir, f"{base}_diarization.json")
        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump({
                'source': audio_path,
                'segments': segments
            }, out_f, indent=2, ensure_ascii=False)

        print(f"Diarización guardada: {out_path}")

if __name__ == '__main__':
    main()

