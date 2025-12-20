import pygame
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from config import *

PRESS_START_PATH = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")




def setup_opengl_projection(width, height):

    # 1. Ajusta Viewport
    glViewport(0, 0, width, height)

    # 2. Configura projeção ortográfica
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)

    # 3. Reset matriz modelo
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 4. Habilita transparência
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class SoundManager:
    def __init__(self):
        self.sons = {}
        # Carrega efeitos sonoros
        self.carregar_som('move', 'move_piece.wav')
        self.carregar_som('rotate', 'rotate_piece.wav')
        self.carregar_som('drop', 'piece_landed.wav')
        self.carregar_som('clear', 'line_clear.wav')
        self.carregar_som('tetris', 'tetris_4_lines.wav')
        self.carregar_som('gameover', 'game_over.wav')
        self.carregar_som('levelup', 'level_up_jingle.wav')

    def carregar_som(self, nome, arquivo):
        try:
            caminho = os.path.join("assets", arquivo)
            if not os.path.exists(caminho): caminho = arquivo
            if os.path.exists(caminho):
                self.sons[nome] = pygame.mixer.Sound(caminho)
                self.sons[nome].set_volume(0.5)
        except Exception:
            pass

    def play(self, nome):
        if nome in self.sons:
            self.sons[nome].play()

    def play_music(self):
        try:
            musica = os.path.join("assets", "theme.mp3")
            if not os.path.exists(musica): musica = "theme.mp3"
            if os.path.exists(musica):
                pygame.mixer.music.load(musica)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(loops=-1)
        except Exception:
            pass


def desenhar_texto(x, y, texto, tamanho=20, cor=(255, 255, 255)):

    try:
        if os.path.exists(PRESS_START_PATH):
            font = pygame.font.Font(PRESS_START_PATH, int(tamanho))
        else:
            font = pygame.font.Font(None, int(tamanho))
    except Exception:
        font = pygame.font.Font(None, int(tamanho))

    surface = font.render(texto, True, cor)
    text_data = pygame.image.tostring(surface, "RGBA", True)
    w, h = surface.get_width(), surface.get_height()
    tid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0);
    glVertex2f(x, y + h)
    glTexCoord2f(1, 0);
    glVertex2f(x + w, y + h)
    glTexCoord2f(1, 1);
    glVertex2f(x + w, y)
    glTexCoord2f(0, 1);
    glVertex2f(x, y)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDeleteTextures([tid])


def medir_texto(texto, tamanho=20):
    try:
        if os.path.exists(PRESS_START_PATH):
            font = pygame.font.Font(PRESS_START_PATH, int(tamanho))
        else:
            font = pygame.font.Font(None, int(tamanho))
    except Exception:
        font = pygame.font.Font(None, int(tamanho))
    surf = font.render(texto, True, (255, 255, 255))
    return surf.get_width(), surf.get_height()


def ajustar_tamanho_para_largura(texto, tamanho_preferido, max_largura):
    w, h = medir_texto(texto, tamanho_preferido)
    if w <= max_largura:
        return int(tamanho_preferido)
    # Escala linear para caber
    proporcao = max_largura / max(1, w)
    novo_tamanho = max(12, int(tamanho_preferido * proporcao))
    return novo_tamanho


def desenhar_retangulo(x, y, largura, altura, cor):
    glColor3fv(cor)
    glBegin(GL_QUADS)
    glVertex2f(x, y);
    glVertex2f(x + largura, y)
    glVertex2f(x + largura, y + altura);
    glVertex2f(x, y + altura)
    glEnd()
    glColor3f(0.26, 0.27, 0.35)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y);
    glVertex2f(x + largura, y)
    glVertex2f(x + largura, y + altura);
    glVertex2f(x, y + altura)
    glEnd()


def desenhar_ghost(x, y, largura, altura, cor_base):
    glEnable(GL_BLEND)
    r, g, b = cor_base
    glColor4f(r, g, b, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(x, y);
    glVertex2f(x + largura, y)
    glVertex2f(x + largura, y + altura);
    glVertex2f(x, y + altura)
    glEnd()
    glColor4f(r, g, b, 0.4)
    glLineWidth(1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y);
    glVertex2f(x + largura, y)
    glVertex2f(x + largura, y + altura);
    glVertex2f(x, y + altura)
    glEnd()


def desenhar_hud(jogo):
    # Fundo do HUD
    glColor3fv(COR_UI_BG)
    glBegin(GL_QUADS)
    glVertex2f(LARGURA_JOGO, 0);
    glVertex2f(LARGURA_TOTAL, 0)
    glVertex2f(LARGURA_TOTAL, ALTURA_JANELA);
    glVertex2f(LARGURA_JOGO, ALTURA_JANELA)
    glEnd()
    glColor3f(1, 1, 1);
    glLineWidth(2)
    glBegin(GL_LINES);
    glVertex2f(LARGURA_JOGO, 0);
    glVertex2f(LARGURA_JOGO, ALTURA_JANELA);
    glEnd()

    x_base = LARGURA_JOGO + 20

    # Nome do Modo
    nome = getattr(jogo, 'nome_modo', 'MODO')
    desenhar_texto(x_base + 2, 20, nome, 20, COR_DESTAQUE)

    # Próxima peça
    desenhar_texto(x_base, 80, "NEXT", 18, COR_TEXTO)
    offset_x_ui = LARGURA_JOGO + 70
    offset_y_ui = 110
    for bloco in jogo.proxima_forma:
        dx = bloco[0] * TAMANHO_BLOCO
        dy = bloco[1] * TAMANHO_BLOCO
        if len(jogo.proxima_forma) == 4 and jogo.proxima_forma[0] == [1, 0]: dx -= 15
        desenhar_retangulo(offset_x_ui + dx - 30, offset_y_ui + dy, TAMANHO_BLOCO, TAMANHO_BLOCO,
                           CORES[jogo.proxima_cor])

    # Score e Infos
    desenhar_texto(x_base, 220, "SCORE", 18, COR_TEXTO)
    desenhar_texto(x_base, 250, str(jogo.score), 25, COR_DESTAQUE)

    # Info Extra (nível, tempo, linha)
    titulo_extra, valor_extra = jogo.get_info_extra()
    desenhar_texto(x_base, 380, titulo_extra, 18, COR_TEXTO)
    desenhar_texto(x_base, 410, valor_extra, 25, COR_DESTAQUE)


def desenhar_jogo(jogo):
    glClearColor(*CORES[0], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Desenha Grid
    for y in range(LINHAS):
        cor_linha = None
        if jogo.animando and y in jogo.linhas_para_animar and jogo.anim_flash_state:
            cor_linha = COR_FLASH
        for x in range(COLUNAS):
            valor = jogo.grid[y][x]
            if valor > 0:
                cor_final = cor_linha if cor_linha else CORES[valor]
                desenhar_retangulo(x * TAMANHO_BLOCO, y * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO, cor_final)

    # Desenha Peça Atual e Ghost
    if not jogo.game_over and not jogo.animando:
        ghost_y = jogo.peca_y
        while not jogo.checar_colisao(jogo.peca_x, ghost_y + 1, jogo.forma_atual):
            ghost_y += 1

        # Ghost
        for bloco in jogo.forma_atual:
            x = (bloco[0] + jogo.peca_x) * TAMANHO_BLOCO
            gy = (bloco[1] + ghost_y) * TAMANHO_BLOCO
            if gy >= -TAMANHO_BLOCO:
                desenhar_ghost(x, gy, TAMANHO_BLOCO, TAMANHO_BLOCO, CORES[jogo.cor_atual])

        # Peça Real
        for bloco in jogo.forma_atual:
            x = (bloco[0] + jogo.peca_x) * TAMANHO_BLOCO
            y = (bloco[1] + jogo.peca_y) * TAMANHO_BLOCO
            if y >= -TAMANHO_BLOCO:
                desenhar_retangulo(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO, CORES[jogo.cor_atual])

    if jogo.game_over:
        msg = "VICTORY!" if jogo.vitoria else "GAMEOVER"
        cor_msg = (0, 255, 0) if jogo.vitoria else (255, 0, 0)
        margem = 40
        max_largura = max(80, LARGURA_JOGO - margem)

        titulo_pref = 48
        titulo_tam = ajustar_tamanho_para_largura(msg, titulo_pref, max_largura)
        w_titulo, h_titulo = medir_texto(msg, titulo_tam)
        x_titulo = (LARGURA_JOGO - w_titulo) // 2
        y_titulo = ALTURA_JANELA // 2 - h_titulo
        desenhar_texto(x_titulo, y_titulo, msg, titulo_tam, cor_msg)

        subtitulo = "Press R or ESC"
        sub_pref = 20
        sub_tam = ajustar_tamanho_para_largura(subtitulo, sub_pref, max_largura)
        w_sub, h_sub = medir_texto(subtitulo, sub_tam)
        x_sub = (LARGURA_JOGO - w_sub) // 2
        desenhar_texto(x_sub, y_titulo + h_titulo + 8, subtitulo, sub_tam, (255, 255, 255))

    # Desenha sempre a HUD lateral (inclui infos de score/next/etc.)
    desenhar_hud(jogo)

    pygame.display.flip()