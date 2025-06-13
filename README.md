# TFG-Clasificador_de_residuos_autonomo
Este proyecto consiste en el desarrollo de un sistema autónomo capaz de clasificar residuos domésticos (papel/cartón, vidrio, envases ligeros y residuos orgánicos) utilizando visión artificial.

Implementado sobre una Raspberry Pi 3B+, el sistema emplea una red neuronal convolucional (CNN) optimizada mediante Transfer Learning con MobileNetV2. El modelo identifica el tipo de residuo a partir de una imagen capturada, y el sistema controla servomotores para depositarlo en el contenedor correspondiente.

El objetivo es fomentar el reciclaje correcto automatizando el proceso, sin depender del conocimiento del usuario sobre la clasificación de residuos. El sistema es económico, replicable y pensado para integrarse fácilmente en entornos domésticos o comerciales.

Tecnologías: Python, TensorFlow, Teachable Machine, Raspberry Pi, sensores (PIR, ultrasonido), cámara OV5647, LCD, servomotores SG90.
