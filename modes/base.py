"""
base.py - Classe base para todos os modos de Tetris
Consolida a lógica comum: grid, colisão, movimento, rotação, peças
"""
import random
from config import COLUNAS, LINHAS, FORMAS


class TetrisBoard:
    #Classe base que encapsula toda a lógica de um tabuleiro Tetris

    def __init__(self, sound_manager):
        #sound_manager: Gerenciador de sons para tocar efeitos

        self.sm = sound_manager
        
        # Grid e peças
        self.grid = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]
        self.forma_atual = None
        self.cor_atual = 0
        self.peca_x = 0
        self.peca_y = 0
        
        self.proxima_forma = random.choice(FORMAS)
        self.proxima_cor = random.randint(1, 7)
        
        # Estado
        self.game_over = False
        self.animando = False
        self.linhas_para_animar = []
        self.anim_timer = 0
        self.anim_flash_state = False
        self.anim_count = 0
        
        # Inicializa primeira peça
        self.nova_peca()

    def nova_peca(self):
        #Cria uma nova peça no topo do grid
        self.forma_atual = self.proxima_forma
        self.cor_atual = self.proxima_cor
        self.peca_x = COLUNAS // 2 - 2
        self.peca_y = 0

        self.proxima_forma = random.choice(FORMAS)
        self.proxima_cor = random.randint(1, 7)

        if self.checar_colisao(self.peca_x, self.peca_y, self.forma_atual):
            self.game_over = True
            self.sm.play('gameover')

    def checar_colisao(self, offset_x, offset_y, forma):
        #Verifica se uma forma em posição causa colisão com grid ou bordas
        for bloco in forma:
            x = bloco[0] + offset_x
            y = bloco[1] + offset_y
            
            # Colisão com bordas
            if x < 0 or x >= COLUNAS or y >= LINHAS:
                return True
            
            # Colisão com grid já preenchido
            if y >= 0 and self.grid[y][x] > 0:
                return True
        
        return False

    def rotacionar(self):
        #Rotaciona a peça atual 90 graus no sentido horário
        if self.game_over or self.animando:
            return
        
        # Rotação: (x, y) -> (-y, x), depois normaliza
        nova_forma = [[-bloco[1], bloco[0]] for bloco in self.forma_atual]
        
        # Normaliza para coordenadas positivas
        min_x = min(b[0] for b in nova_forma)
        min_y = min(b[1] for b in nova_forma)
        nova_forma = [[b[0] - min_x, b[1] - min_y] for b in nova_forma]

        # Tenta rotação se não houver colisão
        if not self.checar_colisao(self.peca_x, self.peca_y, nova_forma):
            self.forma_atual = nova_forma
            self.sm.play('rotate')

    def mover(self, dx, dy):
        #Move a peça atual. Se encontrar colisão vertical, fixa a peça
        if self.game_over or self.animando:
            return False

        if not self.checar_colisao(self.peca_x + dx, self.peca_y + dy, self.forma_atual):
            self.peca_x += dx
            self.peca_y += dy
            if dx != 0:
                self.sm.play('move')
            return True
        
        elif dy > 0:  # Tentou cair e colidiu -> fixa
            self.fixar_peca()
            return False
        
        return False

    def fixar_peca(self):
        #Fixa a peça atual no grid
        for bloco in self.forma_atual:
            x = bloco[0] + self.peca_x
            y = bloco[1] + self.peca_y
            
            if 0 <= y < LINHAS and 0 <= x < COLUNAS:
                self.grid[y][x] = self.cor_atual

        self.sm.play('drop')
        self.verificar_linhas()

    def verificar_linhas(self):
        #Verifica quais linhas estão completas.
        #Subclasses podem sobrescrever para comportamento customizado.
        self.linhas_para_animar = [i for i, linha in enumerate(self.grid) if 0 not in linha]

        if self.linhas_para_animar:
            # Inicia animação
            self.animando = True
            self.anim_timer = 0
            self.anim_count = 0
            self.anim_flash_state = True
        else:
            # Sem linhas completas, próxima peça
            self.nova_peca()

    def update_animacao(self, dt):
        #Atualiza animação de linhas limpas.
        if not self.animando:
            return
        
        self.anim_timer += dt
        if self.anim_timer > 80:
            self.anim_timer = 0
            self.anim_flash_state = not self.anim_flash_state
            self.anim_count += 1
            
            if self.anim_count > 6:
                self.finalizar_linhas()
                self.animando = False
                self.nova_peca()

    def finalizar_linhas(self):
        #Remove as linhas completas do grid.
        #Subclasses podem sobrescrever para adicionar lógica pós-limpeza (pontos, lixo).
        qtd = len(self.linhas_para_animar)
        if qtd == 0:
            return

        # Remove linhas em ordem reversa
        for i in reversed(self.linhas_para_animar):
            del self.grid[i]
        
        # Adiciona linhas em branco no topo
        for _ in self.linhas_para_animar:
            self.grid.insert(0, [0 for _ in range(COLUNAS)])

        self.linhas_para_animar = []

    def update(self, dt):
        #Atualiza lógica do modo (sobrecarregar em subclasses se necessário).
        pass

    def get_info_extra(self):
        #Retorna (Título, Valor) para exibir no HUD.
        #Subclasses devem sobrescrever para mostrar level, tempo, etc.
        return "", ""
