import pygame
import os
from pygame.locals import *
from OpenGL.GL import *
import random
from config import *
from .base import TetrisBoard
from utils import setup_opengl_projection


def desenhar_texto(x, y, texto, tamanho=20, cor=(255, 255, 255)):
    PRESS_START_PATH = os.path.join("assets", "fonts", "PressStart2P-Regular.ttf")
    try:
        if os.path.exists(PRESS_START_PATH):
            font = pygame.font.Font(PRESS_START_PATH, tamanho)
        else:
            font = pygame.font.Font(None, tamanho + 10)
    except Exception:
        font = pygame.font.Font(None, tamanho + 10)
    
    surface = font.render(texto, True, cor)
    data = pygame.image.tostring(surface, "RGBA", True)
    w, h = surface.get_width(), surface.get_height()
    
    tid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y + h)
    glTexCoord2f(1, 0); glVertex2f(x + w, y + h)
    glTexCoord2f(1, 1); glVertex2f(x + w, y)
    glTexCoord2f(0, 1); glVertex2f(x, y)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDeleteTextures([tid])


# --- Configurações de Tela Específicas do Duo ---
LARGURA_BOARD = COLUNAS * TAMANHO_BLOCO
LARGURA_TOTAL = LARGURA_BOARD * 2  # Dois tabuleiros lado a lado
ALTURA_JANELA = LINHAS * TAMANHO_BLOCO


class PlayerInstance(TetrisBoard):
    def __init__(self, player_id, offset_draw_x, sm, opponent=None):
        super().__init__(sm)
        
        self.id = player_id
        self.offset_draw_x = offset_draw_x
        self.opponent = opponent
        self.vencedor = False

        # Input timing
        self.move_timer = 0
        self.last_move_key = None
        self.fall_time = 0
        self.velocidade = 500

    def set_opponent(self, opponent):
        #Define o oponente para enviar lixo
        self.opponent = opponent

    def nova_peca(self):
        #marca vitória do oponente se game over
        super().nova_peca()
        if self.game_over and self.opponent:
            self.opponent.vencedor = True

    def verificar_linhas(self):
        self.linhas_para_animar = [i for i, l in enumerate(self.grid) if 0 not in l]
        if self.linhas_para_animar:
            qtd = len(self.linhas_para_animar)
            if qtd >= 4:
                self.sm.play('tetris')
            else:
                self.sm.play('clear')
            self.animando = True
            self.anim_timer = 0
            self.anim_count = 0
        else:
            self.nova_peca()

    def update_animacao(self, dt):
        if not self.animando:
            return
        self.anim_timer += dt
        if self.anim_timer > 60:
            self.anim_timer = 0
            self.anim_flash_state = not self.anim_flash_state
            self.anim_count += 1
            if self.anim_count > 6:
                self.finalizar_linhas()
                self.animando = False
                self.nova_peca()

    def finalizar_linhas(self):
        #envia lixo para oponente baseado em linhas limpas
        qtd = len(self.linhas_para_animar)
        lixo = 0
        
        if qtd == 2:
            lixo = 1
        elif qtd == 3:
            lixo = 2
        elif qtd >= 4:
            lixo = 4

        if lixo > 0 and self.opponent and not self.opponent.game_over:
            self.opponent.receber_lixo(lixo)
            self.sm.play('garbage')

        # Remove linhas
        super().finalizar_linhas()

    def receber_lixo(self, quantidade):
        #Recebe linhas de lixo do oponente
        for _ in range(quantidade):
            if 0 not in self.grid[0]:
                self.game_over = True
                self.sm.play('gameover')
                if self.opponent:
                    self.opponent.vencedor = True
            
            del self.grid[0]
            linha = [8] * COLUNAS
            linha[random.randint(0, COLUNAS - 1)] = 0
            self.grid.append(linha)

    def update(self, dt, keys, key_map):
        #Atualiza movimento contínuo do player
        if self.game_over or self.vencedor:
            return
        
        if self.animando:
            self.update_animacao(dt)
            return

        # Input contínuo LEFT/RIGHT com delay + repeat
        if keys[key_map['left']] or keys[key_map['right']]:
            current = key_map['left'] if keys[key_map['left']] else key_map['right']
            if self.last_move_key != current:
                self.last_move_key = current
                self.move_timer = 200
                self.mover(-1 if current == key_map['left'] else 1, 0)
            else:
                self.move_timer -= dt
                if self.move_timer <= 0:
                    self.mover(-1 if current == key_map['left'] else 1, 0)
                    self.move_timer = 50
        else:
            self.last_move_key = None

        # Input contínuo DOWN (queda rápida)
        self.fall_time += dt
        limit = 50 if keys[key_map['down']] else self.velocidade
        if self.fall_time >= limit:
            self.mover(0, 1)
            self.fall_time = 0


def desenhar_retangulo_bloco(x, y, cor):
    glColor3fv(cor)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + TAMANHO_BLOCO, y)
    glVertex2f(x + TAMANHO_BLOCO, y + TAMANHO_BLOCO)
    glVertex2f(x, y + TAMANHO_BLOCO)
    glEnd()
    glColor3f(0.2, 0.2, 0.3)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + TAMANHO_BLOCO, y)
    glVertex2f(x + TAMANHO_BLOCO, y + TAMANHO_BLOCO)
    glVertex2f(x, y + TAMANHO_BLOCO)
    glEnd()


def desenhar_player(p):
    ox = p.offset_draw_x
    
    # Fundo do tabuleiro
    glColor3fv(CORES[0])
    glBegin(GL_QUADS)
    glVertex2f(ox, 0)
    glVertex2f(ox + LARGURA_BOARD, 0)
    glVertex2f(ox + LARGURA_BOARD, ALTURA_JANELA)
    glVertex2f(ox, ALTURA_JANELA)
    glEnd()

    # Desenha grid
    for y in range(LINHAS):
        cline = None
        if p.animando and y in p.linhas_para_animar and p.anim_flash_state:
            cline = COR_FLASH
        for x in range(COLUNAS):
            v = p.grid[y][x]
            if v > 0:
                px, py = ox + x * TAMANHO_BLOCO, y * TAMANHO_BLOCO
                desenhar_retangulo_bloco(px, py, cline if cline else CORES[v])

    # Desenha peça atual + ghost
    if not p.game_over and not p.vencedor and not p.animando:
        # Calcula posição ghost
        gy = p.peca_y
        while not p.checar_colisao(p.peca_x, gy + 1, p.forma_atual):
            gy += 1
        
        # Ghost
        glEnable(GL_BLEND)
        r, g, b = CORES[p.cor_atual]
        glColor4f(r, g, b, 0.2)
        glBegin(GL_QUADS)
        for bloco in p.forma_atual:
            px = ox + (bloco[0] + p.peca_x) * TAMANHO_BLOCO
            py = (bloco[1] + gy) * TAMANHO_BLOCO
            if py >= 0:
                glVertex2f(px, py)
                glVertex2f(px + TAMANHO_BLOCO, py)
                glVertex2f(px + TAMANHO_BLOCO, py + TAMANHO_BLOCO)
                glVertex2f(px, py + TAMANHO_BLOCO)
        glEnd()
        glDisable(GL_BLEND)
        
        # Peça real
        for bloco in p.forma_atual:
            px = ox + (bloco[0] + p.peca_x) * TAMANHO_BLOCO
            py = (bloco[1] + p.peca_y) * TAMANHO_BLOCO
            if py >= 0:
                desenhar_retangulo_bloco(px, py, CORES[p.cor_atual])

    # Status final
    if p.game_over:
        desenhar_texto(ox + 40, ALTURA_JANELA // 2, "DEFEAT", 40, (255, 50, 50))
    if p.vencedor:
        desenhar_texto(ox + 20, ALTURA_JANELA // 2, "WINNER!", 40, (50, 255, 50))


# --- FUNÇÃO RUNNER ---
def run_duo_mode(sound_manager):
    # 1. Configura a janela com o tamanho específico deste modo
    pygame.display.set_mode((LARGURA_TOTAL, ALTURA_JANELA), DOUBLEBUF | OPENGL)

    # 2. Usa função centralizada para configurar projeção
    setup_opengl_projection(LARGURA_TOTAL, ALTURA_JANELA)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    sm = sound_manager
    p1 = PlayerInstance(1, 0, sm)
    p2 = PlayerInstance(2, LARGURA_BOARD, sm)
    p1.set_opponent(p2)
    p2.set_opponent(p1)

    keys_p1 = {'left': K_a, 'right': K_d, 'rot': K_w, 'down': K_s, 'drop': K_LSHIFT}
    keys_p2 = {'left': K_LEFT, 'right': K_RIGHT, 'rot': K_UP, 'down': K_DOWN, 'drop': K_RETURN}

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()

        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
                return -1

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False

                # Reset
                if e.key == K_r and (p1.game_over or p2.game_over):
                    return run_duo_mode(sm)

                if not p1.game_over and not p1.vencedor:
                    if e.key == keys_p1['drop']:
                        while p1.mover(0, 1):
                            pass
                    if e.key == keys_p1['rot']:
                        p1.rotacionar()

                if not p2.game_over and not p2.vencedor:
                    if e.key == keys_p2['drop']:
                        while p2.mover(0, 1):
                            pass
                    if e.key == keys_p2['rot']:
                        p2.rotacionar()

        # Atualiza players
        p1.update(dt, keys, keys_p1)
        p2.update(dt, keys, keys_p2)

        # Renderização
        glClearColor(*COR_JANELA, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        desenhar_player(p1)
        desenhar_player(p2)

        # Linha separadora no meio
        meio = LARGURA_BOARD
        glColor3f(1, 1, 1)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(meio, 0)
        glVertex2f(meio, ALTURA_JANELA)
        glEnd()

        # Labels
        desenhar_texto(10, 10, "P1 (WASD)", 18, (150, 150, 150))
        desenhar_texto(LARGURA_BOARD + 10, 10, "P2 (Arrows)", 18, (150, 150, 150))

        pygame.display.flip()

    return 0