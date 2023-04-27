import pygame
import random
from sprites import *
from constantes import *


class Classico:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(MODO_CLASSICO)

        self.fundo_modo_classico = pygame.image.load('img/Modo-Classico.png')

        self.cores_claras = [AZUL, AMARELO, VERDE, VERMELHO]
        self.cores = [AZUL_ESCURO, AMARELO_ESCURO, VERDE_ESCURO, VERMELHO_ESCURO]

        self.circulos = [
            Circulos(300, 270, AZUL_ESCURO),
            Circulos(500, 270, AMARELO_ESCURO),
            Circulos(300, 470, VERDE_ESCURO),
            Circulos(500, 470, VERMELHO_ESCURO)
        ]

        self.circulos_claros = [
            CirculosClaros(300, 270, AZUL),
            CirculosClaros(500, 270, AMARELO),
            CirculosClaros(300, 470, VERDE),
            CirculosClaros(500, 470, VERMELHO) 
        ]

        self.sorteia = True
        self.mostra_circulo = True
        self.cores_sorteadas = []

    def sorteia_circulos(self):
        if self.sorteia:
            cor_sorteada = random.choice(self.cores)
            self.cores_sorteadas.append(cor_sorteada) # Sorteia e coloca a cor na lista das sorteadas

    def roda(self):
        self.jogando = True
        while self.jogando:
            self.botao_clicado = None # botão que o jogador clicou
            self.eventos()
            self.desenha()

    def desenha(self):
        self.window.blit(self.fundo_modo_classico, (0, 0))
        for circulo_claro in self.circulos_claros: # Desenha os circulos claros
            circulo_claro.desenha(self.window)
        for circulo in self.circulos: # Desenha os circulos escuros depois
            circulo.desenha(self.window)

        # AQUI SERLF.SORTEIA VIRA FALSE E O CIRCULO ESCURO SOME DA LISTA DOS SORTEADOS 

        pygame.display.update()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit(0)

jogo = Classico()
while True:
    jogo.roda()