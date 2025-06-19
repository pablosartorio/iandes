#!/usr/bin/env python3
"""
play_with_subtitles_v2.py - Reproduce un audio con subtítulos usando diferentes métodos
"""
import argparse
import subprocess
import os
import sys
import tempfile
from pathlib import Path
import shutil


def check_dependencies():
    """Verifica que las dependencias estén disponibles."""
    missing = []
    if not shutil.which("ffplay"):
        missing.append("ffplay")
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg") 
    
    if missing:
        print(f"Error: {', '.join(missing)} no está/n instalado/s")
        print("Instala FFmpeg:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        sys.exit(1)


def method1_simple_ffplay(audio_path: str, srt_path: str, width: int = 640, height: int = 480):
    """Método 1: ffplay simple con video negro y subtítulos"""
    print("=== Probando Método 1: ffplay directo ===")
    
    cmd = [
        "ffplay",
        "-hide_banner",
        "-autoexit",
        "-f", "lavfi",
        "-i", f"color=size={width}x{height}:rate=25:color=black",
        "-i", audio_path,
        "-vf", f"subtitles={srt_path}",
        "-map", "0:v",
        "-map", "1:a"
    ]
    
    print("Comando:", " ".join(cmd))
    return subprocess.run(cmd)


def method2_ffmpeg_pipe(audio_path: str, srt_path: str, width: int = 640, height: int = 480):
    """Método 2: usar ffmpeg para generar video temporal y reproducir"""
    print("=== Probando Método 2: ffmpeg + ffplay ===")
    
    with tempfile.NamedTemporaryFile(suffix='.mkv', delete=False) as tmp:
        temp_video = tmp.name
    
    try:
        # Crear video con audio y subtítulos
        cmd_create = [
            "ffmpeg", "-y", "-hide_banner",
            "-f", "lavfi", "-i", f"color=size={width}x{height}:rate=25:color=black",
            "-i", audio_path,
            "-vf", f"subtitles={srt_path}",
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "copy",
            "-t", "3600",  # Máximo 1 hora
            temp_video
        ]
        
        print("Creando video temporal...")
        result = subprocess.run(cmd_create, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error creando video:", result.stderr)
            return result
        
        # Reproducir video temporal
        cmd_play = ["ffplay", "-hide_banner", "-autoexit", temp_video]
        print("Reproduciendo video temporal...")
        return subprocess.run(cmd_play)
        
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(temp_video)
        except:
            pass


def method3_simple_no_map(audio_path: str, srt_path: str, width: int = 640, height: int = 480):
    """Método 3: ffplay sin mapeo explícito"""
    print("=== Probando Método 3: ffplay sin mapeo ===")
    
    cmd = [
        "ffplay",
        "-hide_banner", 
        "-autoexit",
        "-i", audio_path,
        "-vf", f"color=size={width}x{height}:rate=25:color=black,subtitles={srt_path}"
    ]
    
    print("Comando:", " ".join(cmd))
    return subprocess.run(cmd)


def play_with_subs(audio_path: str, srt_path: str, width: int = 640, height: int = 480):
    """Intenta reproducir audio con subtítulos usando diferentes métodos."""
    
    check_dependencies()
    
    # Validar archivos
    audio = Path(audio_path)
    subs = Path(srt_path)
    
    if not audio.is_file():
        print(f"Error: no existe el archivo de audio: {audio}")
        sys.exit(1)
        
    if not subs.is_file():
        print(f"Error: no existe el archivo SRT: {subs}")
        sys.exit(1)

    audio_abs = str(audio.resolve())
    subs_abs = str(subs.resolve())
    
    print(f"Audio: {audio_abs}")
    print(f"Subtítulos: {subs_abs}")
    print("Presiona 'q' para salir durante la reproducción")
    print()
    
    # Probar diferentes métodos
    methods = [
        lambda: method1_simple_ffplay(audio_abs, subs_abs, width, height),
        lambda: method3_simple_no_map(audio_abs, subs_abs, width, height),
        lambda: method2_ffmpeg_pipe(audio_abs, subs_abs, width, height)
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            result = method()
            if result.returncode == 0:
                print(f"¡Éxito con método {i}!")
                return
            else:
                print(f"Método {i} falló con código: {result.returncode}")
                
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario")
            return
        except Exception as e:
            print(f"Error en método {i}: {e}")
        
        print()
    
    print("Ningún método funcionó. Verifica:")
    print("1. Que el archivo SRT esté bien formateado")
    print("2. Que no haya caracteres especiales problemáticos en las rutas")
    print("3. Que ffmpeg/ffplay estén actualizados")


def main():
    parser = argparse.ArgumentParser(
        description="Reproduce audio con subtítulos SRT (múltiples métodos)"
    )
    parser.add_argument("audio", help="Archivo de audio")
    parser.add_argument("srt", help="Archivo de subtítulos SRT")
    parser.add_argument("--width", type=int, default=640, help="Ancho del video")
    parser.add_argument("--height", type=int, default=480, help="Alto del video")
    
    args = parser.parse_args()
    play_with_subs(args.audio, args.srt, args.width, args.height)


if __name__ == "__main__":
    main()
