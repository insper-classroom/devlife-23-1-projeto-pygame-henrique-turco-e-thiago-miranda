#loop e atualizacao da tela ensinado por leonardo freitas
from telas import *

# Roda o jogo, começando na tela inicial
tela_atual = TelaInicial()
while True:
    tela_atual.roda()
    tela_atual = tela_atual.update()