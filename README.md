# vcs2020
Script de conversión de vídeo para la PyconES 2020 Covid Edition

Es un script guarro y rápido para la creación de los vídeos finales.

NSFAQ

* Solamente tengo los png de final

Puedes ejecutar un  ```python3 create.py --generate all```

* ¿Cómo funciona?

El vídeo y las carátulas deben empezar por un mismo número, por ejemplo 01-(algo).mp4 para el vídeo y
01-(otro algo carttula)_(resolutcion).png para la carátula. El sistema intentará elegir la mejor carátula
según la resolución de vídeo.

```python3 create.py --video nombre_del_video.mp4```


* ¿Hay control de errores?

He dicho rápido y sucio!

