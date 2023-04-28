import pygame
import random
from sprites import *
from constantes import *

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TÍTULO)
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        self.fundo = pygame.image.load('assets/snd/img/Inicio-Pattern-Pursuit.png')
        self.fundo_modo_classico = pygame.image.load('assets/snd/img/Modo-Classico.png')
        self.fundo_modo_rapido = pygame.image.load('assets/snd/img/Modo-Rápido.png')
        self.fundo_modo_escuro = pygame.image.load('assets/snd/img/Modo-Escuro.png')
        pygame.mixer_music.load('assets/snd/390655__mvrasseli__atari-game-masters-loop.wav')
        pygame.mixer_music.play(loops=-1)

    def roda(self):
        self.desenha()
        pygame.display.update()

class TelaInicial(Jogo):
    def __init__(self):
        super().__init__()
        self.rect_modo_classico = pygame.Rect(235, 190, 330, 90)
        self.rect_modo_rapido = pygame.Rect(235, 290, 330, 90)
        self.rect_modo_escuro = pygame.Rect(235, 390, 330, 90)
        self.rect_sair = pygame.Rect(235, 490, 330, 90)

    def desenha(self):
        self.window.blit(self.fundo, (0, 0))
        pygame.display.update()

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_modo_classico):
                    return TelaClassico()
                elif mouse_rect.colliderect(self.rect_modo_rapido):
                    return TelaRapido()
                elif mouse_rect.colliderect(self.rect_modo_escuro):
                    return TelaEscuro()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self # Retorna a própria tela inicial

class TelaClassico(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_CLASSICO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [AZUL_ESCURO, AMARELO_ESCURO, VERDE_ESCURO, VERMELHO_ESCURO]

        self.quadrados = [
            [210, 180, LARGURA_RECT, ALTURA_RECT, AZUL_ESCURO],
            [410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO_ESCURO],
            [210, 380, LARGURA_RECT, ALTURA_RECT, VERDE_ESCURO],
            [410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO_ESCURO]
        ]

        self.quadrados_claros = [
            QuadradoClaro(210, 180, LARGURA_RECT, ALTURA_RECT, AZUL),
            QuadradoClaro(410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO),
            QuadradoClaro(210, 380, LARGURA_RECT, ALTURA_RECT, VERDE),
            QuadradoClaro(410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO) 
        ]

        self.sorteia = True
        self.mostra_quadrado = True
        self.cores_sorteadas = []
        self.sequencia_jogador = []
        self.rect_sorteados = []
        self.retangulos = []
        self.tempo_start = pygame.time.get_ticks()
        self.indice_quadrado = 0
        self.verificação_individual = 0
        self.validacao_jogada = False
        self.score = 0
        self.highscore = self.get_high_score_classico()
        self.som0 = pygame.mixer.Sound('assets/snd/00.wav')
        self.som1 = pygame.mixer.Sound('assets/snd/01.wav')
        self.som2 = pygame.mixer.Sound('assets/snd/02.wav')
        self.som3 = pygame.mixer.Sound('assets/snd/03.wav')
        pygame.mixer.music.set_volume(0.2)

    def get_high_score_classico(self):
        with open("high_score_classico.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open("high_score_classico.txt", "w") as file:
            if self.score > self.highscore:
                file.write(str(self.score))
            else:
                file.write(str(self.highscore))

    def sorteia_quadrados(self):
        if self.sorteia:
            quadrado_sorteado = random.choice(self.quadrados) 
            self.cores_sorteadas.append(quadrado_sorteado[4]) # self.quadrados[4] = cor
            self.rect_sorteados.append([quadrado_sorteado[0], quadrado_sorteado[1], quadrado_sorteado[2], quadrado_sorteado[3]]) # self.quadrados[0:4]

    def desenha(self):
        self.window.blit(self.fundo_modo_classico, (0, 0))
        Pontuacao(270, 150, f"Score: {str(self.score)}").desenha(self.window)
        Pontuacao(440, 150, f"High Score: {str(self.highscore)}").desenha(self.window)

        for quadrado_claro in self.quadrados_claros: # Desenha os quadrados claros
            quadrado_claro.desenha(self.window)

        for i in range(4): # Cria os retângulos para verificação do clique
            r = pygame.Rect(self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3])
            self.retangulos.append(r) 
    
            if self.mostra_quadrado or self.indice_quadrado >= len(self.cores_sorteadas) or self.cores[i] != self.cores_sorteadas[self.indice_quadrado]:
                pygame.draw.rect(self.window, self.cores[i], (self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3]))

    def update(self):
        self.tempo()
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
                
                if mouse_rect.colliderect(self.retangulos[0]):
                    self.sequencia_jogador.append(self.cores[0])
                    self.verificação_individual += 1
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[1]):
                    self.sequencia_jogador.append(self.cores[1])
                    self.verificação_individual += 1
                    self.som1.play()
                elif mouse_rect.colliderect(self.retangulos[2]):
                    self.sequencia_jogador.append(self.cores[2])
                    self.verificação_individual += 1
                    self.som2.play()
                elif mouse_rect.colliderect(self.retangulos[3]):
                    self.sequencia_jogador.append(self.cores[3])
                    self.verificação_individual += 1
                    self.som3.play()
                
                for i in range(len(self.sequencia_jogador)):
                    if self.sequencia_jogador[i] == self.cores_sorteadas[i]:
                        self.validacao_jogada = True
                    else: # Caso o jogador erre a sequência
                        self.save_score()
                        return TelaGameOverClassico()
                    
                if self.sequencia_jogador == self.cores_sorteadas:
                    self.sorteia = True
                    self.score += 1
                    self.indice_quadrado = 0

            if len(self.sequencia_jogador) == len(self.cores_sorteadas):
                self.sequencia_jogador = []
            
        return self 
    
    def tempo(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 650:
            self.mostra_quadrado = not self.mostra_quadrado
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_quadrado:
                self.indice_quadrado += 1
  
class TelaRapido(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_RÁPIDO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [AZUL_ESCURO, AMARELO_ESCURO, VERDE_ESCURO, VERMELHO_ESCURO]

        self.quadrados = [
            [210, 180, LARGURA_RECT, ALTURA_RECT, AZUL_ESCURO],
            [410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO_ESCURO],
            [210, 380, LARGURA_RECT, ALTURA_RECT, VERDE_ESCURO],
            [410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO_ESCURO]
        ]

        self.quadrados_claros = [
            QuadradoClaro(210, 180, LARGURA_RECT, ALTURA_RECT, AZUL),
            QuadradoClaro(410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO),
            QuadradoClaro(210, 380, LARGURA_RECT, ALTURA_RECT, VERDE),
            QuadradoClaro(410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO) 
        ]

        self.sorteia = True
        self.mostra_quadrado = True
        self.cores_sorteadas = []
        self.sequencia_jogador = []
        self.rect_sorteados = []
        self.retangulos = []
        self.tempo_start = pygame.time.get_ticks()
        self.indice_quadrado = 0
        self.verificação_individual = 0
        self.validacao_jogada = False
        self.score = 0
        self.highscore = self.get_high_score_rapido()
        self.som0 = pygame.mixer.Sound('assets/snd/00.wav')
        self.som1 = pygame.mixer.Sound('assets/snd/01.wav')
        self.som2 = pygame.mixer.Sound('assets/snd/02.wav')
        self.som3 = pygame.mixer.Sound('assets/snd/03.wav')
        pygame.mixer.music.set_volume(0.2)

    def get_high_score_rapido(self):
        with open("high_score_rapido.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open("high_score_rapido.txt", "w") as file:
            if self.score > self.highscore:
                file.write(str(self.score))
            else:
                file.write(str(self.highscore))

    def sorteia_quadrados(self):
        if self.sorteia:
            quadrado_sorteado = random.choice(self.quadrados) 
            self.cores_sorteadas.append(quadrado_sorteado[4]) # self.quadrados[4] = cor
            self.rect_sorteados.append([quadrado_sorteado[0], quadrado_sorteado[1], quadrado_sorteado[2], quadrado_sorteado[3]]) # self.quadrados[0:4]

    def desenha(self):
        self.window.blit(self.fundo_modo_rapido, (0, 0))
        Pontuacao(270, 150, f"Score: {str(self.score)}").desenha(self.window)
        Pontuacao(440, 150, f"High Score: {str(self.highscore)}").desenha(self.window)

        for quadrado_claro in self.quadrados_claros: # Desenha os quadrados claros
            quadrado_claro.desenha(self.window)

        for i in range(4): # Cria os retângulos para verificação do clique
            r = pygame.Rect(self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3])
            self.retangulos.append(r) 
    
            if self.mostra_quadrado or self.indice_quadrado >= len(self.cores_sorteadas) or self.cores[i] != self.cores_sorteadas[self.indice_quadrado]:
                pygame.draw.rect(self.window, self.cores[i], (self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3]))

    def update(self):
        self.tempo()
        if self.sorteia:
            self.sorteia_quadrados()
            self.sorteia = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                
                if mouse_rect.colliderect(self.retangulos[0]):
                    self.sequencia_jogador.append(self.cores[0])
                    self.verificação_individual += 1
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[1]):
                    self.sequencia_jogador.append(self.cores[1])
                    self.verificação_individual += 1
                    self.som1.play()
                elif mouse_rect.colliderect(self.retangulos[2]):
                    self.sequencia_jogador.append(self.cores[2])
                    self.verificação_individual += 1
                    self.som2.play()
                elif mouse_rect.colliderect(self.retangulos[3]):
                    self.sequencia_jogador.append(self.cores[3])
                    self.verificação_individual += 1
                    self.som3.play()
                
                for i in range(len(self.sequencia_jogador)):
                    if self.sequencia_jogador[i] == self.cores_sorteadas[i]:
                        self.validacao_jogada = True
                    else: # Caso o jogador erre a sequência
                        self.save_score()
                        return TelaGameOverRapido()
                    
                if self.sequencia_jogador == self.cores_sorteadas:
                    self.sorteia = True
                    self.score += 1
                    self.indice_quadrado = 0

            if len(self.sequencia_jogador) == len(self.cores_sorteadas):
                self.sequencia_jogador = []
            
        return self 
    
    def tempo(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 320:
            self.mostra_quadrado = not self.mostra_quadrado
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_quadrado:
                self.indice_quadrado += 1
# Tempo rápido não está funcionando, a sequencia é mostrada na mesma velocidade que no modo classico    

class TelaEscuro(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(MODO_ESCURO)
        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [CINZA1, CINZA2, CINZA3, CINZA4]

        self.quadrados = [
            [210, 180, LARGURA_RECT, ALTURA_RECT, CINZA1],
            [410, 180, LARGURA_RECT, ALTURA_RECT, CINZA2],
            [210, 380, LARGURA_RECT, ALTURA_RECT, CINZA3],
            [410, 380, LARGURA_RECT, ALTURA_RECT, CINZA4]
        ]

        self.quadrados_claros = [
            QuadradoClaro(210, 180, LARGURA_RECT, ALTURA_RECT, AZUL),
            QuadradoClaro(410, 180, LARGURA_RECT, ALTURA_RECT, AMARELO),
            QuadradoClaro(210, 380, LARGURA_RECT, ALTURA_RECT, VERDE),
            QuadradoClaro(410, 380, LARGURA_RECT, ALTURA_RECT, VERMELHO) 
        ]

        self.sorteia = True
        self.mostra_quadrado = True
        self.cores_sorteadas = []
        self.sequencia_jogador = []
        self.rect_sorteados = []
        self.retangulos = []
        self.tempo_start = pygame.time.get_ticks()
        self.indice_quadrado = 0
        self.verificação_individual = 0
        self.validacao_jogada = False
        self.score = 0
        self.highscore = self.get_high_score_escuro()
        self.som0 = pygame.mixer.Sound('assets/snd/00.wav')
        self.som1 = pygame.mixer.Sound('assets/snd/01.wav')
        self.som2 = pygame.mixer.Sound('assets/snd/02.wav')
        self.som3 = pygame.mixer.Sound('assets/snd/03.wav')
        pygame.mixer.music.set_volume(0.2)

    def get_high_score_escuro(self):
        with open("high_score_escuro.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open("high_score_escuro.txt", "w") as file:
            if self.score > self.highscore:
                file.write(str(self.score))
            else:
                file.write(str(self.highscore))

    def sorteia_quadrados(self):
        if self.sorteia:
            quadrado_sorteado = random.choice(self.quadrados) 
            self.cores_sorteadas.append(quadrado_sorteado[4]) # self.quadrados[4] = cor
            self.rect_sorteados.append([quadrado_sorteado[0], quadrado_sorteado[1], quadrado_sorteado[2], quadrado_sorteado[3]]) # self.quadrados[0:4]

    def desenha(self):
        self.window.blit(self.fundo_modo_escuro, (0, 0))
        Pontuacao(270, 150, f"Score: {str(self.score)}").desenha(self.window)
        Pontuacao(440, 150, f"High Score: {str(self.highscore)}").desenha(self.window)

        for quadrado_claro in self.quadrados_claros: # Desenha os quadrados claros
            quadrado_claro.desenha(self.window)

        for i in range(4): # Cria os retângulos para verificação do clique
            r = pygame.Rect(self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3])
            self.retangulos.append(r) 
    
            if self.mostra_quadrado or self.indice_quadrado >= len(self.cores_sorteadas) or self.cores[i] != self.cores_sorteadas[self.indice_quadrado]:
                pygame.draw.rect(self.window, self.cores[i], (self.quadrados[i][0], self.quadrados[i][1], self.quadrados[i][2], self.quadrados[i][3]))

    def update(self):
        self.tempo()
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
                
                if mouse_rect.colliderect(self.retangulos[0]):
                    self.sequencia_jogador.append(self.cores[0])
                    self.verificação_individual += 1
                    self.som0.play()
                elif mouse_rect.colliderect(self.retangulos[1]):
                    self.sequencia_jogador.append(self.cores[1])
                    self.verificação_individual += 1
                    self.som1.play()
                elif mouse_rect.colliderect(self.retangulos[2]):
                    self.sequencia_jogador.append(self.cores[2])
                    self.verificação_individual += 1
                    self.som2.play()
                elif mouse_rect.colliderect(self.retangulos[3]):
                    self.sequencia_jogador.append(self.cores[3])
                    self.verificação_individual += 1
                    self.som3.play()
                
                for i in range(len(self.sequencia_jogador)):
                    if self.sequencia_jogador[i] == self.cores_sorteadas[i]:
                        self.validacao_jogada = True
                    else: # Caso o jogador erre a sequência
                        self.save_score()
                        return TelaGameOverEscuro()
                    
                if self.sequencia_jogador == self.cores_sorteadas:
                    self.sorteia = True
                    self.score += 1
                    self.indice_quadrado = 0

            if len(self.sequencia_jogador) == len(self.cores_sorteadas):
                self.sequencia_jogador = []
            
        return self 
    
    def tempo(self):  
        self.tempo_passado = pygame.time.get_ticks() - self.tempo_start
        if self.tempo_passado > 650:
            self.mostra_quadrado = not self.mostra_quadrado
            self.tempo_start = pygame.time.get_ticks()
            if self.mostra_quadrado:
                self.indice_quadrado += 1

class TelaGameOverClassico(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('assets/snd/img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo):
                    return TelaClassico()                    
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self
    
class TelaGameOverRapido(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('assets/snd/img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo):
                    return TelaRapido()                    
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self
    
class TelaGameOverEscuro(Jogo):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption(GAME_OVER)
        self.game_over = pygame.image.load('assets/snd/img/Game-Over-Pattern-Pursuit.png')
        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    def update(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo):
                    return TelaEscuro()                    
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    return TelaInicial()
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit()
        return self