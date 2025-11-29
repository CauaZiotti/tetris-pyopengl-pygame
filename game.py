import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from OpenGL.raw.GL.VERSION.GL_1_0 import *
from OpenGL.raw.GLU import *


WIDTH = 300
HIGHT = 600
SCALE = 30

COLUMN = WIDTH // SCALE
LINE = HIGHT // SCALE

COLORS = [
    (0.1, 0.1, 0.1),    # 0: Fundo (Cinza muito escuro)
    (1.0, 0.2, 0.2),    # 1: Vermelho
    (0.2, 1.0, 0.2),    # 2: Verde
    (0.2, 0.2, 1.0),    # 3: Azul
    (1.0, 1.0, 0.2),    # 4: Amarelo
    (0.2, 1.0, 1.0),    # 5: Ciano
    (1.0, 0.2, 1.0),    # 6: Magenta
    (1.0, 0.6, 0.0)     # 7: Laranja
]

FORMS = [
    [[0, 1], [1, 1], [2, 1], [3, 1]], # I
    [[0, 1], [1, 1], [2, 1], [2, 0]], # J
    [[0, 1], [1, 1], [2, 1], [0, 0]], # L
    [[1, 0], [2, 0], [1, 1], [2, 1]], # O
    [[1, 1], [2, 1], [0, 0], [1, 0]], # S
    [[1, 1], [0, 0], [1, 0], [2, 0]], # T
    [[0, 1], [1, 1], [1, 0], [2, 0]],  # Z
]

def init_opengl():
    glViewport(0, 0, WIDTH, HIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0, 0, 0, 1)

def collided(a, b):
    return (
        a["x"] < b["x"] + b["w"] and
        a["x"] + a["w"] > b["x"] and
        a["y"] < b["y"] + b["h"] and
        a["y"] + a["h"] > b["y"]
    )
