TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20

LARGURA_JOGO = COLUNAS * TAMANHO_BLOCO
LARGURA_UI = 200
LARGURA_TOTAL = LARGURA_JOGO + LARGURA_UI
ALTURA_JANELA = LINHAS * TAMANHO_BLOCO

CORES = [
    (0.15, 0.16, 0.21),  # 0: Fundo
    (1.00, 0.33, 0.33),  # 1: Red
    (0.31, 0.98, 0.48),  # 2: Green
    (0.74, 0.57, 0.97),  # 3: Purple
    (0.94, 0.98, 0.55),  # 4: Yellow
    (0.54, 0.91, 0.99),  # 5: Cyan
    (1.00, 0.47, 0.77),  # 6: Pink
    (1.00, 0.72, 0.42),   # 7: Orange
    (0.40, 0.40, 0.40)  # 8: LIXO
]
COR_UI_BG = (0.10, 0.10, 0.15)
COR_TEXTO = (248, 248, 242)
COR_DESTAQUE = (139, 233, 253)
COR_FLASH = (1.0, 1.0, 1.0)
COR_JANELA = (0.05, 0.05, 0.05)

FORMAS = [
    [[0, 1], [1, 1], [2, 1], [3, 1]],
    [[0, 1], [1, 1], [2, 1], [2, 0]],
    [[0, 1], [1, 1], [2, 1], [0, 0]],
    [[1, 0], [2, 0], [1, 1], [2, 1]],
    [[1, 1], [2, 1], [0, 0], [1, 0]],
    [[1, 1], [0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [1, 0], [2, 0]],
]