import pygame
from .base import TetrisBoard


class InfinitoMode(TetrisBoard):
    def __init__(self, sound_manager):
        super().__init__(sound_manager)
        
        self.nome_modo = "INFINITO"
        self.score = 0
        self.linhas_feitas = 0
        self.nivel = 1
        self.vitoria = False  # Necessário, pois o main.py checa isso

    def update(self, dt):
        pass

    def get_info_extra(self):
        return "LEVEL", str(self.nivel)

    def nova_peca(self):
        super().nova_peca()
        if self.game_over:
            pygame.mixer.music.stop()

    def verificar_linhas(self):
        self.linhas_para_animar = [i for i, linha in enumerate(self.grid) if 0 not in linha]

        if self.linhas_para_animar:
            qtd = len(self.linhas_para_animar)
            if qtd >= 4:
                self.animando = True
                self.anim_timer = 0
                self.anim_count = 0
                self.anim_flash_state = True
                self.sm.play('tetris')
            else:
                self.sm.play('clear')
                self.finalizar_linhas()
                self.nova_peca()
        else:
            self.nova_peca()

    def finalizar_linhas(self):
        qtd = len(self.linhas_para_animar)
        if qtd == 0:
            return

        pontos_base = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += pontos_base.get(qtd, 100) * self.nivel
        self.linhas_feitas += qtd

        # Level UP
        novo_nivel = 1 + (self.linhas_feitas // 10)
        if novo_nivel > self.nivel:
            self.nivel = novo_nivel
            self.sm.play('levelup')

        # Remove linhas e insere brancas no topo
        super().finalizar_linhas()

    def mover(self, dx, dy):
        if self.game_over or self.animando:
            return False

        if not self.checar_colisao(self.peca_x + dx, self.peca_y + dy, self.forma_atual):
            self.peca_x += dx
            self.peca_y += dy
            if dx != 0:
                self.sm.play('move')
            return True
        elif dy > 0:
            self.fixar_peca()
            return False
        return False