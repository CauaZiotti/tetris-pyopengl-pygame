import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


WIDTH = 800
HEIGHT = 600
FPS = 60


# ------------------------------------
# Inicialização básica do OpenGL
# ------------------------------------
def init_opengl():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0, 0, 0, 1)


# ----------------------------------
# Desenho de retângulo simples
# ----------------------------------
def draw_rect(obj):
    glColor3f(obj["r"], obj["g"], obj["b"])
    glBegin(GL_QUADS)
    glVertex2f(obj["x"],             obj["y"])
    glVertex2f(obj["x"] + obj["w"],  obj["y"])
    glVertex2f(obj["x"] + obj["w"],  obj["y"] + obj["h"])
    glVertex2f(obj["x"],             obj["y"] + obj["h"])
    glEnd()


# ----------------------------
# Colisão AABB
# ----------------------------
def collided(a, b):
    return (
        a["x"] < b["x"] + b["w"] and
        a["x"] + a["w"] > b["x"] and
        a["y"] < b["y"] + b["h"] and
        a["y"] + a["h"] > b["y"]
    )


# -----------------------------
# Função principal
# ------------------------------

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Exemplo Procedural: Quadrado Atirando")

init_opengl()
clock = pygame.time.Clock()

# --------------------------------
# Objetos do jogo
# -------------------------------
player = {
    "x": WIDTH // 2,
    "y": 50,
    "w": 50,
    "h": 50,
    "speed": 7,
    "r": 0,
    "g": 1,
    "b": 0
}

shot = {
    "active": False,
    "x": 0,
    "y": 0,
    "w": 10,
    "h": 20,
    "speed": 10,
    "r": 1,
    "g": 1,
    "b": 0
}

enemy = {
    "x": WIDTH // 2 - 25,
    "y": HEIGHT - 120,
    "w": 50,
    "h": 50,
    "alive": True,
    "r": 1,
    "g": 0,
    "b": 0
}

# -------------------
# Loop principal
# -------------------
running = True
while running:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # -----------------
    # Movimentação do player
    # -----------------
    if keys[K_LEFT] and player["x"] > 0:
        player["x"] -= player["speed"]
    if keys[K_RIGHT] and player["x"] + player["w"] < WIDTH:
        player["x"] += player["speed"]

    # -----------------
    # Disparo
    # -----------------
    if keys[K_SPACE] and not shot["active"]:
        shot["active"] = True
        shot["x"] = player["x"] + player["w"] // 2 - 5
        shot["y"] = player["y"] + player["h"]

    # -----------------
    # Atualização do tiro
    # -----------------
    if shot["active"]:
        shot["y"] += shot["speed"]
        if shot["y"] > HEIGHT:
            shot["active"] = False

    # -----------------
    # Colisão tiro x inimigo
    # -----------------
    if enemy["alive"] and shot["active"]:
        if collided(shot, enemy):
            enemy["alive"] = False
            shot["active"] = False

    # -----------------
    # Desenho
    # -----------------
    glClear(GL_COLOR_BUFFER_BIT)

    draw_rect(player)

    if shot["active"]:
        draw_rect(shot)

    if enemy["alive"]:
        draw_rect(enemy)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()