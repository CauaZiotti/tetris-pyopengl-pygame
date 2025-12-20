import pygame
import os
from OpenGL.GL import *
from .base import TetrisBoard


def desenhar_texto_relogio(x, y, texto, tamanho=20, cor=(255, 255, 255)):
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


class ContraRelogioMode(TetrisBoard):
    def __init__(self, sound_manager):
        super().__init__(sound_manager)
        
        self.nome_modo = "RELOGIO"
        
        # --- CONFIGURAÇÃO DO MODO ---
        # Tempo inicial em milissegundos (30 segundos)
        self.tempo_restante = 60 * 1000
        
        # Bônus por linha (3 segundos)
        self.bonus_linha = 3 * 1000
        
        # Força o nível alto para queda mais rápida
        self.nivel = 8
        
        self.vitoria = False
        self.score = 0  # Neste modo, apenas contamos o tempo

    def update(self, dt):
        """Reduz o tempo e verifica Game Over"""
        if not self.game_over and not self.vitoria:
            self.tempo_restante -= dt

            # Se o tempo acabar, Game Over
            if self.tempo_restante <= 0:
                self.tempo_restante = 0
                self.game_over = True
                pygame.mixer.music.stop()
                self.sm.play('gameover')

    def fixar_peca(self):
        #Apenas fixa a peça. Sem bônus por colocar peça.
        super().fixar_peca()

    def finalizar_linhas(self):
        #Sobrescrevemos para dar bonus de tempo por linhas limpas.
        qtd = len(self.linhas_para_animar)
        if qtd == 0:
            return

        if not self.game_over and self.tempo_restante > 0:
            # Ganha 3 segundos por linha
            ganho = self.bonus_linha * qtd
            self.tempo_restante += ganho
            self.sm.play('tetris')  # Som especial

        # Remove linhas
        super().finalizar_linhas()

    def get_info_extra(self):
        #Mostra o tempo restante formatado como mm:ss
        # Converte milissegundos para segundos
        segundos = int(self.tempo_restante / 1000)

        # Formata mm:ss
        minutos = segundos // 60
        segs = segundos % 60
        fmt = f"{minutos}:{segs:02d}"

        # Título muda dependendo do tempo restante
        titulo = "TEMPO"
        if segundos < 10:
            titulo = "CORRA!"
        elif segundos < 5:
            titulo = "ÚLTIMO!"

        return titulo, fmt
