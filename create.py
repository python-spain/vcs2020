#!/usr/bin/env python
""" Script para la creación de los vídeos de la PyconES 2020
    El resultado se guarda como nombre del vídeo principal

    Suponemos que los vídeos están numerados y las carátulas empiezan
    con la numeración de los vídeos.

    El sistema intentará encontrar la mejor resolución de carátula para el vídeo,
    pero no realiza control de errores.

    Vídeos y carátula deben estar en el mismo directorio

    El resultado en el directorio final con el mismo nombre del vídeo.

    Si establecemos la variable a DEBUG solamente se generará el vído de NUM_SECONDS de duracion

"""

from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip, ImageClip
from PIL import Image
import numpy as np
from pathlib import Path
import argparse

from numpy.core.fromnumeric import size
NUM_SECONDS = 5
DEBUG = False

def info(nombre):
    info = VideoFileClip(nombre).subclip(0, NUM_SECONDS)
    print ("info: h: {}, w: {}".format(info.h, info.w))


def generate():
    """Genera los vídeos de finalización"""
    for png in Path('.').glob('end_*.png'):
        nombre = png.stem
        res = nombre.split('_')[1]
        clip = ImageClip(png.name).set_duration(NUM_SECONDS)
        clip.write_videofile('{}.mp4'.format(nombre, res), fps=24)
        print ("info: h: {}, w: {}".format(clip.h, clip.w))
        clip.close()

def generar_caratulas(num, clip_size):
    """generar_caratulas

        Genera y devuelve los vídeos de inicio y fin a partir
        de las imágnes de portada y finalización.

        (width, height)

    """
    inicio_mp4, fin_mp4 = None, None

    # generamos la imagen final
    out="end_{}.mp4".format(clip_size[1])
    if not Path(out).exists():
        im = Image.open('end_1440.png')
        im.resize(clip_size, Image.ANTIALIAS)
        name="end_{}.png".format(clip_size[0])
        im.save(name, "PNG")
        clip = ImageClip(name).set_duration(NUM_SECONDS)
        out="end_{}.mp4".format(clip_size[1])
        clip.write_videofile(out, fps=24)
        clip.close()
    fin_mp4 = Path(out)

    for png in Path('.').glob('{}-*_1440.png'.format(num)):
        im = Image.open(png.name)
        im.resize(clip_size, Image.ANTIALIAS)
        name_png="{}_{}_start.png".format(png.stem, clip_size[1])
        im.save(name_png, "PNG")

        clip = ImageClip(name_png).set_duration(NUM_SECONDS)
        name_mp4 = '{}_{}_start.mp4'.format(png.stem, clip_size[1])
        clip.write_videofile(name_mp4, fps=24)
        clip.close()
        inicio_mp4 = Path(name_mp4)
        break
    return inicio_mp4, fin_mp4

def convert(nombre):
    # Obetenemos resolución
    info = VideoFileClip(nombre).subclip(0, NUM_SECONDS)
    size = (info.w, info.h)
    res = info.h

    # obtenemos número del vídeo
    num = nombre.split('-')[0]

    # Generamos las carátulas

    entradilla, fin  = generar_caratulas(num, size)


    # Generamos vídeo final
    clip1 = VideoFileClip(entradilla.name, target_resolution = (info.h,info.w))
    if DEBUG:
        clip2 = VideoFileClip(nombre, target_resolution = (info.h, info.w)).subclip(0, NUM_SECONDS)
    else:
        clip2 = VideoFileClip(nombre, target_resolution = (info.h, info.w))
    clip3 = VideoFileClip(fin.name, target_resolution = (info.h, info.w))
    final = concatenate_videoclips([clip1, clip2, clip3], method="compose")
    Path('./final').mkdir(exist_ok=True)
    final.write_videofile('./final/{}'.format(nombre))
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

