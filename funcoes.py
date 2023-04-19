import pygame

from classes import Circulo

def inicializa():
    pygame.init()
    largura_janela = 900
    altura_janela = 600
    window = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption('Pattern Pursuit')

    circulos = []
    

    return window


def desenha(window):
    window.fill((0, 0, 0))

    pygame.display.update()


def atualiza_estado():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True