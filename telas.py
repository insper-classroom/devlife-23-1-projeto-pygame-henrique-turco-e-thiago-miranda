import pygame
import random
from sprites import *
from constantes import *


class Jogo:
    """
    Classe utilizada para realizar o loop geral do jogo
    ...

    Atributos
    ---------
    fundo : objeto Surface
        arte do fundo da tela inicial
    fundo_modo_classico : objeto Surface
        arte do fundo da tela do modo clássico
    fundo_modo_rapido : objeto Surface
        arte do fundo da tela do modo rápido
    fundo_modo_escuro : objeto Surface
        arte do fundo da tela do modo escuro
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TÍTULO)
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        # Artes para fundo das telas
        self.fundo = pygame.image.load('assets/snd/img/img/Inicio-Pattern-Pursuit.png')
        self.fundo_modo_classico = pygame.image.load('assets/snd/img/img/Modo-Classico.png')
        self.fundo_modo_rapido = pygame.image.load('assets/snd/img/img/Modo-Rápido.png')
        self.fundo_modo_escuro = pygame.image.load('assets/snd/img/img/Modo-Escuro.png')
        # Música de fundo
        pygame.mixer_music.load('assets/snd/img/Snd/390655__mvrasseli__atari-game-masters-loop.wav')
        pygame.mixer_music.play(loops=-1)

    # Loop
    def roda(self):
        self.desenha()
        pygame.display.update()


class TelaInicial(Jogo):
    """
    Classe utilizada para representar a Tela de Início do jogo
    ...

    Atributos
    ---------
    rect_modo_classico : objeto Rect
        retângulo criado sobre a arte do botão do modo clássico
    rect_modo_rapido : objeto Rect
        retângulo criado sobre a arte do botão do modo rápido
    rect_modo_escuro : objeto Rect
        retângulo criado sobre a arte do botão do modo escuro
    rect_sair : objeto Rect
        retângulo criado sobre a arte do botão de sair do jogo
    """

    def __init__(self):
        super().__init__()
        # Botões dos modos e sair
        self.rect_modo_classico = pygame.Rect(235, 190, 330, 90)
        self.rect_modo_rapido = pygame.Rect(235, 290, 330, 90)
        self.rect_modo_escuro = pygame.Rect(235, 390, 330, 90)
        self.rect_sair = pygame.Rect(235, 490, 330, 90)

    # Desenha a arte da tela inicial com os botões de seleção de modo de jogo e sair
    def desenha(self):
        self.window.blit(self.fundo, (0, 0)) # Desenha a arte da tela inicial
        pygame.display.update()

    # Atualiza a tela inicial e retorna a tela selecionada pelo jogador
    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            # Seleção de modos de jogo e sair
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_modo_classico): # Tela Modo Clássico
                    return TelaClassico()
                elif mouse_rect.colliderect(self.rect_modo_rapido): # Tela Modo Rápido
                    return TelaRapido()
                elif mouse_rect.colliderect(self.rect_modo_escuro): # Tela Modo Escuro
                    return TelaEscuro()
                elif mouse_rect.colliderect(self.rect_sair): # Tela Sair
                    pygame.quit()
                    quit()
        return self # Retorna a própria tela inicial


class TelaClassico(Jogo):
    """
    Classe utilizada para representar a Tela do Modo Clássico
    ...

    Atributos
    ---------
    quadrados : lista
        lista de quadrados escuros que estão desenhados em cima dos mais claros, com as dimensões, posições e cores
    quadrados_claros : lista
        lista de quadrados claros que estão desenhados em baixo dos mais escuros, com as dimensões, posições e cores. Já contendo a função de desenhá-los no arquivo sprites.py
    sorteia : booleano
        booleano que indica se o jogo está sorteando / pode sortear, uma nova cor para a sequência
    mostra_quadrado : booleano
        booleano que indica se o jogo deve mostrar os quadrados escuros em cima dos claros ou não
    validacao_jogada : booleano
        valida cada jogada do jogador, se ele acertou ou errou
    cores_sorteadas e retangulos: listas
        listas que guardam as cores sorteadas e os retângulos dos quadrados escuros para colisão com clique do jogador, respectivamente
    retangulos : lista
        lista que guarda os retângulos dos quadrados escuros para colisão com clique do jogador
    indice_quadrado : int
        verifica na lista das cores sorteadas se o índice de cada quadrado representa um quadrado que deve ser mostrado na tela ou ação de piscar
    tempo_start : int
        tempo inicial do jogo para realizar o pisque em intervalos de x segundos estipulados pela função tempo_entre_pisques()
    som0, som1, som2, som3 : pygame.mixer.Sound
        sons tocados para cada interação com os quadrados, seja o clique do jogador ou o pisque
    """
    
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_CLASSICO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [AZUL_ESCURO, AMARELO_ESCURO, VERDE_ESCURO, VERMELHO_ESCURO]

        # Quadrados escuros
        self.quadrados = [
            [210, 180, LARGURA_RECT, ALTURA_RECT, AZUL_ESCURO],
            [410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO_ESCURO],
            [210, 380, LARGURA_RECT, ALTURA_RECT, VERDE_ESCURO],
            [410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO_ESCURO]
        ]

        # Quadrados mais claros para "piscar"
        self.quadrados_claros = [
            QuadradoClaro(210, 180, LARGURA_RECT, ALTURA_RECT, AZUL),
            QuadradoClaro(410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO),
            QuadradoClaro(210, 380, LARGURA_RECT, ALTURA_RECT, VERDE),
            QuadradoClaro(410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO) 
        ]

        # Booleanos
        self.sorteia = True
        self.mostra_quadrado = True
        self.validacao_jogada = False
        #Listas
        self.cores_sorteadas = []
        self.retangulos = []
        self.sequencia_jogador = []
        # Valores
        self.indice_quadrado = 0
        self.score = 0
        self.highscore = self.get_high_score_classico()
        self.tempo_start = pygame.time.get_ticks()
        # Sons
        self.som0 = pygame.mixer.Sound('assets/snd/img/snd/00.wav')
        self.som1 = pygame.mixer.Sound('assets/snd/img/snd/01.wav')
        self.som2 = pygame.mixer.Sound('assets/snd/img/snd/02.wav')
        self.som3 = pygame.mixer.Sound('assets/snd/img/snd/03.wav')
        self.som_game_over = pygame.mixer.Sound('assets\snd\img\Snd\mixkit-funny-game-over-2878.wav')
        pygame.mixer.music.set_volume(0.2)

    # Função para ler o High Score
    def get_high_score_classico(self):
        with open("high_score_classico.txt", "r") as file:
            score = file.read()
        return int(score)

    # Função para salvar o High Score e se for o caso, substituir o antigo
    def save_score(self):
        with open("high_score_classico.txt", "w") as file:
            if self.score > self.highscore:
                file.write(str(self.score))
            else:
                file.write(str(self.highscore))

    # Função para sortear a sequência de cores
    def sorteia_quadrados(self):
        if self.sorteia:
            quadrado_sorteado = random.choice(self.quadrados) 
            self.cores_sorteadas.append(quadrado_sorteado[4]) # self.quadrados[4] = cor

    def desenha(self):
        self.window.blit(self.fundo_modo_classico, (0, 0))
        # Desenha Score e High Score
        Pontuacao(270, 150, f"Score: {str(self.score)}").desenha(self.window)
        Pontuacao(440, 150, f"High Score: {str(self.highscore)}").desenha(self.window)

        # Desenha os quadrados claros (atrás dos escuros)
        for quadrado_claro in self.quadrados_claros:
            quadrado_claro.desenha(self.window)

        for i in range(4): # Cria os retângulos para verificação do clique
            r = pygame.Rect(self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3])
            self.retangulos.append(r) 
            if self.mostra_quadrado or self.indice_quadrado >= len(self.cores_sorteadas) or self.cores[i] != self.cores_sorteadas[self.indice_quadrado]:
                pygame.draw.rect(self.window, self.cores[i], (self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3]))
            else:
                if self.quadrados[i][4] == AZUL_ESCURO:
                    self.som0.play()
                elif self.quadrados[i][4] == AMARELO_ESCURO:
                    self.som1.play()
                elif self.quadrados[i][4] == VERDE_ESCURO:
                    self.som2.play()
                elif self.quadrados[i][4] == VERMELHO_ESCURO:
                    self.som3.play()
    
    # Função para fazer os quadrados "piscarem", criar a sequência do jogador e verificar se a sequência está correta
    def update(self):
        self.tempo_entre_pisques()
        if self.sorteia:
            self.sorteia_quadrados()
            self.sorteia = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN :
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                # Cria a sequência do jogador 
                if mouse_rect.colliderect(self.retangulos[0]):
                    self.som0.play()
                    self.sequencia_jogador.append(self.cores[0])
                elif mouse_rect.colliderect(self.retangulos[1]):
                    self.som1.play()
                    self.sequencia_jogador.append(self.cores[1])
                elif mouse_rect.colliderect(self.retangulos[2]):
                    self.som2.play()
                    self.sequencia_jogador.append(self.cores[2])
                elif mouse_rect.colliderect(self.retangulos[3]):
                    self.som3.play()
                    self.sequencia_jogador.append(self.cores[3])
                # Verifica se o jogador acertou a sequência
                for i in range(len(self.sequencia_jogador)):
                    if self.sequencia_jogador[i] == self.cores_sorteadas[i]:
                        self.validacao_jogada = True
                    else: # Caso o jogador erre a sequência, tela Game Over é chamada
                        self.save_score()
                        self.som_game_over.play()
                        return TelaGameOverClassico()   
                if self.sequencia_jogador == self.cores_sorteadas: # Jogador acertou a sequência
                    self.score += 1
                    self.indice_quadrado = 0
                    self.sorteia = True
                    self.pausa_entre_rodadas(2)
            if len(self.sequencia_jogador) == len(self.cores_sorteadas): # Quando acaba a rodada a sequência do jogador é reinicializada
                self.sequencia_jogador = []
                self.tempo_start = pygame.time.get_ticks()
        return self 
    
    # Função que controla o tempo de exibição dos quadrados
    def tempo_entre_pisques(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 650:
            self.mostra_quadrado = not self.mostra_quadrado
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_quadrado:
                self.indice_quadrado += 1
    
    # Função que pausa o jogo entre as rodadas (solução criada com ajuda do ChatGPT)
    def pausa_entre_rodadas(self, seconds):
        pygame.time.set_timer(pygame.USEREVENT, seconds * 1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    return


class TelaRapido(Jogo):
    """
    Classe utilizada para representar a Tela do Modo Rápido
    ...

    Atributos
    ---------
    quadrados : lista
        lista de quadrados escuros que estão desenhados em cima dos mais claros, com as dimensões, posições e cores
    quadrados_claros : lista
        lista de quadrados claros que estão desenhados em baixo dos mais escuros, com as dimensões, posições e cores. Já contendo a função de desenhá-los no arquivo sprites.py
    sorteia : booleano
        booleano que indica se o jogo está sorteando / pode sortear, uma nova cor para a sequência
    mostra_quadrado : booleano
        booleano que indica se o jogo deve mostrar os quadrados escuros em cima dos claros ou não
    validacao_jogada : booleano
        valida cada jogada do jogador, se ele acertou ou errou
    cores_sorteadas e retangulos: listas
        listas que guardam as cores sorteadas e os retângulos dos quadrados escuros para colisão com clique do jogador, respectivamente
    retangulos : lista
        lista que guarda os retângulos dos quadrados escuros para colisão com clique do jogador
    indice_quadrado : int
        verifica na lista das cores sorteadas se o índice de cada quadrado representa um quadrado que deve ser mostrado na tela ou ação de piscar
    tempo_start : int
        tempo inicial do jogo para realizar o pisque em intervalos de x segundos estipulados pela função tempo_entre_pisques(), nesse caso é um tempo menor comparado aos outros dois modos
    som0, som1, som2, som3 : pygame.mixer.Sound
        sons tocados para cada interação com os quadrados, seja o clique do jogador ou o pisque
    """
    
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_RÁPIDO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [AZUL_ESCURO, AMARELO_ESCURO, VERDE_ESCURO, VERMELHO_ESCURO]

        # Quadrados escuros
        self.quadrados = [
            [210, 180, LARGURA_RECT, ALTURA_RECT, AZUL_ESCURO],
            [410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO_ESCURO],
            [210, 380, LARGURA_RECT, ALTURA_RECT, VERDE_ESCURO],
            [410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO_ESCURO]
        ]

        # Quadrados mais claros para "piscar"
        self.quadrados_claros = [
            QuadradoClaro(210, 180, LARGURA_RECT, ALTURA_RECT, AZUL),
            QuadradoClaro(410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO),
            QuadradoClaro(210, 380, LARGURA_RECT, ALTURA_RECT, VERDE),
            QuadradoClaro(410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO) 
        ]

        # Booleanos
        self.sorteia = True
        self.mostra_quadrado = True
        self.validacao_jogada = False
        # Listas
        self.cores_sorteadas = []
        self.retangulos = []
        self.sequencia_jogador = []
        # Valores
        self.indice_quadrado = 0
        self.score = 0
        self.highscore = self.get_high_score_rapido()
        self.tempo_start = pygame.time.get_ticks()
        # Sons
        self.som0 = pygame.mixer.Sound('assets/snd/img/snd/00.wav')
        self.som1 = pygame.mixer.Sound('assets/snd/img/snd/01.wav')
        self.som2 = pygame.mixer.Sound('assets/snd/img/snd/02.wav')
        self.som3 = pygame.mixer.Sound('assets/snd/img/snd/03.wav')
        self.som_game_over = pygame.mixer.Sound('assets\snd\img\Snd\mixkit-funny-game-over-2878.wav')
        pygame.mixer.music.set_volume(0.2)

    # Função para ler High Score
    def get_high_score_rapido(self):
        with open("high_score_rapido.txt", "r") as file:
            score = file.read()
        return int(score)

    # Função para salvar o High Score e se for o caso, substituir o antigo
    def save_score(self):
        with open("high_score_rapido.txt", "w") as file:
            if self.score > self.highscore:
                file.write(str(self.score))
            else:
                file.write(str(self.highscore))

    # Função para sortear a sequência de cores
    def sorteia_quadrados(self):
        if self.sorteia:
            quadrado_sorteado = random.choice(self.quadrados) 
            self.cores_sorteadas.append(quadrado_sorteado[4]) # self.quadrados[4] = cor
            
    def desenha(self):
        self.window.blit(self.fundo_modo_rapido, (0, 0))
        # Desenha Score e High Score 
        Pontuacao(270, 150, f"Score: {str(self.score)}").desenha(self.window)
        Pontuacao(440, 150, f"High Score: {str(self.highscore)}").desenha(self.window)

        # Desenha os quadrados claros (atrás dos escuros)
        for quadrado_claro in self.quadrados_claros:
            quadrado_claro.desenha(self.window)

        for i in range(4): # Cria os retângulos para verificação do clique
            r = pygame.Rect(self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3])
            self.retangulos.append(r) 
            if self.mostra_quadrado or self.indice_quadrado >= len(self.cores_sorteadas) or self.cores[i] != self.cores_sorteadas[self.indice_quadrado]:
                pygame.draw.rect(self.window, self.cores[i], (self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3]))
            else:
                if self.quadrados[i][4] == AZUL_ESCURO:
                    self.som0.play()
                elif self.quadrados[i][4] == AMARELO_ESCURO:
                    self.som1.play()
                elif self.quadrados[i][4] == VERDE_ESCURO:
                    self.som2.play()
                elif self.quadrados[i][4] == VERMELHO_ESCURO:
                    self.som3.play()

    # Função para fazer os quadrados "piscarem", criar a sequência do jogador e verificar se a sequência está correta
    def update(self):
        self.tempo_entre_pisques()
        if self.sorteia:
            self.sorteia_quadrados()
            self.sorteia = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                # Cria a sequência do jogador 
                if mouse_rect.colliderect(self.retangulos[0]):
                    self.sequencia_jogador.append(self.cores[0])
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[1]):
                    self.sequencia_jogador.append(self.cores[1])
                    self.som1.play()
                elif mouse_rect.colliderect(self.retangulos[2]):
                    self.sequencia_jogador.append(self.cores[2])
                    self.som2.play()
                elif mouse_rect.colliderect(self.retangulos[3]):
                    self.sequencia_jogador.append(self.cores[3])
                    self.som3.play()
                # Verifica se o jogador acertou a sequência
                for i in range(len(self.sequencia_jogador)):
                    if self.sequencia_jogador[i] == self.cores_sorteadas[i]:
                        self.validacao_jogada = True
                    else: # Caso o jogador erre a sequência, tela Game Over é chamada
                        self.save_score()
                        self.som_game_over.play()
                        return TelaGameOverRapido()
                if self.sequencia_jogador == self.cores_sorteadas: # Jogador acertou a sequência
                    self.sorteia = True
                    self.score += 1
                    self.indice_quadrado = 0
                    self.pausa_entre_rodadas(1)
            if len(self.sequencia_jogador) == len(self.cores_sorteadas): # Quando acaba a rodada a sequência do jogador é reinicializada
                self.sequencia_jogador = []
                self.tempo_start = pygame.time.get_ticks() 
        return self 
    
    # Função que controla o tempo de exibição dos quadrados
    def tempo_entre_pisques(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 280:
            self.mostra_quadrado = not self.mostra_quadrado
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_quadrado:
                self.indice_quadrado += 1
    
    # Função que pausa o jogo entre as rodadas (solução criada com ajuda do ChatGPT)
    def pausa_entre_rodadas(self, seconds):
        pygame.time.set_timer(pygame.USEREVENT, seconds * 1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    return
   

class TelaEscuro(Jogo):
    """
    Classe utilizada para representar a Tela do Modo Rápido
    ...

    Atributos
    ---------
    quadrados : lista
        lista de quadrados escuros que estão desenhados em cima dos mais claros, com as dimensões, posições e cores
    quadrados_claros : lista
        lista de quadrados claros que estão desenhados em baixo dos mais escuros, com as dimensões, posições e cores. Já contendo a função de desenhá-los no arquivo sprites.py
    sorteia : booleano
        booleano que indica se o jogo está sorteando / pode sortear, uma nova cor para a sequência
    mostra_quadrado : booleano
        booleano que indica se o jogo deve mostrar os quadrados escuros em cima dos claros ou não
    validacao_jogada : booleano
        valida cada jogada do jogador, se ele acertou ou errou
    cores_sorteadas e retangulos: listas
        listas que guardam as cores sorteadas e os retângulos dos quadrados escuros para colisão com clique do jogador, respectivamente
    retangulos : lista
        lista que guarda os retângulos dos quadrados escuros para colisão com clique do jogador
    indice_quadrado : int
        verifica na lista das cores sorteadas se o índice de cada quadrado representa um quadrado que deve ser mostrado na tela ou ação de piscar
    tempo_start : int
        tempo inicial do jogo para realizar o pisque em intervalos de x segundos estipulados pela função tempo_entre_pisques(), esse tempo é igual o tempo do modo clássico
    som0 : pygame.mixer.Sound
        som único para todos os quadrados
    """

    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_ESCURO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [CINZA1, CINZA2, CINZA3, CINZA4]

        # Quadrados escuros
        self.quadrados = [
            [210, 180, LARGURA_RECT, ALTURA_RECT, CINZA1],
            [410, 180, LARGURA_RECT, ALTURA_RECT, CINZA2],
            [210, 380, LARGURA_RECT, ALTURA_RECT, CINZA3],
            [410, 380, LARGURA_RECT, ALTURA_RECT, CINZA4]
        ]

        # Quadrados mais claros para "piscar"
        self.quadrados_claros = [
            QuadradoClaro(210, 180, LARGURA_RECT, ALTURA_RECT, AZUL),
            QuadradoClaro(410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO),
            QuadradoClaro(210, 380, LARGURA_RECT, ALTURA_RECT, VERDE),
            QuadradoClaro(410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO) 
        ]

        # Booleanos
        self.sorteia = True
        self.mostra_quadrado = True
        self.validacao_jogada = False
        # Listas
        self.cores_sorteadas = []
        self.retangulos = []
        self.sequencia_jogador = []
        # Valores
        self.indice_quadrado = 0
        self.score = 0
        self.highscore = self.get_high_score_escuro()
        self.tempo_start = pygame.time.get_ticks()
        # Sons
        self.som0 = pygame.mixer.Sound('assets/snd/img/snd/00.wav')
        self.som_game_over = pygame.mixer.Sound('assets\snd\img\Snd\mixkit-funny-game-over-2878.wav')
        pygame.mixer.music.set_volume(0.2)

    # Função para ler o High Score
    def get_high_score_escuro(self):
        with open("high_score_escuro.txt", "r") as file:
            score = file.read()
        return int(score)

    # Função para salvar o High Score e se for o caso, substituir o antigo
    def save_score(self):
        with open("high_score_escuro.txt", "w") as file:
            if self.score > self.highscore:
                file.write(str(self.score))
            else:
                file.write(str(self.highscore))

    # Função para sortear a sequência de cores
    def sorteia_quadrados(self):
        if self.sorteia:
            quadrado_sorteado = random.choice(self.quadrados) 
            self.cores_sorteadas.append(quadrado_sorteado[4]) # self.quadrados[4] = cor

    def desenha(self):
        self.window.blit(self.fundo_modo_escuro, (0, 0))
        # Desenha Score e High Score
        Pontuacao(270, 150, f"Score: {str(self.score)}").desenha(self.window)
        Pontuacao(440, 150, f"High Score: {str(self.highscore)}").desenha(self.window)

        # Desenha os quadrados claros (atrás dos escuros)
        for quadrado_claro in self.quadrados_claros:
            quadrado_claro.desenha(self.window)

        for i in range(4): # Cria os retângulos para verificação do clique
            r = pygame.Rect(self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3])
            self.retangulos.append(r) 
    
            if self.mostra_quadrado or self.indice_quadrado >= len(self.cores_sorteadas) or self.cores[i] != self.cores_sorteadas[self.indice_quadrado]:
                pygame.draw.rect(self.window, self.cores[i], (self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3]))
            else:
                if self.quadrados[i][4] == CINZA1:
                    self.som0.play()
                elif self.quadrados[i][4] == CINZA2:
                    self.som0.play()
                elif self.quadrados[i][4] == CINZA3:
                    self.som0.play()
                elif self.quadrados[i][4] == CINZA4:
                    self.som0.play()

    # Função para fazer os quadrados "piscarem", criar a sequência do jogador e verificar se a sequência está correta
    def update(self):
        self.tempo_entre_pisques()
        if self.sorteia:
            self.sorteia_quadrados()
            self.sorteia = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                # Cria a sequência do jogador 
                if mouse_rect.colliderect(self.retangulos[0]):
                    self.sequencia_jogador.append(self.cores[0])
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[1]):
                    self.sequencia_jogador.append(self.cores[1])
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[2]):
                    self.sequencia_jogador.append(self.cores[2])
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[3]):
                    self.sequencia_jogador.append(self.cores[3])
                    self.som0.play()
                # Verifica se o jogador acertou a sequência
                for i in range(len(self.sequencia_jogador)):
                    if self.sequencia_jogador[i] == self.cores_sorteadas[i]:
                        self.validacao_jogada = True
                    else: # Caso o jogador erre a sequência, tela Game Over é chamada
                        self.save_score()
                        self.som_game_over.play()
                        return TelaGameOverEscuro()
                if self.sequencia_jogador == self.cores_sorteadas: # Jogador acertou a sequência
                    self.sorteia = True
                    self.score += 1
                    self.indice_quadrado = 0
                    self.pausa_entre_rodadas(2)
            if len(self.sequencia_jogador) == len(self.cores_sorteadas): # Quando acaba a rodada a sequência do jogador é reinicializada
                self.sequencia_jogador = []
                self.tempo_start = pygame.time.get_ticks()
        return self 
    
    # Função que controla o tempo de exibição dos quadrados
    def tempo_entre_pisques(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 650:
            self.mostra_quadrado = not self.mostra_quadrado
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_quadrado:
                self.indice_quadrado += 1
    
    # Função que pausa o jogo entre as rodadas (solução criada com ajuda do ChatGPT)
    def pausa_entre_rodadas(self, seconds):
        pygame.time.set_timer(pygame.USEREVENT, seconds * 1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    return


class TelaGameOverClassico(Jogo):
    """
    Classe utilizada para representar a Tela de Game Over que retorna (botão tentar de novo) para o Modo Clássico
    ...

    Atributos
    ---------
    rect_tentar_de_novo : objeto Rect
        retângulo criado sobre a arte do botão de tentar de novo que retorna a tela do Modo Clássico
    rect_voltar_inicio : objeto Rect
        retângulo criado sobre a arte do botão de voltar para a tela inicial do jogo
    rect_sair : objeto Rect
        retângulo criado sobre a arte do botão de sair do jogo
    """

    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('assets/snd/img/img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    # Função para verificação dos cliques do mouse nos botões de seleção de telas
    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Seleção dos botões
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo): # Tentar de novo volta para o Modo Clássico
                    return TelaClassico()                    
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self
    

class TelaGameOverRapido(Jogo):
    """
    Classe utilizada para representar a Tela de Game Over que retorna (botão tentar de novo) para o Modo Rápido
    ...

    Atributos
    ---------
    rect_tentar_de_novo : objeto Rect
        retângulo criado sobre a arte do botão de tentar de novo que retorna a tela do Modo Rápido
    rect_voltar_inicio : objeto Rect
        retângulo criado sobre a arte do botão de voltar para a tela inicial do jogo
    rect_sair : objeto Rect
        retângulo criado sobre a arte do botão de sair do jogo
    """

    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('assets/snd/img/img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    # Função para verificação dos cliques do mouse nos botões de seleção de telas
    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Seleção dos botões
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo): # Tentar de novo volta para o Modo Rápido
                    return TelaRapido()                    
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self


class TelaGameOverEscuro(Jogo):
    """
    Classe utilizada para representar a Tela de Game Over que retorna (botão tentar de novo) para o Modo Escuro
    ...

    Atributos
    ---------
    rect_tentar_de_novo : objeto Rect
        retângulo criado sobre a arte do botão de tentar de novo que retorna a tela do Modo Escuro
    rect_voltar_inicio : objeto Rect
        retângulo criado sobre a arte do botão de voltar para a tela inicial do jogo
    rect_sair : objeto Rect
        retângulo criado sobre a arte do botão de sair do jogo
    """

    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('assets/snd/img/img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    # Função para verificação dos cliques do mouse nos botões de seleção de telas
    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Seleção dos botões
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo): # Tentar de novo volta para o Modo Escuro
                    return TelaEscuro()                    
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self