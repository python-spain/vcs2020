#!/usr/bin/env python
""" Script para la creación de los vídeos de la PyconES 2020

  El Script necesita:
  1. Foto de inicio : foto_inicio.png que será la que se utilizará para crear el video inicial 5s
  2. Vídeo principal
  3. Vídeo final: por defecto video_end.mp4

  El resultado se guarda como nombre del vídeo principal

  Para simplificar supondremos que se sigue la convención:

  Foto inicio: video_principal.png
  Vídeo principal: video_principal.mp4
"""

from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip, ImageClip
from pathlib import Path
import argparse

def info(nombre):
    nombre = Path(nombre).stem
    num = nombre.split('-')[0]
    info = VideoFileClip('{}.mp4'.format(nombre)).subclip(0, 5)
    print ("info: h: {}, w: {}".format(info.h, info.w))


def generate():
    """Genera los vídeos de finalización"""
    for png in Path('.').glob('end_*.png'):
        nombre = png.stem
        res = nombre.split('_')[1]
        clip = ImageClip(png.name).set_duration(5)
        clip.write_videofile('{}.mp4'.format(nombre, res), fps=24)
        print ("info: h: {}, w: {}".format(clip.h, clip.w))
        clip.close()

def convert(nombre):
    # Obetenemos resolución
    nombre = Path(nombre).stem
    num = nombre.split('-')[0]
    info = VideoFileClip('{}.mp4'.format(nombre)).subclip(0, 5)
    res = info.h

    # Generamos la entradilla
    for png in Path('.').glob('{}-*_{}.png'.format(num, res)):
        clip = ImageClip(png.name).set_duration(5)
        clip.write_videofile('{}_start.mp4'.format(png.stem), fps=24)
        clip.close()
        entradilla = png


    # Generamos vídeo final
    clip1 = VideoFileClip('{}_start.mp4'.format(entradilla.stem))
    clip2 = VideoFileClip('{}.mp4'.format(nombre))
    clip3 = VideoFileClip('end_{}.mp4'.format(res))

    final = concatenate_videoclips([clip1, clip2, clip3], method="compose")
    final.write_videofile('{}_final.mp4'.format(nombre))
    final.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', help='nombre del video principal sin mp4')
    parser.add_argument('--info', help="muestra las dimensiones del video")
    parser.add_argument('--generate', help="genera los finales, use --generate all")
    args = parser.parse_args()
    if args.video:
        convert(args.video)
    elif args.info:
        info(args.info)
    elif args.generate:
        generate()
    else:
        print (__doc__)

