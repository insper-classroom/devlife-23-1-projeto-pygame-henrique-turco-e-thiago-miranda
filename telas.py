import pygame
import random
from sprites import *
from constantes import *

class Jogo:
    def __init__(self):
        pass

    def game_loop(self):
        pass


class TelaInicial:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TÍTULO)
        self.window = pygame.display.set_mode((LARGURA, ALTURA))

        self.fundo = pygame.image.load('img/Inicio-Pattern-Pursuit.png')

        self.rect_modo_classico = pygame.Rect(235, 190, 330, 90)
        self.rect_modo_rapido = pygame.Rect(235, 290, 330, 90)
        self.rect_modo_escuro = pygame.Rect(235, 390, 330, 90)
        self.rect_sair = pygame.Rect(235, 490, 330, 90)

    def roda(self):
        self.jogando = True
        while self.jogando:
            self.eventos()
            self.desenha()

    def desenha(self):
        self.window.blit(self.fundo, (0, 0))
        pygame.display.update()

    def update(self):
        jogo = Jogo()
        jogo.game_loop()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if evento.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_modo_classico):
                    self.jogando = False
                    self.modo_classico = True
                    self.modo_rapido = False
                    self.modo_escuro = False
                elif mouse_rect.colliderect(self.rect_modo_rapido):
                    self.jogando = False
                    self.modo_classico = False
                    self.modo_rapido = True
                    self.modo_escuro = False
                elif mouse_rect.colliderect(self.rect_modo_escuro):
                    self.jogando = False
                    self.modo_classico = False
                    self.modo_rapido = False
                    self.modo_escuro = True
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit(0)

# jogo = TelaInicial()
# while True:
#     jogo.roda()


class TelaGameOver:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_OVER)
        self.window = pygame.display.set_mode((LARGURA, ALTURA))

        self.game_over = pygame.image.load('img/Game-Over-Pattern-Pursuit.png')

        self.rect_tentar_de_novo = pygame.Rect(235, 282, 330, 90)
        self.rect_voltar_inicio = pygame.Rect(235, 382, 330, 90)
        self.rect_sair = pygame.Rect(235, 482, 330, 90)

    def roda(self):
        self.jogando = True
        while self.jogando:
            self.eventos()
            self.desenha()

    def desenha(self):
        self.window.blit(self.game_over, (0, 0))
        pygame.display.update()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if evento.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(x, y, 1, 1)
                if mouse_rect.colliderect(self.rect_tentar_de_novo):
                    self.jogando = False
                    self.tentar_de_novo = True
                    self.voltar_inicio = False
                elif mouse_rect.colliderect(self.rect_voltar_inicio):
                    self.jogando = False
                    self.tentar_de_novo = False
                    self.voltar_inicio = True
                elif mouse_rect.colliderect(self.rect_sair):
                    pygame.quit()
                    quit(0)


# jogo = TelaGameOver()
# while True:
#     jogo.roda()