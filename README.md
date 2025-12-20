# 🕹️ Tetris: Releitura jogo Atari Com pyOpenGL

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenGL](https://img.shields.io/badge/OpenGL-%23FFFFFF.svg?style=for-the-badge&logo=opengl&logoColor=5586A4)
![Status](https://img.shields.io/badge/Status-Finalizado-brightgreen?style=for-the-badge)

## 📝 1. Informações Gerais
Fizemos uma releitura do clássico jogo de Atari, **Tetris**, utilizando as bibliotecas **Pygame** e **PyOpenGL**. 

> O projeto foi focado em uma implementação moderna e organizada, priorizando a **Orientação a Objetos (POO)** para garantir a escalabilidade e facilidade de manutenção.

Separamos a lógica do tabuleiro da implementação específica de cada modo de jogo e do gerenciamento de janela/renderização em módulos distintos para evitar código "macarrônico".

---

## 🏗️ 2. Arquitetura e Orientação a Objetos
A estrutura do projeto utiliza conceitos sólidos de **herança** e **encapsulamento**:

*   🧩 **`base.py` (Engine):** Funciona como a "classe pai". Encapsula a matriz do grid, a peça atual e a lógica fundamental (física e movimentação).
*   ♾️ **`infinito.py`:** Herda as funcionalidades da base e implementa regras específicas, como o sistema de níveis e a aceleração progressiva.
*   🛠️ **Modularidade:** Essa separação permite que novos modos de jogo sejam criados apenas estendendo a lógica base, sem precisar reescrever o motor do jogo.

---

## ⚙️ 3. Implementação Técnica e Renderização
Integramos o melhor de duas tecnologias poderosas:

*   🖥️ **PyGame:** Responsável pela criação da janela e captura precisa de eventos de entrada (teclado e mouse) via `pygame.event.get()`.
*   🎨 **PyOpenGL:** Utilizado para a renderização gráfica de alta performance. Usamos primitivas como `glVertex2f` e `GL_QUADS` para desenhar cada bloco e os elementos da interface.

### 📐 Mecânica de Colisão
Implementamos um método **Grid-based**. A função `checar_colisão` realiza uma verificação matemática constante:
1. Valida se as coordenadas futuras da peça coincidem com células ocupadas em `self.grid`.
2. Garante que a peça não ultrapasse os limites laterais ou o "chão" da matriz.

---

## 🏆 4. Progressão e Pontuação
Como o Tetris possui fases implícitas, desenvolvemos sistemas para manter o desafio dinâmico:

*   **📈 Sistema de Níveis:** No modo infinito, a cada **10 linhas** completadas, o nível sobe e a velocidade de queda aumenta.
*   **🔢 Pontuação:** Calculada pelo método `finalizar_linhas`, que multiplica o número de linhas eliminadas simultaneamente pelo nível atual do jogador.
*   **📢 Feedback:** O jogo fornece mensagens visuais de **VICTORY!** ou **GAME OVER** customizadas para cada modo.

---

## 🎮 5. Modos de Jogo
Implementamos três modalidades distintas para diversificar a experiência:

| Modo | Objetivo | Diferencial |
| :--- | :--- | :--- |
| **♾️ Infinito** | Sobreviver e pontuar. | O clássico. A velocidade aumenta conforme o nível sobe. |
| **⏱️ Contra-Relógio** | Pontuar contra o tempo. | Começa com 1min. Cada linha limpa concede **+3 segundos**. |
| **⚔️ Duo (1x1)** | Vencer o oponente. | Multijogador local. Limpar linhas envia "lixo" para a base do adversário. |

---

### 🚀 Como executar
1. Certifique-se de ter o Python instalado.
2. Instale as dependências:
   ```bash
   pip install pygame PyOpenGL numpy
   ```
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```

---
*Desenvolvido como projeto de releitura de clássicos utilizando computação gráfica.*


Por: Cauã Ziotti & Diego Breskovit