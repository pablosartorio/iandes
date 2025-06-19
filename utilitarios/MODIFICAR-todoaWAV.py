"""
ingest.py - Primero paso del pipeline: detecta archivos de audio y video, extrae el audio de los videos,
crea un manifiesto JSON con la lista de audios preparados para los siguientes pasos (diarización y transcripción).

Uso:
    python ingest.py <input_dir> <output_dir>

    - <input_dir>: carpeta que contiene archivos de audio (.wav, .mp3, .flac, .m4a)
                   y/o video (.mp4, .mkv, .mov, .avi). Puede tener subdirectorios.
    - <output_dir>: carpeta donde se guardarán:
         * audios extraídos (o symlinks de los audios originales)
         * manifest.json con:
             [
               {"source": "ruta/original/file.ext", "audio": "ruta/output/file.wav"},
               ...
             ]

Requisitos:
    - Python 3.7+
    - ffmpeg instalado en el sistema (para extraer audio de videos)

"""
import os
import argparse
import logging
import json
import subprocess

# Extensiones soportadas
VIDEO_EXT = ['.mp4', '.mkv', '.mov', '.avi']
AUDIO_EXT = ['.wav', '.mp3', '.flac', '.m4a']


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detecta archivos de audio/video y prepara audios para transcripción"
    )
    parser.add_argument(
        'input_dir',
        help="Carpeta raíz con archivos de audio o video"
    )
    parser.add_argument(
        'output_dir',
        help="Carpeta donde se guardarán los audios procesados y el manifiesto"
    )
    parser.add_argument(
        '--ext',
        nargs='+',
        default=AUDIO_EXT + VIDEO_EXT,
        help="Extensiones a incluir (por defecto .wav,.mp3,.flac,.m4a,.mp4,.mkv,.mov,.avi)"
    )
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def find_media_files(root_dir, extensions):
    """
    Recorre root_dir recursivamente y devuelve lista de rutas
    cuyos nombres terminan en una de las extensiones.
    """
    exts = set(ext.lower() for ext in extensions)
    media = []
    for path, _, files in os.walk(root_dir):
        for fname in files:
            if os.path.splitext(fname)[1].lower() in exts:
                media.append(os.path.join(path, fname))
    return media


def extract_audio_from_video(video_path, output_path):
    """
    Usa ffmpeg para extraer el audio de un video a WAV mono 16kHz.
    """
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vn',                # sin video
        '-acodec', 'pcm_s16le',
        '-ar', '16000',       # tasa de muestreo 16 kHz
        '-ac', '1',           # mono
        output_path
    ]
    try:
#        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(cmd, check=True, capture_output=True, text=True)  # Muestra errores
        logging.info(f"Audio extraído: {output_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error extrayendo audio de {video_path}: {e}")


def main():
    args = parse_args()
    setup_logging()

    # Crear carpeta de salida si no existe
    os.makedirs(args.output_dir, exist_ok=True)

    manifest = []
    media_files = find_media_files(args.input_dir, args.ext)

    for src in media_files:
        base, ext = os.path.splitext(os.path.basename(src))
        ext = ext.lower()

        if ext in VIDEO_EXT:
            # Extraer audio de video
            out_audio = os.path.join(args.output_dir, f"{base}.wav")
            extract_audio_from_video(src, out_audio)
            manifest.append({'source': src, 'audio': out_audio})
        else:
            # Audio: creamos un symlink en output_dir para uniformidad
            dest = os.path.join(args.output_dir, os.path.basename(src))
            if not os.path.exists(dest):
                os.symlink(os.path.abspath(src), dest)
            manifest.append({'source': src, 'audio': dest})

        logging.info(f"Procesado: {src}")

    # Guardar manifiesto
    manifest_path = os.path.join(args.output_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    logging.info(f"Manifiesto guardado en: {manifest_path}")


if __name__ == '__main__':
    main()
