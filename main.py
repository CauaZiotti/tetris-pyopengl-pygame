"""
Autores: Cauã Felipe Ziotti Tamiozzo e Diego Breskovit Morcelli
Jogo de inspiração: Tetris (Atari)
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *

from config import *
from utils import SoundManager, desenhar_retangulo, desenhar_texto, desenhar_jogo, setup_opengl_projection
from modes.infinito import InfinitoMode
from modes.duo import run_duo_mode
from modes.contraRelogio import ContraRelogioMode


def loop_menu(clock):
    # Garante a resolução correta sempre que entra no menu
    pygame.display.set_mode((LARGURA_TOTAL, ALTURA_JANELA), DOUBLEBUF | OPENGL)
    setup_opengl_projection(LARGURA_TOTAL, ALTURA_JANELA)

    selecionado = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT: return -1
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selecionado = (selecionado - 1) % 4
                elif event.key == K_DOWN:
                    selecionado = (selecionado + 1) % 4
                elif event.key == K_RETURN:
                    if selecionado == 3: return -1
                    return selecionado

        # Renderização do Menu
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        desenhar_retangulo(0, 0, LARGURA_TOTAL, ALTURA_JANELA, COR_UI_BG)
        desenhar_texto(LARGURA_TOTAL // 2 - 160, 70, "TETRIS", 50, COR_DESTAQUE)

        opcoes = ["INFINITO", "PVP(DUO)", "RELÓGIO", "SAIR"]
        y_start = 240
        espacamento = 56
        for i, texto in enumerate(opcoes):
            selecionado_cor = COR_DESTAQUE if i == selecionado else COR_TEXTO
            x_text = LARGURA_TOTAL // 2 - 80
            if i == selecionado:
                desenhar_texto(x_text - 28, y_start + i * espacamento, ">", 22, selecionado_cor)
            desenhar_texto(x_text, y_start + i * espacamento, texto, 22, selecionado_cor)

        pygame.display.flip()


def run_infinito(sm, clock, modo_class=None):
    # Usar InfinitoMode como padrão se nenhuma classe for fornecida
    if modo_class is None:
        modo_class = InfinitoMode
    
    # Garante resolução correta
    pygame.display.set_mode((LARGURA_TOTAL, ALTURA_JANELA), DOUBLEBUF | OPENGL)
    setup_opengl_projection(LARGURA_TOTAL, ALTURA_JANELA)

    jogo = modo_class(sm)
    running = True
    fall_time = 0
    velocidade_base = 500
    move_timer = 0;
    move_delay = 200;
    move_interval = 50;
    last_move_key = None

    while running:
        dt = clock.tick(60)
        jogo.update(dt)

        for event in pygame.event.get():
            if event.type == QUIT: return -1
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: running = False
                if event.key == K_r and (jogo.game_over or getattr(jogo, 'vitoria', False)):
                    sm.play_music()
                    jogo = modo_class(sm)

                # Inputs Instantâneos
                if not jogo.game_over and not jogo.animando:
                    if event.key == K_UP: jogo.rotacionar()
                    if event.key == K_SPACE:
                        while jogo.mover(0, 1): pass
                    if event.key == K_LEFT:
                        jogo.mover(-1, 0);
                        move_timer = 0;
                        last_move_key = K_LEFT
                    elif event.key == K_RIGHT:
                        jogo.mover(1, 0);
                        move_timer = 0;
                        last_move_key = K_RIGHT

        # Inputs Contínuos
        if not jogo.game_over and not jogo.animando:
            keys = pygame.key.get_pressed()
            if not keys[K_LEFT] and not keys[K_RIGHT]: last_move_key = None
            if last_move_key and keys[last_move_key]:
                move_timer += dt
                if move_timer > move_delay:
                    if move_timer > move_delay + move_interval:
                        dx = -1 if last_move_key == K_LEFT else 1
                        jogo.mover(dx, 0);
                        move_timer = move_delay

            vel_atual = max(50, velocidade_base - (jogo.nivel * 40))
            limit = 50 if keys[K_DOWN] else vel_atual
            fall_time += dt
            if fall_time >= limit:
                jogo.mover(0, 1);
                fall_time = 0

        elif jogo.animando:
            jogo.update_animacao(dt)

        desenhar_jogo(jogo)
        
        # Se for Contra-Relógio, desenha HUD customizado no topo
        from modes.contraRelogio import ContraRelogioMode, desenhar_texto_relogio
        if isinstance(jogo, ContraRelogioMode):
            # Fundo semi-transparente no topo
            glEnable(GL_BLEND)
            glColor4f(0, 0, 0, 0.6)
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(LARGURA_JOGO, 0)
            glVertex2f(LARGURA_JOGO, 80)
            glVertex2f(0, 80)
            glEnd()
            glDisable(GL_BLEND)
            
            # Tempo grande à direita
            titulo, tempo = jogo.get_info_extra()
            cor_tempo = (255, 0, 0) if titulo == "CORRA!" else (139, 233, 253)
            desenhar_texto_relogio(LARGURA_JOGO - 160, 15, tempo, 32, cor_tempo)
    return 0


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption("Tetris GL Modular")

    sm = SoundManager()
    clock = pygame.time.Clock()

    app_running = True
    musica_tocando = False
    while app_running:
        if not musica_tocando:
            sm.play_music()
            musica_tocando = True

        # O menu gerencia a configuração da janela sozinho
        opcao = loop_menu(clock)

        if opcao == -1: break

        if opcao == 0:  # Infinito
            res = run_infinito(sm, clock)
            if res == -1: break

        elif opcao == 1:  # Duo
            # Duo abre sua própria janela e devolve ao terminar
            res = run_duo_mode(sm)
            if res == -1: break

        elif opcao == 2:  # Contra-Relógio
            res = run_infinito(sm, clock, ContraRelogioMode)
            if res == -1:
                break

    pygame.quit()


if __name__ == "__main__":
    main()
